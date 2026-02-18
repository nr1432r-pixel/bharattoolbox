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
from flask import Flask, render_template, request, jsonify
import requests, cv2, os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfReader, PdfWriter
import os, uuid, asyncio, requests, json, random, subprocess, cv2
from datetime import datetime
import edge_tts
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfReader, PdfWriter
import os, uuid, json, random, subprocess, cv2, requests, asyncio
from datetime import datetime
import edge_tts
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfReader, PdfWriter
import os, uuid, json, random, subprocess, cv2, requests, asyncio
from datetime import datetime
import edge_tts

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os, json, uuid, subprocess, requests, cv2, asyncio
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfReader, PdfWriter
import edge_tts

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os, json, uuid, subprocess, requests, cv2, asyncio
from flask import Response
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session, Response

# ================= APP =================
app = Flask(__name__, static_folder="static")
app.secret_key = "bharat_chat_super_secret_key_2026"

# ================= DATABASE =================
CHAT_DB = "chat_db.json"
USERS_DB = "users_db.json"

for db in [CHAT_DB, USERS_DB]:
    if not os.path.exists(db):
        with open(db, "w") as f:
            json.dump([], f)

# ================= FOLDERS =================
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
AUDIO_FOLDER = os.path.join("static", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= CHAT PAGE =================
@app.route("/bharat-chat")
def bharat_chat():
    return render_template("bharat-chat.html")

# ================= AUTH =================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    mobile = data["mobile"]
    password = generate_password_hash(data["password"])

    users = json.load(open(USERS_DB))
    if any(u["mobile"] == mobile for u in users):
        return jsonify({"error": "Mobile already exists"}), 400

    users.append({"mobile": mobile, "password": password})
    json.dump(users, open(USERS_DB, "w"), indent=2)
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    mobile = data["mobile"]
    password = data["password"]

    users = json.load(open(USERS_DB))
    user = next((u for u in users if u["mobile"] == mobile), None)

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid login"}), 401

    session["user"] = mobile
    return jsonify({"success": True})

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"success": True})

# ================= CHAT =================
@app.route("/send-message", methods=["POST"])
def send_message():
    if "user" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    chat = json.load(open(CHAT_DB))

    msg = {
        "sender": session["user"],
        "receiver": data["receiver"],
        "message": data["message"],
        "time": datetime.now().strftime("%d %b %I:%M %p")
    }
    chat.append(msg)
    json.dump(chat, open(CHAT_DB, "w"), indent=2)
    return jsonify({"success": True})

@app.route("/get-messages/<uid>")
def get_messages(uid):
    if "user" not in session:
        return jsonify([])

    chat = json.load(open(CHAT_DB))
    return jsonify([
        m for m in chat
        if uid in (m["sender"], m["receiver"])
    ])

# YAHAN SE TUMHARA PEHLE WALA TOOL CODE AS-IT-IS RAHEGA
# (PDF, Voice, Insta, Translator, etc.)
# =========================================================

# ================= RUN =================
# ======================
# 🔹 Yahan se tumhara existing code SAME rahega
# 🔹 Kuch delete nahi kiya gaya
# ======================
# HOME
# =====================

# ======================
# TOOL PAGES
# ======================
# ======================
# 💖 VALENTINE TOOL
# ======================
@app.route("/student-daily-tool")
def student_daily_tool():
    return render_template("student-daily-tool.html")

@app.route("/railway-super-tool")
def railway_super_tool():
    return render_template("railway-super-tool.html")

@app.route("/money-calculator")
def money_calculator():
    return render_template("money-calculator.html")  

@app.route("/video-downloader")
def video_downloader():
    return render_template("video-downloader.html")

@app.route("/valentine")
def valentine():
    return render_template("valentine.html")
    
@app.route("/pan-aadhaar")
def pan_aadhaar():
    return render_template("pan-aadhaar.html")
    
@app.route("/age-calculator")
def age_calculator():
    return render_template("age-calculator.html")
    
@app.route("/name-meaning")
def name_meaning():
    return render_template("name-meaning.html")
# ======================  
    
@app.route("/astrology")
def astrology():
    return render_template("astrology.html")

@app.route("/birthday")
def birthday():
    return render_template("birthday.html")
    
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

# ---------------- RESULT HELPER ----------------
# ---------------- RESULT HELPER ----------------
@app.route("/result-helper")
def result_helper():
    return render_template("result-helper.html")
# ---------------- TOOL PAGES ----------------

from flask import Flask, render_template, request, jsonify
import requests

@app.route("/hinglish-ai", methods=["GET", "POST"])
def hinglish_ai():
    # ---------- GET = Page ----------
    if request.method == "GET":
        return render_template("hinglish-ai.html")

    # ---------- POST = AI ----------
    data = request.get_json(force=True)
    text = data.get("text","")

    url = "https://inputtools.google.com/request"
    payload = [{
        "text": text,
        "itc": "hi-t-i0-und",
        "num": 5
    }]

    try:
        r = requests.post(url, json=payload, timeout=10)
        res = r.json()
        if res[0] == "SUCCESS":
            return jsonify({"result": res[1][0][1][0]})
    except Exception as e:
        print("HINGLISH AI ERROR:", e)

    return jsonify({"result": text})

