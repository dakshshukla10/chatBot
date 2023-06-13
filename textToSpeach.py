import requests
from decouple import config
import os

ELEVEN_LABS_API_KEY = os.environ["ELEVEN_LABS_API_KEY"]

# Eleven Labs
# Convert text to speech
def convertTextToSpeech(message):
  body = {
    "text": message,
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
  }

  voice_shaun = "mTSvIrm2hmcnOvb21nW2"
  voice_rachel = "21m00Tcm4TlvDq8ikWAM"
  voice_antoni = "ErXwobaYiN019PkySvjV"

  # Construct request headers and url
  headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

  try:
    response = requests.post(endpoint, json=body, headers=headers)
  except Exception as e:
     return

  if response.status_code == 200:
      with open("output.wav", "wb") as f:
          f.write(response.content)
      return 
  else:
    return
