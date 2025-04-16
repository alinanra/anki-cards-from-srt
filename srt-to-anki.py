from moviepy.editor import AudioFileClip
import re
import csv

# === Parse SRT to Dict for Audio Cutting ===
def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    subtitles = {}
    for match in pattern.finditer(content):
        start_time = match.group(1)
        end_time = match.group(2)
        text = match.group(3).replace('\n', ' ')
        subtitles[(start_time, end_time)] = text

    return subtitles

# === Parse SRT to Ordered List for Anki Deck ===
def parse_srt_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n', re.DOTALL)
    return [match.group(1).replace('\n', ' ') for match in pattern.finditer(content)]

# === Time Conversion Helper ===
def srt_time_to_seconds(time_str):
    h, m, s, ms = map(int, re.split('[:,]', time_str))
    return h * 3600 + m * 60 + s + ms / 1000.0

# === Step 1: Cut MP3 and Save Basic CSV ===
def cut_mp3_and_generate_csv(mp3_path, srt_path, output_folder, csv_path):
    subtitles = parse_srt(srt_path)
    audio_clip = AudioFileClip(mp3_path)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Start Time', 'End Time', 'Portuguese']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, ((start, end), text) in enumerate(subtitles.items()):
            start_sec = srt_time_to_seconds(start)
            end_sec = srt_time_to_seconds(end)

            duration = end_sec - start_sec
            if duration <= 0:
                print(f"Skipping clip {i+1}: end time is not after start time ({start} -> {end})")
                continue
            if duration < 0.2:
                print(f"Skipping clip {i+1}: too short ({duration:.3f} seconds)")
                continue

            try:
                audio_subclip = audio_clip.subclip(start_sec, end_sec)
                audio_subclip.write_audiofile(f"{output_folder}/COMERCIAL-MARGARINA_{i+1}.mp3")
                writer.writerow({'Start Time': start, 'End Time': end, 'Portuguese': text})
            except Exception as e:
                print(f"Error processing clip {i+1} ({start}–{end}): {e}")

# === Step 2: Create Anki CSV from Portuguese and English SRTs ===
def create_anki_deck_csv(srt_path_PT, srt_path_EN, output_folder, csv_path_anki):
    portuguese_lines = parse_srt_to_list(srt_path_PT)
    english_lines = parse_srt_to_list(srt_path_EN)

    # Pad the shorter list with blank strings to match length
    max_len = max(len(portuguese_lines), len(english_lines))
    while len(portuguese_lines) < max_len:
        portuguese_lines.append("")
    while len(english_lines) < max_len:
        english_lines.append("")

    with open(csv_path_anki, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Portuguese', 'Audio', 'English']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, (pt_text, en_text) in enumerate(zip(portuguese_lines, english_lines)):
            audio_clip_name = f"COMERCIAL-MARGARINA{i+1}.mp3"
            writer.writerow({
                'Portuguese': pt_text,
                'Audio': f"[sound:{audio_clip_name}]",
                'English': en_text
            })

# Example usage
mp3_path = r'filename'
srt_path_BN = r'filename'
output_folder = r'filename'
csv_path = r'filename'

csv_path_basic = rf'{output_folder}\COMERCIAL-MARGARINA-basic.csv'
csv_path_anki = rf'{output_folder}\COMERCIAL-MARGARINA-anki.csv'

# Step 1: Cut audio and create basic subtitle CSV
cut_mp3_and_generate_csv(mp3_path, srt_path_PT, output_folder, csv_path_basic)

# Step 2: Create Anki deck CSV using both SRT files
create_anki_deck_csv(srt_path_PT, srt_path_EN, output_folder, csv_path_anki)
