import whisper

model = whisper.load_model("large")


def transcribe(wav, language="ja", fp16=False):
    return model.transcribe(wav, language=language, fp16=fp16)
