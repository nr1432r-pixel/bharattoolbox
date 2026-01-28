from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from pdf2docx import Converter
from pypdf import PdfReader, PdfWriter
import os, uuid, requests, subprocess, asyncio
import edge_tts

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
# PDF TO WORD (OK)
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
# WORD TO PDF (FIXED ✅ Linux Safe)
# =========================================================
@app.route("/word-to-pdf", methods=["POST"])
def word_to_pdf():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    docx_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.docx")
    out_name = f"{uuid.uuid4()}.pdf"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)

    file.save(docx_path)

    try:
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", OUTPUT_FOLDER,
                docx_path
            ],
            check=True,
            timeout=60
        )
    except Exception as e:
        print("WORD → PDF ERROR:", e)
        return "Word to PDF failed", 500

    return send_file(out_path, as_attachment=True, download_name="converted.pdf")

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
# TRANSLATE
# =========================================================
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    text = data.get("text", "")
    target = data.get("target", "en")

    if not text:
        return jsonify({"translated": ""})

    try:
        r = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "auto",
                "tl": target,
                "dt": "t",
                "q": text
            },
            timeout=20
        )
        result = r.json()
        translated = "".join(i[0] for i in result[0])
        return jsonify({"translated": translated})

    except Exception:
        return jsonify({"translated": "Translation failed"})

# =========================================================
# VOICE
# =========================================================
@app.route("/voice", methods=["POST"])
def voice():
    data = request.get_json(force=True)
    text = data.get("text", "")
    lang = data.get("lang", "en")

    voices = {
        "en": "en-US-AriaNeural",
        "hi": "hi-IN-MadhurNeural"
    }

    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(AUDIO_FOLDER, filename)

    async def run():
        c = edge_tts.Communicate(text, voices.get(lang))
        await c.save(path)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    loop.close()

    return jsonify({"file": filename})

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

# =========================================================
# INSTAGRAM DOWNLOAD (PUBLIC ONLY)
# =========================================================
@app.route("/instagram-download", methods=["POST"])
def instagram_download():
    data = request.get_json(force=True)
    url = data.get("url")
    option = data.get("option")

    if not url:
        return jsonify({"error": "URL required"}), 400

    out_id = str(uuid.uuid4())

    try:
        if option == "video":
            out_file = os.path.join(OUTPUT_FOLDER, f"{out_id}.mp4")
            cmd = [
                "yt-dlp",
                "-f", "bv*+ba/b",
                "--merge-output-format", "mp4",
                "-o", out_file,
                url
            ]
        else:
            out_file = os.path.join(OUTPUT_FOLDER, f"{out_id}.mp3")
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "-o", out_file,
                url
            ]

        subprocess.run(cmd, check=True, timeout=120)
        return send_file(out_file, as_attachment=True)

    except Exception:
        return jsonify({
            "error": "Only PUBLIC Instagram reels supported. Private/login reels will not work."
        }), 400

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
