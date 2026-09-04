from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile

def synthesize(text, lang_code, output_filename):
    print(f"Loading model for '{lang_code}'...")
    model = VitsModel.from_pretrained(f"facebook/mms-tts-{lang_code}")
    tokenizer = AutoTokenizer.from_pretrained(f"facebook/mms-tts-{lang_code}")

    inputs = tokenizer(text, return_tensors="pt")

    print(f"Synthesizing: \"{text}\"")
    with torch.no_grad():
        output = model(**inputs).waveform

    scipy.io.wavfile.write(
        output_filename,
        rate=model.config.sampling_rate,
        data=output.squeeze().numpy()
    )
    print(f"Saved to {output_filename}\n")

# Y1-1 — rated 5/5/5 with YarnGPT
synthesize("Ẹ káàárọ̀", "yor", "test_Y1-1_kaaro.wav")

# Y1-5 — rated 5/5/5 with YarnGPT
synthesize("Ẹ ṣéun púpọ̀", "yor", "test_Y1-5_seun.wav")

# Y1-8 — rated 4/4/5 with YarnGPT (medium-length, translation issue not TTS issue)
synthesize("Iye ọjà yìí jẹ́ èló?", "yor", "test_Y1-8_iye.wav")

print("Done. Play all three and compare against how these sounded in your original evaluation.")