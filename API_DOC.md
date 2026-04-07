# pyvideotrans HTTP API 文档

## 启动服务

```bash
# 默认监听 0.0.0.0:9011
uv run python api.py

# 自定义地址和端口
uv run python api.py --host 127.0.0.1 --port 8080
```

启动成功后终端会输出：

```
Checking GPUs...
Starting API server on 0.0.0.0:9011
```

---

## API 端点总览

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/upload` | POST | 上传文件 |
| `/api/task` | POST | 提交翻译任务 |
| `/api/task/<task_id>` | GET | 查询任务状态与日志 |
| `/api/tasks` | GET | 列出所有任务 |

所有响应均为 JSON，基本结构：

```json
{
    "code": 0,
    "msg": "ok",
    "data": {}
}
```

`code` 为 `0` 表示成功，非 `0` 表示失败，`msg` 中包含错误信息。

---

## 1. 上传文件

**POST** `/api/upload`

Content-Type: `multipart/form-data`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 要上传的文件 |

### 请求示例

```bash
curl -F "file=@/home/user/videos/test.mp4" http://localhost:9011/api/upload
```

### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "filepath": "/path/to/pyvideotrans/upload/test.mp4"
    }
}
```

> 返回的 `filepath` 即为服务端文件路径，后续提交任务时作为 `name` 参数使用。

---

## 2. 提交任务

**POST** `/api/task`

Content-Type: `application/json`

### 公共参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | string | 是 | 任务类型：`stt` / `tts` / `sts` / `vtv` |
| name | string | 是 | 文件绝对路径（可使用上传接口返回的 filepath） |

### 2.1 语音转录 (STT)

将音频/视频中的语音转录为字幕文件。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| recogn_type | int | 0 | 语音识别渠道（0=faster-whisper, 1=openai-whisper, ...） |
| detect_language | string | "auto" | 音频语言代码 |
| model_name | string | "tiny" | 模型名称（tiny/small/base/medium/large-v3-turbo/large-v1/large-v2/large-v3） |
| is_cuda | bool | false | 是否使用 CUDA 加速 |
| remove_noise | bool | false | 是否降噪 |
| enable_diariz | bool | false | 是否启用说话人识别 |
| nums_diariz | int | -1 | 指定说话人数量（-1 为自动） |
| rephrase | int | 0 | 重新断句（0=不处理, 1=LLM 断句） |
| fix_punc | bool | false | 是否恢复标点符号 |

#### 请求示例

```bash
curl -X POST http://localhost:9011/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "stt",
    "name": "/path/to/pyvideotrans/upload/test.mp4",
    "recogn_type": 0,
    "model_name": "tiny",
    "detect_language": "en",
    "is_cuda": false
  }'
```

#### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "task_id": "a1b2c3d4e5",
        "target_dir": "/path/to/pyvideotrans/output/test-mp4"
    }
}
```

---

### 2.2 文字配音 (TTS)

将字幕文件合成为语音。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| tts_type | int | 0 | 配音渠道 |
| voice_role | string | **必填** | 音色名称（具体可用值请在 GUI 中查看） |
| voice_rate | string | "+0%" | 语速 |
| volume | string | "+0%" | 音量 |
| pitch | string | "+0Hz" | 音调 |
| is_cuda | bool | false | 是否使用 CUDA 加速 |
| voice_autorate | bool | false | 自动加速音频以对齐字幕 |
| align_sub_audio | bool | false | 强制对齐字幕与音频 |
| target_language_code | string | null | 目标语言代码 |

#### 请求示例

```bash
curl -X POST http://localhost:9011/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "tts",
    "name": "/path/to/pyvideotrans/upload/subtitle.srt",
    "tts_type": 0,
    "voice_role": "zh-CN-XiaoxiaoNeural",
    "voice_rate": "+0%",
    "target_language_code": "zh-cn"
  }'
```

#### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "task_id": "f6g7h8i9j0",
        "target_dir": "/path/to/pyvideotrans/output/subtitle-srt"
    }
}
```

---

### 2.3 字幕翻译 (STS)

将字幕文件翻译为另一种语言。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| translate_type | int | 0 | 翻译渠道 |
| source_language_code | string | "auto" | 原始语言代码 |
| target_language_code | string | **必填** | 目标语言代码 |

#### 请求示例

```bash
curl -X POST http://localhost:9011/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "sts",
    "name": "/path/to/pyvideotrans/upload/subtitle.srt",
    "translate_type": 0,
    "source_language_code": "en",
    "target_language_code": "zh-cn"
  }'
```

#### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "task_id": "k1l2m3n4o5",
        "target_dir": "/path/to/pyvideotrans/output/subtitle-srt"
    }
}
```

---

### 2.4 视频翻译 (VTV)

完整的视频翻译流程：语音识别 -> 字幕翻译 -> 配音 -> 合成输出。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| source_language_code | string | **必填** | 原始语言代码（不可为 auto） |
| target_language_code | string | **必填** | 目标语言代码 |
| recogn_type | int | 0 | 语音识别渠道 |
| model_name | string | "tiny" | 语音识别模型 |
| is_cuda | bool | false | CUDA 加速 |
| remove_noise | bool | false | 降噪 |
| enable_diariz | bool | false | 说话人识别 |
| nums_diariz | int | -1 | 说话人数量 |
| rephrase | int | 0 | 重新断句 |
| fix_punc | bool | false | 恢复标点 |
| tts_type | int | 0 | 配音渠道 |
| voice_role | string | "No" | 音色（"No" 表示不配音） |
| voice_rate | string | "+0%" | 语速 |
| volume | string | "+0%" | 音量 |
| pitch | string | "+0Hz" | 音调 |
| voice_autorate | bool | false | 自动加速音频 |
| video_autorate | bool | false | 自动慢速视频 |
| align_sub_audio | bool | false | 强制对齐字幕与音频 |
| translate_type | int | 0 | 翻译渠道 |
| is_separate | bool | false | 分离人声与背景音 |
| recogn2pass | bool | false | 二次语音识别 |
| subtitle_type | int | 1 | 字幕嵌入类型（0=无, 1=硬字幕, 2=软字幕, 3=硬双语, 4=软双语） |
| clear_cache | bool | true | 完成后是否清理缓存 |

#### 请求示例

```bash
curl -X POST http://localhost:9011/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "vtv",
    "name": "/path/to/pyvideotrans/upload/test.mp4",
    "source_language_code": "en",
    "target_language_code": "zh-cn",
    "recogn_type": 0,
    "model_name": "tiny",
    "is_cuda": false,
    "tts_type": 0,
    "voice_role": "zh-CN-XiaoxiaoNeural",
    "subtitle_type": 1,
    "is_separate": false
  }'
```

#### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "task_id": "p6q7r8s9t0",
        "target_dir": "/path/to/pyvideotrans/output/test-mp4"
    }
}
```

---

## 3. 查询任务状态

**GET** `/api/task/<task_id>`

每次请求会排空该任务累积的日志，追加到返回结果的 `logs` 列表中。

### 请求示例

```bash
curl http://localhost:9011/api/task/a1b2c3d4e5
```

### 响应示例

```json
{
    "code": 0,
    "data": {
        "task_id": "a1b2c3d4e5",
        "status": "running",
        "task_type": "vtv",
        "file": "/path/to/pyvideotrans/upload/test.mp4",
        "target_dir": "/path/to/pyvideotrans/output/test-mp4",
        "error": null,
        "logs": [
            {"text": "正在识别语音...", "type": "logs", "uuid": "a1b2c3d4e5"},
            {"text": "语音识别完成", "type": "logs", "uuid": "a1b2c3d4e5"}
        ]
    }
}
```

### 任务状态说明

| status | 说明 |
|--------|------|
| pending | 已提交，等待执行 |
| running | 正在执行 |
| done | 执行完成，输出文件在 `target_dir` 中 |
| error | 执行失败，详情见 `error` 字段 |

---

## 4. 列出所有任务

**GET** `/api/tasks`

返回所有任务的摘要信息（不含完整日志）。

### 请求示例

```bash
curl http://localhost:9011/api/tasks
```

### 响应示例

```json
{
    "code": 0,
    "data": [
        {
            "task_id": "a1b2c3d4e5",
            "status": "done",
            "task_type": "vtv",
            "file": "/path/to/pyvideotrans/upload/test.mp4",
            "target_dir": "/path/to/pyvideotrans/output/test-mp4",
            "error": null,
            "created_at": 1711360000.123
        },
        {
            "task_id": "f6g7h8i9j0",
            "status": "running",
            "task_type": "stt",
            "file": "/path/to/pyvideotrans/upload/audio.wav",
            "target_dir": "/path/to/pyvideotrans/output/audio-wav",
            "error": null,
            "created_at": 1711360100.456
        }
    ]
}
```

---

## 完整工作流示例

以下演示一个完整的「上传文件 -> 提交视频翻译任务 -> 轮询状态」流程。

### 第一步：上传视频文件

```bash
curl -F "file=@./my_video.mp4" http://localhost:9011/api/upload
```

返回：

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "filepath": "/path/to/pyvideotrans/upload/my_video.mp4"
    }
}
```

### 第二步：提交视频翻译任务

```bash
curl -X POST http://localhost:9011/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "vtv",
    "name": "/path/to/pyvideotrans/upload/my_video.mp4",
    "source_language_code": "en",
    "target_language_code": "zh-cn",
    "model_name": "tiny",
    "voice_role": "No",
    "subtitle_type": 1
  }'
```

返回：

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "task_id": "a1b2c3d4e5",
        "target_dir": "/path/to/pyvideotrans/output/my_video-mp4"
    }
}
```

### 第三步：轮询任务状态

```bash
# 每隔几秒查询一次，直到 status 变为 done 或 error
curl http://localhost:9011/api/task/a1b2c3d4e5
```

当 `status` 为 `done` 时，翻译后的文件位于 `target_dir` 目录中。

---

## 常用语言代码

| 代码 | 语言 |
|------|------|
| zh-cn | 简体中文 |
| zh-tw | 繁体中文 |
| en | 英语 |
| ja | 日语 |
| ko | 韩语 |
| fr | 法语 |
| de | 德语 |
| es | 西班牙语 |xx
| ru | 俄语 |
| ar | 阿拉伯语 |

> 完整语言代码列表请参考项目中 `translator.LANGNAME_DICT` 的定义。
