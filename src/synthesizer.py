import time
import torch
import soundfile as sf

from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none

lang = "Japanese"
tag = "kan-bayashi/tsukuyomi_full_band_vits_prosody"
vocoder_tag = "none"

# Use device="cuda" if you have GPU
text2speech = Text2Speech.from_pretrained(
    model_tag=str_or_none(tag),
    vocoder_tag=str_or_none(vocoder_tag),
    device="cpu",
    # Only for Tacotron 2 & Transformer
    threshold=0.5,
    # Only for Tacotron 2
    minlenratio=0.0,
    maxlenratio=10.0,
    use_att_constraint=False,
    backward_window=1,
    forward_window=3,
    # Only for FastSpeech & FastSpeech2 & VITS
    speed_control_alpha=1.0,
    # Only for VITS
    noise_scale=0.333,
    noise_scale_dur=0.333,
)


def tts(text: str):
    with torch.no_grad():
        wav = text2speech(text)["wav"]
    wav_data = wav.view(-1).cpu().numpy()
    sample_rate = text2speech.fs
    return wav_data, sample_rate


if __name__ == "__main__":
    x = "お兄ちゃん　朝だよ　起きて"

    ts = text2speech(x)
    print(ts)

    # synthesis
    with torch.no_grad():
        start = time.time()
        wav = text2speech(x)["wav"]
    rtf = (time.time() - start) / (len(wav) / text2speech.fs)
    print(f"RTF = {rtf:5f}")

    wavdata = wav.view(-1).cpu().numpy()
    samplerate = text2speech.fs

    sf.write(f"./data/{x.replace('/','_')}.wav", wavdata, samplerate, subtype="PCM_24")
