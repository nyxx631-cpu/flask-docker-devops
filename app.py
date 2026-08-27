from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "DevOps Pipeline: Flask + Docker",
        "version": "1.0.0"
    })

@app.route("/health")
def health():
    return jsonify({"health": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
