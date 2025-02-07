from fastapi import FastAPI, HTTPException
import speech_recognition as sr
import openai

# Set your OpenAI API key here
openai.api_key = OPENKEY

# FastAPI app initialization
app = FastAPI()

@app.post("/speech-to-text")
async def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        # Using Microphone as source to record audio
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Convert speech to text using Google Speech Recognition API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")

        # Send the transcribed text to OpenAI and get a response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # You can change this to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": text}]
        )

        # Extract the response from OpenAI
        chatgpt_answer = response['choices'][0]['message']['content'].strip()

        # Return the OpenAI response as JSON
        return {"text": text, "chatgpt_response": chatgpt_answer}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand the audio.")
    except sr.RequestError:
        raise HTTPException(status_code=500, detail="Speech recognition service error.")
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