@app.route("/hashtag")
def hashtag_page():
    return render_template("hashtag.html")

@app.route("/petrol")
def petrol_page():
    return render_template("petrol.html")

@app.route("/qr")
def qr_page():
    return render_template("qr.html")

@app.route("/govt")
def govt_page():
    return render_template("govt.html")

# ======================
# SPEED TEST
# ======================
@app.route("/speed-test")
def speed_test():
    return render_template("speed-test.html")


# ======================
# IP CHECKER
# ======================
@app.route("/ip-checker")
def ip_checker():
    return render_template("ip-checker.html")
    
# ---------------- 1️⃣ HINGLISH → HINDI ----------------
@app.route("/hinglish-convert", methods=["POST"])
def hinglish_convert():
    text = request.json.get("text","")

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client":"gtx",
        "sl":"en",
        "tl":"hi",
        "dt":"t",
        "q":text
    }

    res = requests.get(url, params=params)
    hindi = "".join([i[0] for i in res.json()[0]])
    return jsonify({"result": hindi})


# ---------------- 2️⃣ HASHTAG GENERATOR ----------------
@app.route("/generate-hashtags", methods=["POST"])
def generate_hashtags():
    key = request.json.get("keyword","")
    tags = [
        f"#{key}", f"#{key}reels", f"#{key}viral",
        "#reelsindia", "#instagood", "#trending"
    ]
    return jsonify({"hashtags":" ".join(tags)})


# ---------------- 3️⃣ PETROL COST ----------------
@app.route("/petrol-calc", methods=["POST"])
def petrol_calc():
    d = float(request.json["distance"])
    m = float(request.json["mileage"])
    p = float(request.json["price"])

    cost = round((d/m)*p, 2)
    return jsonify({"cost": cost})


# ---------------- 4️⃣ QR SAFETY ----------------
@app.route("/qr-check", methods=["POST"])
def qr_check():
    file = request.files["file"]
    path = "temp.png"
    file.save(path)

    img = cv2.imread(path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        return jsonify({"safe":False, "msg":"Invalid QR"})

    safe = data.startswith("https://")
    return jsonify({"url":data, "safe":safe})


# ---------------- 5️⃣ GOVT FORM HELPER ----------------
@app.route("/govt-help", methods=["POST"])
def govt_help():
    form = request.json["form"]

    data = {
        "pan":[
            "Aadhaar must match PAN name",
            "Photo signature clear",
            "DOB same everywhere"
        ],
        "aadhaar":[
            "Mobile number linked",
            "Correct address proof",
            "Biometric required"
        ]
    }
    return jsonify({"steps": data.get(form, [])})

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

# ===============================
# 🌐 UNIVERSAL VIDEO DOWNLOADER
# ===============================
@app.route("/video-info", methods=["POST"])
def video_info():
    data = request.get_json(force=True)
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL"}), 400

    try:
        cmd = [
            "yt-dlp",
            "-J",
            url
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        info = json.loads(result.stdout)

        formats = []
        for f in info.get("formats", []):
            if f.get("ext") == "mp4" and f.get("height"):
                formats.append({
                    "id": f["format_id"],
                    "quality": f"{f['height']}p",
                    "size": round((f.get("filesize",0) or 0)/1048576,2)
                })

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        })

    except Exception as e:
        print("VIDEO INFO ERROR:", e)
        return jsonify({"error": "Failed"}), 500


@app.route("/video-download", methods=["POST"])
def video_download():
    data = request.get_json(force=True)
    url = data.get("url")
    fid = data.get("format")

    if not url or not fid:
        return jsonify({"error": "Missing data"}), 400

    out_name = f"{uuid.uuid4()}.mp4"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)

    try:
        subprocess.run([
            "yt-dlp",
            "-f", f"{fid}+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", out_path,
            url
        ], check=True)

        return send_file(
            out_path,
            as_attachment=True,
            download_name="video.mp4"
        )

    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        return jsonify({"error": "Download failed"}), 500
# ===============================
# ===============================
# ===============================
# ===============================
# ===============================
# ===============================
# ===============================
# ===============================
# ===============================
# 🎬 YOUTUBE → SMART SHORTS TOOL (DUAL MODE)
# ===============================

import subprocess
import uuid
import os
import threading
import json
import random
import shutil
from flask import request, jsonify, render_template, send_from_directory

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

SHORTS_PROGRESS = {}

HOOK_WORDS = ["🔥", "🚀", "💰", "⚡", "😱", "🎯"]
COMMON_TAGS = ["#shorts", "#viral", "#reels", "#trending"]

# Detect if Chrome exists (Local Ultra HD Mode)
ULTRA_MODE = shutil.which("chrome") is not None or shutil.which("google-chrome") is not None


# ===============================
# PAGE
# ===============================
@app.route("/youtube-to-shorts")
def youtube_to_shorts():
    return render_template("youtube-to-shorts.html")


