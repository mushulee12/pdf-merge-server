from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/merge", methods=["GET", "POST"])
def merge_pdf():
    if request.method == "GET":
        return "Merge server is alive 🟢"  # UptimeRobot이 이 응답만 보고 깨어있게 유지함

    merger = PdfMerger()
    files = request.files.getlist("pdfs")

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        merger.append(path)

    output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)
