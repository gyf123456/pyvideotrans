# 去水印


def openwin():

    import json
    import os
    import time
    import threading
    from pathlib import Path
    from PySide6.QtCore import QThread, Signal, QUrl, QTimer
    from PySide6.QtGui import QDesktopServices
    from PySide6.QtWidgets import QFileDialog
    from videotrans.util import contants
    from videotrans.configure.config import tr, app_cfg, settings, params, TEMP_DIR, HOME_DIR, defaulelang
    from videotrans.util import tools

    class CompThread(QThread):
        uito = Signal(str)

        def __init__(self, *, parent=None, regions, mode=0):
            super().__init__(parent=parent)
            # regions: list of (x, y, w, h)
            self.regions = regions
            self.mode = int(mode)
            self.every_percent = 1 / max(len(winobj.videourls), 1)
            self.percent = 0
            self.end = False

        def post(self, type='logs', text=""):
            self.uito.emit(json.dumps({"type": type, "text": text}))

        def hebing_pro(self, protxt, video_time=0):
            percent = 0
            while 1:
                if app_cfg.exit_soft:
                    return
                if self.end or percent >= 100:
                    return
                content = tools.read_last_n_lines(protxt)
                if not content:
                    time.sleep(1)
                    continue
                if content[-1] == 'progress=end':
                    return
                idx = len(content) - 1
                end_time = "00:00:00"
                while idx > 0:
                    if content[idx].startswith('out_time='):
                        end_time = content[idx].split('=')[1].strip()
                        break
                    idx -= 1
                if video_time == 0:
                    self.post(type='jd', text=f'{end_time}')
                    time.sleep(1)
                    continue
                h, m, s = end_time.split(':')
                tmp1 = round((int(h) * 3600000 + int(m) * 60000 + int(s[:2]) * 1000) / video_time, 2)
                if percent + tmp1 < 99.9:
                    percent += tmp1
                self.percent += percent * self.every_percent / 100
                self.post(type='jd', text=f'{self.percent * 100}%')
                time.sleep(1)

        def run(self) -> None:
            for video in winobj.videourls:
                video_dir = str(Path(video).parent)
                result_file = os.path.join(video_dir, f'{Path(video).stem}_no_watermark.mp4')

                if self.mode == 0:
                    self._run_delogo(video, result_file)
                else:
                    self._run_lama(video, result_file)

                self.percent += self.every_percent
                self.post(type='jd', text=f'{self.percent * 100}%')

            self.post(type='ok', text='Ended')
            self.end = True

        def _run_delogo(self, video, result_file):
            duration = tools.get_video_duration(video)
            protxt = TEMP_DIR + f'/jd{time.time()}.txt'
            threading.Thread(target=self.hebing_pro, args=(protxt, duration), daemon=True).start()

            # Chain multiple delogo filters: delogo=...,delogo=...
            vf = ",".join(
                f"delogo=x={x}:y={y}:w={w}:h={h}"
                for x, y, w, h in self.regions
            )
            ffmpeg_command = [
                "-y",
                "-progress", protxt,
                "-i", os.path.normpath(video),
                "-vf", vf,
                "-c:v", "libx265",
                "-crf", f"{settings.get('crf', 26)}",
                "-preset", f"{settings.get('preset', 'fast')}",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                result_file
            ]
            try:
                tools.runffmpeg(ffmpeg_command, force_cpu=False)
            except Exception as e:
                from videotrans.configure._except import get_msg_from_except
                self.post(type='error', text=get_msg_from_except(e))

        def _run_lama(self, video, result_file):
            try:
                from videotrans.util.lama_inpaint import lama_remove_watermark
                model_dir = os.path.join(os.path.dirname(TEMP_DIR), "models", "lama")

                def on_progress(pct):
                    if pct < 0:
                        self.post(type='logs', text=(
                            "正在下载 LaMa 模型..." if defaulelang == 'zh'
                            else "Downloading LaMa model..."
                        ))
                    else:
                        total_pct = self.percent + (pct / 100) * self.every_percent
                        self.post(type='jd', text=f'{total_pct * 100:.1f}%')

                lama_remove_watermark(
                    video, result_file,
                    self.regions,
                    model_dir=model_dir,
                    progress_callback=on_progress
                )
            except Exception as e:
                from videotrans.configure._except import get_msg_from_except
                self.post(type='error', text=get_msg_from_except(e))

    def feed(d):
        if winobj.has_done:
            return
        d = json.loads(d)
        if d['type'] == "error":
            winobj.has_done = True
            tools.show_error(d['text'])
            winobj.startbtn.setText(tr("Start operating"))
            winobj.startbtn.setDisabled(False)
            winobj.resultlabel.setText('')
        elif d['type'] == 'jd':
            winobj.startbtn.setText(d['text'])
        elif d['type'] == 'logs':
            winobj.resultlabel.setText(d['text'])
        else:
            winobj.has_done = True
            winobj.startbtn.setText(tr('zhixingwc'))
            winobj.startbtn.setDisabled(False)
            winobj.resultlabel.setText(tr('quanbuend'))
            winobj.resultbtn.setDisabled(False)

    def get_file():
        format_str = " ".join(['*.' + f for f in contants.VIDEO_EXTS])
        fname, _ = QFileDialog.getOpenFileNames(winobj, "Select Video",
                                                params['last_opendir'],
                                                f"Video files({format_str})")
        if fname:
            winobj.videourls = [it.replace('file:///', '').replace('\\', '/') for it in fname]
            winobj.videourl.setText(",".join(winobj.videourls))

    def select_region():
        if not winobj.videourls:
            tools.show_error(
                "请先选择视频文件" if defaulelang == 'zh'
                else "Please select a video file first"
            )
            return
        from videotrans.component.region_selector import RegionSelectorDialog
        dlg = RegionSelectorDialog(winobj.videourls[0], parent=winobj)
        if dlg.exec() and dlg.result:
            x, y, w, h = dlg.result
            label = f"x={x}  y={y}  w={w}  h={h}"
            winobj.regions_list.addItem(label)

    def delete_region():
        row = winobj.regions_list.currentRow()
        if row >= 0:
            winobj.regions_list.takeItem(row)

    def _get_regions():
        regions = []
        for i in range(winobj.regions_list.count()):
            text = winobj.regions_list.item(i).text()
            # parse "x=10  y=20  w=100  h=50"
            parts = {}
            for token in text.split():
                k, v = token.split('=')
                parts[k.strip()] = int(v.strip())
            regions.append((parts['x'], parts['y'], parts['w'], parts['h']))
        return regions

    def start():
        winobj.has_done = False
        if not winobj.videourls:
            tools.show_error(
                "必须选择视频文件" if defaulelang == 'zh'
                else "Must select video files"
            )
            return

        regions = _get_regions()
        if not regions:
            tools.show_error(
                "请至少添加一个水印区域" if defaulelang == 'zh'
                else "Please add at least one watermark region"
            )
            return

        mode = winobj.combo_mode.currentIndex()
        winobj.startbtn.setText(tr("under implementation in progress..."))
        winobj.startbtn.setDisabled(True)
        winobj.resultbtn.setDisabled(True)

        task = CompThread(parent=winobj, regions=regions, mode=mode)
        task.uito.connect(feed)
        task.start()

    def opendir():
        target = str(Path(winobj.videourls[0]).parent) if winobj.videourls else HOME_DIR
        QDesktopServices.openUrl(QUrl.fromLocalFile(target))

    from videotrans.component.set_form import DewatermarkForm
    winobj = DewatermarkForm()
    app_cfg.child_forms['fn_dewatermark'] = winobj
    winobj.show()

    def _bind():
        winobj.videobtn.clicked.connect(get_file)
        winobj.select_region_btn.clicked.connect(select_region)
        winobj.delete_region_btn.clicked.connect(delete_region)
        winobj.resultbtn.clicked.connect(opendir)
        winobj.startbtn.clicked.connect(start)

    QTimer.singleShot(10, _bind)
