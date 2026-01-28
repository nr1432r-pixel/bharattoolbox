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
