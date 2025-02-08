from fastapi import FastAPI, HTTPException, File, UploadFile
import speech_recognition as sr
import openai
import os

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()

    try:
        # Read the uploaded audio file
        with open("temp_audio.wav", "wb") as buffer:
            buffer.write(await file.read())

        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio)

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
