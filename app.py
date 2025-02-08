from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import speech_recognition as sr

app = FastAPI()

@app.post("/speech-to-text")
def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        # Use the microphone as the audio source.
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Recognize the speech using Google's Web Speech API
        text = recognizer.recognize_google(audio)
        return {"recognized_text": text}

    except sr.UnknownValueError:
        return JSONResponse(content={"error": "Could not understand the audio."}, status_code=400)
    except sr.RequestError:
        return JSONResponse(content={"error": "Speech recognition service error."}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
