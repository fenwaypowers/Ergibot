import json, os
from urllib.parse import urlparse

def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def save_json(file: str, data: dict):
    "removes old file and then replaces it with fresh data @tpowell11"
    os.remove(file)  # delete outdated data
    dumpData = json.dumps(data)
    with open(file, 'w') as f:  # open file
        f.write(dumpData)  # write the new json
        f.close()

def load_json(jsonfilename : str):
    with open(jsonfilename, 'r') as file:
        data = file.read()
        output = json.loads(data)
        file.close()
    return output

def save_and_load_json(jsonfilename: str, data: dict):
    save_json(jsonfilename, data)
    return load_json(jsonfilename)

class Embedder():
    def __init__(self, video_link: str, image_link: str):
        self.domain = "https://discord.nfp.is/"
        self.vid_ind = "?v="
        self.img_ind = "&i="
        self.vid = video_link
        self.img = image_link
        self.link = self.domain + self.vid_ind + self.vid + self.img_ind + self.img
    
    @classmethod
    def fromlink(cls, link: str):
        vid_link = link.split("?v=")[1].split("&i")[0]
        img_link = link.split("&i=")[1]
        print(vid_link)
        print(img_link)

        return cls(vid_link, img_link)
    
    @classmethod
    def fromnothing(cls):
        return cls("https://valve-software.com/videos/gabeNewell.mp4", "https://cdn.discordapp.com/attachments/798075108853809163/1073687119194771456/gabeNewell.png")

    def __str__(self):
        return self.link