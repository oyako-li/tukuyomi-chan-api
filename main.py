from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.synthesizer import tts
from src.tokenizer import morphogenesis, tokenize, vectorise
from src.transcriber import transcribe
from src import body
import tempfile
import warnings
import base64
import json
import pyautogui as robot
import soundfile as sf
import numpy as np

warnings.simplefilter("ignore", UserWarning)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(body.router)


class AudioData(BaseModel):
    audio: str


@app.get("/")
def root():
    return "Hello World!"


@app.get("/tts", response_class=FileResponse)
async def get_tts(text: str):
    audio_bytes, sample_rate = tts(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        sf.write(tmpfile, audio_bytes, samplerate=sample_rate, format="WAV")
        return FileResponse(
            tmpfile.name,
            filename=f"{text.replace('/', '_')}.wav",
            media_type="audio/wav",
        )


@app.get("/morphologic")
async def get_morphologic(text: str):
    return json.dumps(morphogenesis(text))


@app.get("/tokenize")
async def get_token(text: str):
    tokens = tokenize(text)
    encoding = {k: v.tolist() for k, v in tokens.items()}
    return json.dumps(encoding)


@app.get("/vector")
async def get_vector(text: str):
    tokens = tokenize(text)
    vector = vectorise(tokens).tolist()
    return json.dumps(vector)


# テスト用にファイルをBase64エンコードしてPOSTする場合
@app.post("/upload_and_transcribe")
async def upload_and_transcribe(base64_audio: str):
    # Base64エンコードされたデータをデコード
    audio_bytes = base64.b64decode(base64_audio)
    return await post_transcribe(audio_bytes)


@app.post("/transcribe")
async def post_transcribe(data: AudioData):
    try:
        # ここでaudio_bytesを使用して必要な処理を行います（保存、解析など）
        audio_bytes = base64.b64decode(data.audio.split(",")[1])
        # バイト列からNumPy配列を作成
        # BytesIOを使用してメモリ上のバイナリストリームを作成し、wavfile.readに渡す
        audio_float = (
            np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        )
        result = transcribe(audio_float, fp16=False, language="ja")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/robot")
async def post_action():
    return robot.click()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
