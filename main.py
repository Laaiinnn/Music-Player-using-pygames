import tkinter as tk
from tkinter import filedialog
import pygame
from os.path import basename

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x350")

        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False

        self.create_widgets()

        # Initialize pygame mixer
        pygame.mixer.init()

    def create_widgets(self):
        self.btn_add = tk.Button(self.root, text="Add Song", command=self.add_song)
        self.btn_add.grid(row=0, column=0, pady=5)

        self.btn_play_pause = tk.Button(self.root, text="Play", command=self.play_pause_music)
        self.btn_play_pause.grid(row=0, column=1, pady=5, padx=5)

        self.btn_stop = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.btn_stop.grid(row=0, column=2, pady=5, padx=5)

        self.btn_next = tk.Button(self.root, text="Next", command=self.next_track)
        self.btn_next.grid(row=0, column=3, pady=5, padx=5)

        self.btn_sort = tk.Button(self.root, text="Sort Playlist", command=self.sort_playlist)
        self.btn_sort.grid(row=0, column=4, pady=5, padx=5)

        self.lbl_playlist = tk.Label(self.root, text="Playlist:")
        self.lbl_playlist.grid(row=1, column=0, columnspan=5, pady=5)

        self.lst_playlist = tk.Listbox(self.root, width=50)
        self.lst_playlist.grid(row=2, column=0, columnspan=5, pady=5)

        self.scale_volume = tk.Scale(self.root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.scale_volume.set(0.5)
        self.scale_volume.grid(row=3, column=0, columnspan=5, pady=5)

        self.lbl_song_duration = tk.Label(self.root, text="Song Duration: 00:00 / 00:00")
        self.lbl_song_duration.grid(row=4, column=0, columnspan=5, pady=5)

        self.progress_bar = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=500, command=self.seek_track)
        self.progress_bar.grid(row=5, column=0, columnspan=5, pady=5)

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)
            self.lst_playlist.insert(tk.END, basename(file_path))

    def play_pause_music(self):
        if self.playlist:
            if self.is_playing:
                pygame.mixer.music.pause()
                self.is_playing = False
                self.btn_play_pause.config(text="Play")
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                else:
                    self.play_current_track()
                self.is_playing = True
                self.btn_play_pause.config(text="Pause")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.btn_play_pause.config(text="Play")

    def next_track(self):
        if self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            self.play_current_track()

    def play_current_track(self):
        pygame.mixer.music.load(self.playlist[self.current_track_index])
        pygame.mixer.music.play()
        self.update_song_info()
        self.update_progress_bar()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_song_info(self):
        audio = pygame.mixer.Sound(self.playlist[self.current_track_index])
        duration = audio.get_length()
        self.lbl_song_duration.config(text=f"Song Duration: 00:00 / {self.format_duration(duration)}")
        audio.stop()

    def update_progress_bar(self):
        audio = pygame.mixer.Sound(self.playlist[self.current_track_index])
        duration = audio.get_length()
        current_position = pygame.mixer.music.get_pos() / 1000
        progress = min(current_position / duration * 100, 100)
        self.progress_bar.set(progress)
        audio.stop()
        if self.is_playing:
            self.root.after(1000, self.update_progress_bar)

    def format_duration(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def sort_playlist(self):
        n = len(self.playlist)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if basename(self.playlist[j]) > basename(self.playlist[j + 1]):
                    self.playlist[j], self.playlist[j + 1] = self.playlist[j + 1], self.playlist[j]
                    self.lst_playlist.delete(j)
                    self.lst_playlist.insert(j, basename(self.playlist[j]))
                    self.lst_playlist.delete(j + 1)
                    self.lst_playlist.insert(j + 1, basename(self.playlist[j + 1]))

    def seek_track(self, value):
        if self.playlist:
            audio = pygame.mixer.Sound(self.playlist[self.current_track_index])
            duration = audio.get_length()
            target_position = float(value) / 100 * duration
            pygame.mixer.music.set_pos(target_position / 1000)
            audio.stop()

# Create the Tkinter application window
root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
