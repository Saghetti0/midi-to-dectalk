import requests
import glob

for file in glob.glob("outtext/out_*"):
    print(file)

    with open(file, "r") as fh:
        contents = fh.read()

    poo = requests.get("https://tts.cyzon.us/tts", params={"text": contents})

    with open("outwav/" + (file.split("/")[1]).split(".")[0] + ".wav", "wb") as fh:
        fh.write(poo.content)
