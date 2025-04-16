import tkinter as tk
from tkinter import filedialog, messagebox
import os

class AudioSRTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio SRT Processor")
        self.root.geometry("600x300")

        # Labels and Entries
        tk.Label(root, text="MP3 File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.mp3_entry = tk.Entry(root, width=50)
        self.mp3_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_mp3).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Portuguese SRT:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.srt_pt_entry = tk.Entry(root, width=50)
        self.srt_pt_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_srt_pt).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="English SRT:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.srt_en_entry = tk.Entry(root, width=50)
        self.srt_en_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_srt_en).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(root, text="Output Folder:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=3, column=2, padx=5, pady=5)

        # Process Button
        tk.Button(root, text="Process", command=self.process_files).grid(row=4, column=1, pady=20)

        # Status Label
        self.status_label = tk.Label(root, text="Ready", wraplength=500)
        self.status_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def browse_mp3(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if path:
            self.mp3_entry.delete(0, tk.END)
            self.mp3_entry.insert(0, path)

    def browse_srt_pt(self):
        path = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
        if path:
            self.srt_pt_entry.delete(0, tk.END)
            self.srt_pt_entry.insert(0, path)

    def browse_srt_en(self):
        path = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
        if path:
            self.srt_en_entry.delete(0, tk.END)
            self.srt_en_entry.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def process_files(self):
        # Import main.py only when the button is pressed
        from main import cut_mp3_and_generate_csv, create_anki_deck_csv

        mp3_path = self.mp3_entry.get()
        srt_path_PT = self.srt_pt_entry.get()
        srt_path_EN = self.srt_en_entry.get()
        output_folder = self.output_entry.get()

        if not all([mp3_path, srt_path_PT, srt_path_EN, output_folder]):
            self.status_label.config(text="Error: All fields must be filled!")
            return

        try:
            csv_path_basic = os.path.join(output_folder, 'COMERCIAL-MARGARINA-basic.csv')
            csv_path_anki = os.path.join(output_folder, 'COMERCIAL-MARGARINA-anki.csv')

            self.status_label.config(text="Processing audio and basic CSV...")
            self.root.update()  # Update GUI to show status
            cut_mp3_and_generate_csv(mp3_path, srt_path_PT, output_folder, csv_path_basic)

            self.status_label.config(text="Creating Anki deck CSV...")
            self.root.update()
            create_anki_deck_csv(srt_path_PT, srt_path_EN, output_folder, csv_path_anki)

            self.status_label.config(text="Processing complete! Check output folder.")
            messagebox.showinfo("Success", "Files processed successfully!")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to process files: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSRTApp(root)
    root.mainloop()
