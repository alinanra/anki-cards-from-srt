from moviepy.editor import AudioFileClip
import re
import csv

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

def srt_time_to_seconds(time_str):
    h, m, s, ms = map(int, re.split('[:,]', time_str))
    return h * 3600 + m * 60 + s + ms / 1000.0

def cut_mp3_and_generate_csv(mp3_path, srt_path_BN, output_folder, csv_path):
    subtitles = parse_srt(srt_path_BN)
    audio_clip = AudioFileClip(mp3_path)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Start Time', 'End Time', 'Bengali']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, ((start, end), text) in enumerate(subtitles.items()):
            start_sec = srt_time_to_seconds(start)
            end_sec = srt_time_to_seconds(end)
            audio_subclip = audio_clip.subclip(start_sec, end_sec)
            audio_subclip.write_audiofile(f"{output_folder}/clip_{i+1}.mp3")

            writer.writerow({'Start Time': start, 'End Time': end, 'Bengali': text})

# Example usage
mp3_path = r'filename'
srt_path_BN = r'filename'
output_folder = r'filename'
csv_path = r'filename'

cut_mp3_and_generate_csv(mp3_path, srt_path_BN, output_folder, csv_path)
