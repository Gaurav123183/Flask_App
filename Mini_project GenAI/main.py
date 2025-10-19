from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv




env_loaded = load_dotenv("api.env")

api_key = os.getenv("OPENAI_API_KEY")




client = OpenAI(api_key=api_key)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/info", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form["prompt"]
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200
        )
        response_text = completion.choices[0].message.content
    return render_template("info.html", response=response_text)


@app.route("/image", methods=["GET", "POST"])
def image():
    image_url = ""
    if request.method == "POST":
        img = request.form["input"]
        img_response = client.images.generate(
            model="dall-e-3",
            prompt=img,
            size="1024x1024",
        )
        image_url = img_response.data[0].url
    return render_template("image.html", image_url=image_url)


@app.route("/textToSpeech", methods=["GET", "POST"])
def texttospeech():
    text = ""
    audio_url = ""

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("textToSpeech.html", error="No file uploaded.")

        file = request.files["file"]
        if file.filename == "":
            return render_template("textToSpeech.html", error="Empty file name.")

        text = file.read().decode("utf-8", errors="ignore")

        # Save speech to static folder
        output_path = "static/speech.mp3"

        # Generate speech using OpenAI API
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )

       
        with open(output_path, "wb") as f:
            f.write(response.content)

        audio_url = "/static/speech.mp3"

    return render_template("textToSpeech.html", text=text, audio_url=audio_url)

print("API Key loaded:", api_key[:8], "********")

if __name__ == "__main__":
    app.run(debug=True)
