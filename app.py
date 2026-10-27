
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "app": "Ishwar AI",
        "message": "Ishwar AI is running!"
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

    # AI model connection will be added here.
    # No paid API or external service is activated.

    return jsonify({
        "success": True,
        "reply": (
            "आपका संदेश Ishwar AI तक पहुँच गया है। "
            "अभी असली AI मॉडल कनेक्ट नहीं है। "
            "मॉडल कनेक्ट होने के बाद यहाँ AI का जवाब आएगा।"
        )
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