# ===============================
# GENERATE SHORTS
# ===============================
@app.route("/generate-shorts", methods=["POST"])
def generate_shorts():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL"}), 400

    job_id = str(uuid.uuid4())

    SHORTS_PROGRESS[job_id] = {
        "status": "Starting...",
        "progress": 0,
        "files": [],
        "title": "",
        "hashtags": []
    }

    def process():

        try:
            video_id = str(uuid.uuid4())
            input_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
            output_folder = os.path.join(OUTPUT_FOLDER, video_id)
            os.makedirs(output_folder, exist_ok=True)

            # =====================
            # 1️⃣ GET METADATA
            # =====================
            SHORTS_PROGRESS[job_id]["status"] = "Fetching info..."

            meta = subprocess.run(["yt-dlp", "-J", url], stdout=subprocess.PIPE)
            info = json.loads(meta.stdout.decode())
            title = info.get("title", "Amazing Video")

            emoji = random.choice(HOOK_WORDS)
            short_title = emoji + " " + title[:60]

            words = title.lower().split()
            tags = []
            for w in words[:6]:
                clean = ''.join(c for c in w if c.isalnum())
                if len(clean) > 3:
                    tags.append("#" + clean)

            hashtags = list(set(tags + COMMON_TAGS))[:8]

            SHORTS_PROGRESS[job_id]["title"] = short_title
            SHORTS_PROGRESS[job_id]["hashtags"] = hashtags

            # =====================
            # 2️⃣ DOWNLOAD
            # =====================
            SHORTS_PROGRESS[job_id]["status"] = "Downloading..."

            try:
                if ULTRA_MODE:
                    # 🟢 ULTRA HD LOCAL MODE
                    subprocess.run([
                        "yt-dlp",
                        "--cookies-from-browser", "chrome",
                        "-f", "bestvideo+bestaudio/best",
                        "--merge-output-format", "mp4",
                        "-o", input_path,
                        url
                    ], check=True)
                else:
                    # 🟡 RENDER SAFE MODE (360p)
                    subprocess.run([
                        "yt-dlp",
                        "-f", "18",
                        "-o", input_path,
                        url
                    ], check=True)

            except:
                # Fallback 360p
                subprocess.run([
                    "yt-dlp",
                    "-f", "18",
                    "-o", input_path,
                    url
                ], check=True)

            SHORTS_PROGRESS[job_id]["progress"] = 25

            # =====================
            # 3️⃣ GET DURATION
            # =====================
            probe = subprocess.run([
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                input_path
            ], stdout=subprocess.PIPE)

            duration = float(probe.stdout.decode().strip())

            clip_length = 25 if duration <= 1500 else 240
            total = int(duration // clip_length)

            if clip_length == 25:
                total = min(total, 12)
            else:
                total = min(total, 6)

            if total == 0:
                total = 1

            # =====================
            # 4️⃣ CREATE SHORTS (HD OUTPUT)
            # =====================
            for i in range(total):

                SHORTS_PROGRESS[job_id]["status"] = f"Creating {i+1}/{total}"

                start = i * clip_length
                out_file = os.path.join(output_folder, f"short_{i+1}.mp4")

                subprocess.run([
                    "ffmpeg",
                    "-ss", str(start),
                    "-t", str(clip_length),
                    "-i", input_path,
                    "-vf",
                    "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    "-c:v", "libx264",
                    "-preset", "medium",
                    "-crf", "20",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-y",
                    out_file
                ], check=True)

                SHORTS_PROGRESS[job_id]["files"].append(
                    f"/outputs/{video_id}/short_{i+1}.mp4"
                )

                SHORTS_PROGRESS[job_id]["progress"] = int(
                    25 + ((i+1)/total)*75
                )

            SHORTS_PROGRESS[job_id]["status"] = "done"
            SHORTS_PROGRESS[job_id]["progress"] = 100

        except Exception as e:
            SHORTS_PROGRESS[job_id]["status"] = "error"
            SHORTS_PROGRESS[job_id]["progress"] = 0
            print("ERROR:", e)

    threading.Thread(target=process).start()

    return jsonify({"job_id": job_id})


# ===============================
# PROGRESS
# ===============================
@app.route("/shorts-progress/<job_id>")
def shorts_progress(job_id):
    return jsonify(SHORTS_PROGRESS.get(job_id, {
        "status": "unknown",
        "progress": 0,
        "files": [],
        "title": "",
        "hashtags": []
    }))


# ===============================
# SERVE FILES
# ===============================
@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory("outputs", filename)

# ======================
# SEO FILES
# ======================

@app.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\nAllow: /\n\nSitemap: https://bharttollbox.in/sitemap.xml",
        mimetype="text/plain"
    )

@app.route("/sitemap.xml")
def sitemap():
    return Response("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://bharttollbox.in/</loc>
    <priority>1.0</priority>
  </url>
</urlset>""", mimetype="application/xml")
    
# ======================
if __name__ == "__main__":
    app.run(debug=True)




