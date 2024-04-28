from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from synthesize import tts
import soundfile as sf
import tempfile
import warnings

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
