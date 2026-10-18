import random
from flask import Flask, request, render_template_string, render_template
flag:str = "RSI{c0o1_1npu7_7a3f89b1c0d4e2f5a6b8c}";
app = Flask(__name__)
app.config["FLAG"] = "RSI{C00L_1NPU7_7a3f89b1c0d4e2f5a6b8c}"
STYLES = [
    {"name": "Neon Pink", "css": "color:#ff2bd6;text-shadow:0 0 8px #ff2bd6;"},
    {"name": "Cyber Blue", "css": "color:#00e5ff;text-shadow:0 0 8px #00e5ff;"},
    {"name": "Matrix Green", "css": "color:#39ff14;text-shadow:0 0 6px #39ff14;"},
    {"name": "Glitch Red", "css": "color:#ff0033;animation:glitch 1s infinite;"},
    {"name": "Gold Glow", "css": "color:#ffd700;text-shadow:0 0 10px #ffae00;"},
    {"name": "Violet Pulse", "css": "color:#b388ff;animation:pulse 1.5s ease-in-out infinite;"},
]
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/style", methods=["POST"])
def style():
    user_text = request.form.get("text", "")
    chosen = random.choice(STYLES)
    template_src = f"""
    <div class="result-box" style="{chosen['css']}">
      {user_text}
    </div>
    <p class="style-label">Style rolled: <strong>{chosen['name']}</strong></p>
    """
    render = render_template_string(template_src)

    return render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
