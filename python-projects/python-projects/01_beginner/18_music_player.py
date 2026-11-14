"""
18 - Music Player
=================
A desktop music player: open a folder, pick a song, play / pause / stop,
skip tracks and change the volume. Plays MP3, WAV and OGG files.

Needs the pygame library (for the sound). Install it once:
    pip install pygame

Concepts you'll practise:
  - Combining two libraries: tkinter (the window) + pygame (the audio)
  - filedialog.askdirectory() to let the user pick a folder
  - Listbox, Scale (slider), Frame and Button widgets
  - The % (modulo) operator to wrap around: after the last song comes the first
  - Polling with root.after(): checking every second if the song has ended
  - Cleaning up when the window closes (WM_DELETE_WINDOW)

Run:  python 18_music_player.py

Challenges:
  1. Add a Shuffle button.
  2. Show how long the current song has been playing (pygame.mixer.music.get_pos()).
  3. Remember the last folder you opened (save it to a JSON file).
"""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

try:
    import pygame
except ImportError:
    print("This project needs pygame. Install it with:")
    print("    pip install pygame")
    raise SystemExit(1)

SUPPORTED = {".mp3", ".wav", ".ogg"}


class MusicPlayer:
    def __init__(self, root):
        pygame.mixer.init()
        self.root = root
        self.playlist = []         # list of Path objects
        self.current = None        # index of the current song
        self.paused = False
        self.stopped = True

        root.title("Music Player")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.close)

        tk.Button(root, text="Open Folder...", command=self.open_folder).pack(
            fill="x", padx=10, pady=(10, 5))

        self.listbox = tk.Listbox(root, width=55, height=12, activestyle="none")
        self.listbox.pack(padx=10, pady=5)
        self.listbox.bind("<Double-Button-1>", lambda event: self.play_selected())

        controls = tk.Frame(root)
        controls.pack(pady=5)
        for text, command in [("Prev", self.previous_song), ("Play", self.play_selected),
                              ("Pause", self.toggle_pause), ("Stop", self.stop),
                              ("Next", self.next_song)]:
            tk.Button(controls, text=text, width=7, command=command).pack(side="left", padx=2)

        self.volume = tk.Scale(root, from_=0, to=100, orient="horizontal",
                               label="Volume", command=self.set_volume)
        self.volume.set(70)
        self.volume.pack(fill="x", padx=10)

        self.status = tk.Label(root, text="Open a folder to begin.", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(5, 10))

        self.check_if_song_ended()

    # ---------- loading songs ----------
    def open_folder(self):
        folder = filedialog.askdirectory(title="Choose a folder with music")
        if not folder:
            return                                  # user pressed Cancel
        self.stop()
        self.playlist = sorted(p for p in Path(folder).iterdir()
                               if p.suffix.lower() in SUPPORTED)
        self.listbox.delete(0, tk.END)
        for song in self.playlist:
            self.listbox.insert(tk.END, song.stem)
        self.current = None
        self.status.config(text=f"{len(self.playlist)} song(s) found.")

    # ---------- playback ----------
    def play(self, index):
        self.current = index
        song = self.playlist[index]
        try:
            pygame.mixer.music.load(str(song))
            pygame.mixer.music.play()
        except pygame.error as error:
            messagebox.showerror("Can't play this file", f"{song.name}\n\n{error}")
            return
        self.paused = False
        self.stopped = False
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.see(index)
        self.status.config(text=f"Playing: {song.stem}")

    def play_selected(self):
        if not self.playlist:
            return
        selection = self.listbox.curselection()
        index = selection[0] if selection else (self.current or 0)
        self.play(index)

    def toggle_pause(self):
        if self.current is None or self.stopped:
            return
        if self.paused:
            pygame.mixer.music.unpause()
            self.status.config(text=f"Playing: {self.playlist[self.current].stem}")
        else:
            pygame.mixer.music.pause()
            self.status.config(text="Paused")
        self.paused = not self.paused

    def stop(self):
        pygame.mixer.music.stop()
        self.stopped = True
        self.paused = False
        self.status.config(text="Stopped")

    def next_song(self):
        if self.playlist:
            index = 0 if self.current is None else (self.current + 1) % len(self.playlist)
            self.play(index)

    def previous_song(self):
        if self.playlist:
            index = 0 if self.current is None else (self.current - 1) % len(self.playlist)
            self.play(index)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(int(value) / 100)   # pygame wants 0.0 to 1.0

    # ---------- housekeeping ----------
    def check_if_song_ended(self):
        """Every second: if a song finished on its own, play the next one."""
        if not self.stopped and not self.paused and not pygame.mixer.music.get_busy():
            self.next_song()
        self.root.after(1000, self.check_if_song_ended)

    def close(self):
        pygame.mixer.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    MusicPlayer(root)
    root.mainloop()
