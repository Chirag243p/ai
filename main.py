from fastapi import FastAPI, HTTPException, File, UploadFile
import speech_recognition as sr
import openai
import io
import os

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

@app.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    recognizer = sr.Recognizer()

    try:
        # Read the audio file bytes
        audio_bytes = await audio_file.read()
        audio_file_obj = io.BytesIO(audio_bytes)

        # Use AudioFile to process the uploaded file
        with sr.AudioFile(audio_file_obj) as source:
            audio_data = recognizer.record(source)

        # Convert speech to text using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized text: {text}")

        # Send the transcribed text to OpenAI and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[{"role": "user", "content": text}]
        )

        # Extract ChatGPT response
        chatgpt_response = response['choices'][0]['message']['content'].strip()

        return {"text": text, "chatgpt_response": chatgpt_response}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand the audio.")
    except sr.RequestError:
        raise HTTPException(status_code=500, detail="Speech recognition service error.")
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
