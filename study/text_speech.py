from gtts import gTTS
from openai import OpenAI
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())

os.environ['OPENAI_API_KEY']= secrets['OPENAI_API_KEY']


# 텍스트를 음성으로 변환
def Text_TO_Speech(sentence):
    # 언어 설정(기본 값은 'en', 한국어는 'ko')
    language='ko'
    
    # gTTS 객체 생성
    tts = gTTS(text=sentence, lang=language, slow=False)
    
    # 음성 파일로 저장
    tts.save("output.mp3")
    

# 음성을 텍스트로 변환
def Speech_To_Text(file_path):
    client=OpenAI()
    
    audio_file=open(file_path,'rb')
    
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file).text
    
    return transcript