import requests
import glob

phonemes = ["bah", "ow", "uw"]

for phoneme in phonemes:
    for i in range(1,38):
        file_name = f"soundfont/{phoneme}_{i}.wav"
        print(file_name)

        poo = requests.get("https://tts.cyzon.us/tts", params={"text": f"[:phoneme on] [{phoneme}<10000,{i}>]"})

        with open(file_name, "wb") as fh:
            fh.write(poo.content)