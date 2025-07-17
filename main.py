from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/merge": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/merge", methods=["GET", "POST"])
def merge_pdf():
    if request.method == "GET":
        return "Merge server is alive 🟢"  # UptimeRobot 상태 체크용

    try:
        merger = PdfMerger()
        files = request.files.getlist("pdfs")

        if not files:
            print("❌ No files received!")
            return "No files received", 400

        for file in files:
            print(f"📁 Received file: {file.filename}")
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            merger.append(path)

        output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
        merger.write(output_path)
        merger.close()

        print("✅ PDF merge completed.")
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"🔥 Error during merging: {str(e)}")
        return f"Error: {str(e)}", 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)
