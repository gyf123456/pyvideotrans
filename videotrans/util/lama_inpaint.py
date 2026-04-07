import os
import time
import glob
import numpy as np
import torch
from pathlib import Path

from videotrans.configure.config import logger, TEMP_DIR


def download_lama_model(model_dir):
    """Return model path, downloading via mirror fallback if not present."""
    model_path = os.path.join(model_dir, "big-lama.pt")
    if os.path.exists(model_path):
        return model_path
    os.makedirs(model_dir, exist_ok=True)

    from videotrans.util.help_down import is_connect_hf
    import huggingface_hub

    endpoint = 'https://hf-mirror.com'
    logger.info(f"Downloading big-lama model via {endpoint} ...")
    huggingface_hub.hf_hub_download(
        repo_id="fashn-ai/LaMa",
        filename="big-lama.pt",
        local_dir=model_dir,
        endpoint=endpoint,
    )
    return model_path


def _load_model(model_path, device):
    """Load TorchScript LaMa model."""
    model = torch.jit.load(model_path, map_location=device)
    model.eval()
    return model


def _inpaint_frame(model, frame_rgb, mask, device):
    """
    Run LaMa inpainting on a single frame.
    frame_rgb: H x W x 3 uint8
    mask: H x W uint8 (255 = inpaint region)
    Returns: H x W x 3 uint8
    """
    h, w = frame_rgb.shape[:2]
    # Pad to multiple of 8
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    if pad_h or pad_w:
        frame_rgb = np.pad(frame_rgb, ((0, pad_h), (0, pad_w), (0, 0)), mode='reflect')
        mask = np.pad(mask, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0)

    # Normalize
    img_t = torch.from_numpy(frame_rgb).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    mask_t = torch.from_numpy(mask).unsqueeze(0).unsqueeze(0).float() / 255.0

    img_t = img_t.to(device)
    mask_t = mask_t.to(device)

    with torch.no_grad():
        result = model(img_t, mask_t)

    result = result[0].permute(1, 2, 0).cpu().numpy()
    result = np.clip(result * 255, 0, 255).astype(np.uint8)

    # Remove padding
    if pad_h or pad_w:
        result = result[:h, :w]
    return result


def _compute_flow(prev_gray, curr_gray):
    """Compute optical flow between two grayscale frames."""
    import cv2
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray,
        None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2,
        flags=0
    )
    return flow


def _blend_with_flow(prev_result, curr_result, flow, mask, alpha=0.6):
    """Blend current inpainted frame with warped previous using optical flow."""
    import cv2
    h, w = curr_result.shape[:2]
    flow_map = np.column_stack((
        np.repeat(np.arange(w)[np.newaxis, :], h, axis=0).flatten(),
        np.repeat(np.arange(h)[:, np.newaxis], w, axis=1).flatten()
    )).reshape(h, w, 2).astype(np.float32)
    flow_map += flow
    warped = cv2.remap(prev_result, flow_map[:, :, 0], flow_map[:, :, 1], cv2.INTER_LINEAR)

    # Only blend in the mask region
    mask_3c = np.stack([mask, mask, mask], axis=2).astype(np.float32) / 255.0
    blended = (alpha * curr_result.astype(np.float32) +
               (1 - alpha) * warped.astype(np.float32))
    result = curr_result.copy()
    result = np.where(mask_3c > 0.5,
                      np.clip(blended, 0, 255).astype(np.uint8),
                      curr_result)
    return result


def lama_remove_watermark(video_path, output_path, regions, *,
                          model_dir=None, progress_callback=None):
    """
    Remove watermarks from video using LaMa AI inpainting with optical flow smoothing.

    Args:
        video_path: Input video file path
        output_path: Output video file path
        regions: list of (x, y, w, h) tuples — one per watermark region
        model_dir: Directory for model storage
        progress_callback: callable(percent_float) for progress updates
    """
    import cv2
    from videotrans.util import tools

    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(TEMP_DIR), "models", "lama")

    model_path = download_lama_model(model_dir)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    model = _load_model(model_path, device)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    # Build combined mask from all regions
    mask = np.zeros((frame_h, frame_w), dtype=np.uint8)
    for x, y, w, h in regions:
        x1 = max(0, int(x))
        y1 = max(0, int(y))
        x2 = min(frame_w, x1 + int(w))
        y2 = min(frame_h, y1 + int(h))
        mask[y1:y2, x1:x2] = 255

    # Process frames
    out_frames_dir = os.path.join(TEMP_DIR, f"lama_out_{int(time.time())}")
    os.makedirs(out_frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    prev_gray = None
    prev_result = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Inpaint
        inpainted = _inpaint_frame(model, frame_rgb, mask, device)

        # Optical flow temporal smoothing
        if prev_gray is not None and prev_result is not None:
            flow = _compute_flow(prev_gray, gray)
            inpainted = _blend_with_flow(prev_result, inpainted, flow, mask)

        prev_gray = gray
        prev_result = inpainted

        # Save frame
        out_frame = cv2.cvtColor(inpainted, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(out_frames_dir, f"{frame_idx:08d}.png"), out_frame)

        frame_idx += 1
        if progress_callback and total_frames > 0:
            progress_callback(frame_idx / total_frames * 100)

    cap.release()

    # Reassemble with FFmpeg (copy audio from original)
    ffmpeg_cmd = [
        "-y",
        "-framerate", str(fps),
        "-i", os.path.join(out_frames_dir, "%08d.png"),
        "-i", os.path.normpath(video_path),
        "-map", "0:v",
        "-map", "1:a?",
        "-c:v", "libx265",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        os.path.normpath(output_path)
    ]
    tools.runffmpeg(ffmpeg_cmd, force_cpu=False)

    # Cleanup temp frames
    import shutil
    shutil.rmtree(out_frames_dir, ignore_errors=True)
