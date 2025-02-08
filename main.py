from fastapi import FastAPI
from fastapi.responses import JSONResponse
import speech_recognition as sr
import os

app = FastAPI()

@app.post("/speech-to-text")
def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        # This will fail in Render because there is no microphone hardware!
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
    # Use the PORT environment variable provided by Render (default to 5000 for local testing)
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
