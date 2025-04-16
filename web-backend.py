from flask import Flask, request
from main import cut_mp3_and_generate_csv, create_anki_deck_csv
import os

app = Flask(__name__)

@app.route("/api/process", methods=["POST"])
def process():
    mp3 = request.files["mp3"]
    srt_pt = request.files["srt_pt"]
    srt_en = request.files["srt_en"]
    output_folder = request.form["output_folder"]
    # Save files temporarily, process, and return results
    try:
        mp3_path = os.path.join(output_folder, mp3.filename)
        srt_pt_path = os.path.join(output_folder, srt_pt.filename)
        srt_en_path = os.path.join(output_folder, srt_en.filename)
        mp3.save(mp3_path)
        srt_pt.save(srt_pt_path)
        srt_en.save(srt_en_path)
        csv_path_basic = os.path.join(output_folder, "COMERCIAL-MARGARINA-basic.csv")
        csv_path_anki = os.path.join(output_folder, "COMERCIAL-MARGARINA-anki.csv")
        cut_mp3_and_generate_csv(mp3_path, srt_pt_path, output_folder, csv_path_basic)
        create_anki_deck_csv(srt_pt_path, srt_en_path, output_folder, csv_path_anki)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
