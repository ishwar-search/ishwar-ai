
import os
from flask import Flask, render_template, request, jsonify

from google import genai
from google.genai import types

app = Flask(__name__)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "app": "Ishwar AI",
        "ai_configured": bool(os.getenv("GEMINI_API_KEY"))
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "success": False,
            "reply": "भैया, पहले अपना सवाल लिखिए।"
        }), 400

    if len(message) > 4000:
        return jsonify({
            "success": False,
            "reply": "कृपया 4000 अक्षरों से छोटा सवाल भेजें।"
        }), 400

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "success": False,
            "reply": "Gemini API key सर्वर पर सेट नहीं है।"
        }), 503

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are Ishwar AI, a helpful assistant. "
                    "Answer clearly and accurately. "
                    "Reply in Hindi when the user writes in Hindi. "
                    "If you are unsure, say so honestly."
                ),
                max_output_tokens=700,
                temperature=0.7
            )
        )

        answer = response.text

        if not answer:
            answer = "इस बार जवाब नहीं मिल पाया। कृपया दोबारा कोशिश करें।"

        return jsonify({
            "success": True,
            "reply": answer
        })

    except Exception as error:
        # Details go to server logs, not to the public website.
       app.logger.exception("Gemini API request failed")

        return jsonify({
            "success": False,
            "reply": (
                "अभी AI से जवाब नहीं मिल पाया। "
                "Free Tier की सीमा, मॉडल की उपलब्धता या API सेटिंग जाँचें। "
                "कोई भुगतान चालू न करें।"
            )
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
