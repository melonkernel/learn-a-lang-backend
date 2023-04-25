import pytube
import time
import json
import hashlib
import os
from glob import glob
from cryptography.fernet import Fernet
import uuid

# Initialize the device
#device = "cuda" if torch.cuda.is_available() else "cpu"
#model = whisper.load_model("base", device=device)

QUEUE_FOLDER = 'queue'
ENCRYPT_KEY = 'vBgCrKSte2WJe5S1Jq-97K0k4-PZZkIzk-Z5pDEKtwc=' #Fernet.generate_key()
fernet = Fernet(ENCRYPT_KEY)

def determineSource(url):
    return 'youtube'

def cleanUrl(url):
    source = determineSource(url)
    if source == 'youtube':
        id = pytube.extract.video_id(url)
        return 'https://www.youtube.com/watch?v=' + id
    else:
        return url

def uuidFromUrl(url):
    return str(uuid.uuid3(uuid.NAMESPACE_URL, cleanUrl(url)))

def determineId(url):
    source = determineSource(url)
    if source == 'youtube':
        return pytube.extract.video_id(url)
    else:
        return hashlib.md5(url.encode()).hexdigest()

def mediaIsAlreadyQueued(url):
    file_part = createFileNameWithoutDate(url)
    fileList = glob(QUEUE_FOLDER + "/*" + file_part)
    for trueFile in fileList:
        return True
    return False

def createFileNameWithoutDate(url):
    return "---" + uuidFromUrl(url) + ".json"

def createFileName(url):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = QUEUE_FOLDER + "/" + timestr + createFileNameWithoutDate(url)
    return file

def getTimeStrFromFile(filepath):
    file = os.path.basename(filepath)
    timestr, _ = file.split('---')
    return timestr

def createMediaQueueEntry(url):
    url = cleanUrl(url)
    if (not mediaIsAlreadyQueued(url)):
        file = createFileName(url)
        timestr = getTimeStrFromFile(file)
        dictionary = {
            "source": 'youtube',
            "url": url,
            "timestr": timestr
        }
        json.dumps(dictionary, indent = 4)
        with open(file, "w") as outfile:
            json.dump(dictionary, outfile)
        return str(file)
    else:
        return "Media is queued"

 