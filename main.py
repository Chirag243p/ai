from fastapi import FastAPI, HTTPException
import speech_recognition as sr
import openai
import os

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

@app.post("/speech-to-text")
async def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        # Use the microphone as source for input.
        # This will only work in an environment with a microphone.
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for your voice command...")
            audio_data = recognizer.listen(source)

        # Convert speech to text using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized text: {text}")

        # Send the transcribed text to OpenAI and get a response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # or "gpt-3.5-turbo" as needed
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
