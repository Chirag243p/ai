from fastapi import FastAPI, HTTPException, File, UploadFile
import speech_recognition as sr
import openai
import os
from pydub import AudioSegment

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    audio_path = "temp_audio.wav"

    try:
        # Convert file to WAV format
        audio = await file.read()
        with open(audio_path, "wb") as f:
            f.write(audio)

        # Use pydub to convert to WAV if needed
        if not file.filename.endswith(".wav"):
            sound = AudioSegment.from_file(audio_path)
            sound.export(audio_path, format="wav")

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio_data)

        # Send text to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": text}]
        )

        return {"text": text, "chatgpt_response": response['choices'][0]['message']['content'].strip()}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand the audio.")
    except sr.RequestError:
        raise HTTPException(status_code=500, detail="Speech recognition service error.")
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
