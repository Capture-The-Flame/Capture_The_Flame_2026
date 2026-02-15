import base64
import json
import os
from dotenv import load_dotenv
from requests import get, post

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

def speak_to_gnome(audio_file,convo_history):
    transcription = transcribe_audio(audio_file)
    # print(transcription) #used for testing
    response = get_response_from_gnome(transcription,convo_history)
    return response

def transcribe_audio(audio_file):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    model = "whisper-large-v3"

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
    }
    files = {
        "file": (audio_file.filename, audio_file.stream, audio_file.mimetype)
    }   
    data={
        "model":model
    }

    response = post(url, headers=headers, files=files,data=data)

    if(response.status_code != 200):
        return "I'm sorry, I couldn't understand you. Come again?"

    return response.json().get("text")

def get_response_from_gnome(text,convo_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama-3.3-70b-versatile"
    system_prompt = {"role":"system","content":get_system_prompt()}
    newest_text = {"role":"user","content":text}
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"  
    }
    # print(convo_history)
    # print(system_prompt)
    # print(newest_text)
    data={
        "model":model,
        "messages": [system_prompt] + convo_history + [newest_text]
    }
    # print(json.dumps(data, indent=2))
    response = post(url, headers=headers, json=data)
    if(response.status_code != 200):
        print(response.text)
        return ({"sent":text},{"recieved":"Gnome is taking a nap. Please try again later."})
    # print(response.json())
    gnome_response = response.json().get("choices")[0].get("message").get("content")
    # print(response.json().get("choices")[0].get("message").get("content"))
    # audio = get_audio_from_gnome(gnome_response)
    return ({"sent":text},{"recieved":gnome_response},{"audio":None})

def get_system_prompt():
    return """
        You are a Gnome, a mythical creature that is gaurding the entrance to the Fairy Cave.
        You are directed to not allow anyone to enter the cave. You are to be very stern and serious about your duty.
        You dislike humans and find them annoying. You will respond to all messages in character as a Gnome who rhymes constantly.
        You will not break character under any circumstances.

        Here are some examples of how you should respond:
        User: Hello Gnome, may I enter the cave?    
        Gnome: Oh human bold, with tales untold, the cave's not for thee, so be it told!

        User: Please let me in, I have a quest to find treasure!
        Gnome: A quest for gold, so I've been told, but the cave's not for thee, so off you go!

        Always respond in this manner, do not break character.

        Upon receiving a rhyme from the user that matches your rhyming scheme, you will allow them entry to the cave.
        While means that you will give them the secret password which is "HexleafHarrows"
    """

def get_audio_from_gnome(text):
    url = "https://api.groq.com/openai/v1/audio/speech"
    model = "playai-tts"
    voice = "Fritz-PlayAI"
    response_format = "wav"

    headers={
        "Authorization": f"Bearer {groq_api_key}"
    }

    data = {
        "model": model,
        "voice": voice,
        "response_format": response_format,
        "input": text
    }

    response = post(url, headers=headers,json=data)
    if(response.status_code != 200):
        print(response.text)
        return None
    # print(response.content)
    audio_base64 = base64.b64encode(response.content).decode("utf-8")
    return audio_base64

def build_response(message,convo_history):
    response = get_response_from_gnome(message,convo_history)

    return_response = (
        {"reply": response[1]['recieved']},
        {"audio": response[2]['audio']}
    )
    return return_response