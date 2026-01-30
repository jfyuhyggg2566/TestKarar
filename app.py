from flask import Flask, request, jsonify, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"py", "zip"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Telegram Bot Hosting</title>
<style>
body {
    background: linear-gradient(135deg, #0a0f1f, #05070d);
    font-family: Arial, sans-serif;
    color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.container {
    background: #0e1629;
    padding: 30px;
    width: 420px;
    border-radius: 14px;
    box-shadow: 0 0 25px rgba(0, 132, 255, 0.5);
    text-align: center;
}
h1 {
    color: #1e90ff;
    margin-bottom: 20px;
}
input[type=file] {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    background: #02040a;
    color: #fff;
    border: 1px solid #1e90ff;
    border-radius: 6px;
}
button {
    width: 100%;
    padding: 10px;
    background: #1e90ff;
    border: none;
    color: #fff;
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
}
button:hover {
    background: #0b63c7;
}
pre {
    margin-top: 15px;
    background: #02040a;
    padding: 10px;
    border-radius: 6px;
    text-align: left;
    font-size: 13px;
    max-height: 160px;
    overflow: auto;
}
</style>
</head>
<body>

<div class="container">
    <h1>Telegram Bot Hosting</h1>

    <form id="uploadForm">
        <input type="file" id="file" name="file" required>
        <button type="submit">Upload</button>
    </form>

    <pre id="responseBox"></pre>
</div>

<script>
document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    document.getElementById("responseBox").textContent =
        JSON.stringify(data, null, 2);
});
</script>

</body>
</html>
"""

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file sent"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected"})

    if not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File type not allowed"})

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    return jsonify({
        "status": "success",
        "message": "File uploaded successfully",
        "filename": filename,
        "saved_path": path
    })

if __name__ == "__main__":
    app.run(debug=True)