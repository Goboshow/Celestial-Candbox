import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os

print("Current folder:", os.getcwd())
print("Title exists:", os.path.exists("Sprites/TitleBG.png"))
print("Button exists:", os.path.exists("Sprites/StartButton.png"))

pygame.mixer.init()
pygame.mixer.music.load("Song/LSO.mp3")
pygame.mixer.music.play(-1)

class CelestialCandbox:
    def __init__(self, root):
        self.root = root

        self.root.title("Celestial Candbox")
        self.root.geometry("1280x720")
        self.root.minsize(640, 360)

        self.original_bg = Image.open("Sprites/TitleBG.png")
        self.original_button = Image.open("Sprites/StartButton.png")

        self.bg_label = tk.Label(root)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_photo = None
        self.button_photo = None

        self.start_button = tk.Button(
            root,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_game
        )

        self.start_button.place(anchor="center")

        self.update_graphics()

        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        self.update_graphics()

    def update_graphics(self):
        width = max(self.root.winfo_width(), 1)
        height = max(self.root.winfo_height(), 1)

        bg = self.original_bg.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        self.bg_photo = ImageTk.PhotoImage(bg)
        self.bg_label.config(image=self.bg_photo)

        button_width = max(150, width // 6)

        aspect_ratio = (
            self.original_button.height /
            self.original_button.width
        )

        button_height = int(button_width * aspect_ratio)

        resized_button = self.original_button.resize(
            (button_width, button_height),
            Image.Resampling.LANCZOS
        )

        self.button_photo = ImageTk.PhotoImage(resized_button)

        self.start_button.config(image=self.button_photo)

        x = width * 0.75
        y = height * 0.75

        self.start_button.place(
            x=x,
            y=y,
            anchor="center"
        )

    def start_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Song/lil jingle.mp3")
        pygame.mixer.music.play(-1)

        self.start_button.destroy()
        self.bg_label.destroy()

        red_screen = tk.Frame(
            self.root,
            bg="red"
        )

        red_screen.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = CelestialCandbox(root)
    root.mainloop
