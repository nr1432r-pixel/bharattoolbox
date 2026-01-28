from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfReader, PdfWriter
import os, uuid, asyncio, requests
import edge_tts
import requests
import asyncio
import edge_tts
import subprocess

app = Flask(__name__, static_folder="static")

# ======================
# FOLDERS
# ======================
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
AUDIO_FOLDER = os.path.join("static", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return render_template("home.html")

# ======================
# TOOL PAGES
# ======================
@app.route("/PDF Tools")
def PDF_Tools():
    return render_template("PDF Tools.html")

@app.route("/Image Tools")
def image_tools():
    return render_template("Image Tools.html")

@app.route("/Advanced Scientific Calculator")
def calculator():
    return render_template("Advanced Scientific Calculator.html")

@app.route("/instagram-video-downloader")
def instagram_video_downloader():
    return render_template("instagram-video-downloader.html")

@app.route("/Password Generator")
def password_generator():
    return render_template("Password Generator.html")

@app.route("/QR Code Generator")
def qr_code_generator():
    return render_template("QR Code Generator.html")

@app.route("/Text Tools")
def text_tools():
    return render_template("Text Tools.html")

@app.route("/Translator + Voice")
def translator_voice():
    return render_template("Translator + Voice.html")

@app.route("/Unit Converter")
def unit_converter():
    return render_template("Unit Converter.html")

# =========================================================
# PDF TO WORD
# =========================================================
@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    docx_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.docx")

    file.save(pdf_path)
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    return send_file(docx_path, as_attachment=True, download_name="converted.docx")

# =========================================================
# WORD TO PDF
# =========================================================
@app.route("/word-to-pdf", methods=["POST"])
def word_to_pdf():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    docx_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.docx")
    pdf_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.pdf")

    file.save(docx_path)
    convert(docx_path, pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name="converted.pdf")

# =========================================================
# MERGE PDF
# =========================================================
@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():
    files = request.files.getlist("files")
    if len(files) < 2:
        return "Select at least 2 PDFs", 400

    writer = PdfWriter()
    output_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.pdf")

    for f in files:
        temp_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
        f.save(temp_path)
        reader = PdfReader(temp_path)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as out:
        writer.write(out)

    return send_file(output_path, as_attachment=True, download_name="merged.pdf")

# =========================================================
# COMPRESS PDF (basic safe)
# =========================================================
@app.route("/compress-pdf", methods=["POST"])
def compress_pdf():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    in_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    out_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}_compressed.pdf")

    file.save(in_path)
    reader = PdfReader(in_path)
    writer = PdfWriter()

    for p in reader.pages:
        writer.add_page(p)

    with open(out_path, "wb") as f:
        writer.write(f)

    return send_file(out_path, as_attachment=True, download_name="compressed.pdf")

# =========================================================
# REAL TRANSLATION
# =========================================================

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)

    text = data.get("text", "").strip()
    target = data.get("target", "en")

    if not text:
        return jsonify({"translated": ""})

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target,
        "dt": "t",
        "q": text
    }

    try:
        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        result = res.json()

        translated_text = ""
        for part in result[0]:
            translated_text += part[0]

        return jsonify({"translated": translated_text})

    except Exception as e:
        print("TRANSLATE ERROR:", e)
        return jsonify({"translated": "Translation failed"})
# =========================================================
# REAL VOICE (MP3)
# =========================================================
import asyncio
import edge_tts

@app.route("/voice", methods=["POST"])
def voice():
    data = request.get_json(force=True)

    text = data.get("text", "").strip()
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    voices = {
        "en": "en-US-AriaNeural",
        "hi": "hi-IN-MadhurNeural",
        "ta": "ta-IN-PallaviNeural",
        "or": "or-IN-SrutiNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "es": "es-ES-ElviraNeural",
        "ar": "ar-SA-ZariyahNeural",
        "ru": "ru-RU-SvetlanaNeural",
        "ja": "ja-JP-NanamiNeural"
    }

    voice_name = voices.get(lang, "en-US-AriaNeural")

    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(AUDIO_FOLDER, filename)

    async def generate():
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(path)

    # ✅ SAFE LOOP (THIS FIXES EVERYTHING)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate())
    loop.close()

    # safety check
    if not os.path.exists(path) or os.path.getsize(path) < 5000:
        return jsonify({"error": "Voice generation failed"}), 500

    return jsonify({"file": filename})

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)
# =========================================================
# INSTAGRAM DOWNLOAD

@app.route("/instagram-download", methods=["POST"])
def instagram_download():
    data = request.get_json(force=True)
    url = data.get("url")
    option = data.get("option")  # video / audio

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    out_id = str(uuid.uuid4())
    out_dir = OUTPUT_FOLDER
    os.makedirs(out_dir, exist_ok=True)

    try:
        if option == "video":
            out_file = os.path.join(out_dir, f"{out_id}.mp4")
            cmd = [
                "yt-dlp",
                "-f", "mp4",
                "-o", out_file,
                url
            ]

        elif option == "audio":
            out_file = os.path.join(out_dir, f"{out_id}.mp3")
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "-o", out_file,
                url
            ]
        else:
            return jsonify({"error": "Invalid option"}), 400

        subprocess.run(cmd, check=True)

        return send_file(
            out_file,
            as_attachment=True,
            download_name=os.path.basename(out_file)
        )

    except Exception as e:
        print("INSTAGRAM DOWNLOAD ERROR:", e)
        return jsonify({"error": "Download failed"}), 500


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
