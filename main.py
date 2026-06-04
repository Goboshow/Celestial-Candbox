import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pygame
import os

print("Current folder:", os.getcwd())
print("Title exists:", os.path.exists("Sprites/TitleBG.png"))
print("Button exists:", os.path.exists("Sprites/StartButton.png"))

pygame.mixer.init()
pygame.mixer.music.load("Song/LSO.mp3")
pygame.mixer.music.play(-1)

class Planet:
    def __init__(self, x, y, vx, vy, mass, sprite):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.sprite = sprite
        self.id = None

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

        self.root.after(50, self.update_menu)
        self.root.bind("<Configure>", self.on_resize)

        self.drag_start = None

        self.root.bind("<Button-1>", self.mouse_down)
        self.root.bind("<ButtonRelease-1>", self.mouse_up)

    def mouse_down(self, event):
        if not hasattr(self, "canvas"):
            return
        self.drag_start = (event.x, event.y)

    def mouse_up(self, event):
        if not hasattr(self, "canvas") or self.drag_start is None:
            return
        
        x0, y0 = self.drag_start
        x1, y1 = event.x, event.y

        vx = (x1 - x0) * 0.05
        vy = (y1 - y0) * 0.05

        self.spawn_planet(x0, y0, vx, vy)

        self.drag_start = None

    def on_resize(self, event=None):
        if hasattr(self, "canvas"):
            return
        else:
            self.update_menu

    def update_menu(self):
        width = max(self.root.winfo_width(), 1)
        height = max(self.root.winfo_height(), 1)

        bg = self.original_bg.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(bg)
        self.bg_label.config(image=self.bg_img)

        bw = max(150, width // 6)
        aspect = self.original_button.height / self.original_button.width
        bh = int(bw * aspect)

        btn = self.original_button.resize((bw, bh), Image.Resampling.LANCZOS)
        self.btn_img = ImageTk.PhotoImage(btn)
        self.start_button.config(image=self.btn_img)

        self.start_button.place(x=width * 0.75, y=height * 0.75, anchor="center")

    def start_game(self):
        pygame.mixer.music.load("Song/lil jingle.mp3")
        pygame.mixer.music.play(-1)

        self.start_button.destroy()
        self.bg_label.destroy()

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        print(self.canvas)

        self.objects = []
        self.running = True

        self.update_simulation()

    def spawn_planet(self, x, y, vx, vy):
        img = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.ellipse(
            (0, 0, 240, 240),
            fill=(180, 200, 255, 255)
        )

        img = img.resize((60, 60), Image.Resampling.LANCZOS)

        planet_img = ImageTk.PhotoImage(img)

        if not hasattr(self, "planet_images"):
            self.planet_images = []
        self.planet_images.append(planet_img)

        p = Planet(x, y, vx, vy, 10, planet_img)

        p.sprite = planet_img

        p.id = self.canvas.create_image(p.x, p.y, image=p.sprite)
        self.objects.append(p)

        print("Spawn:", x, y, vx, vy)

    def update_simulation(self):
        if not self.running:
            return
        
        for obj in self.objects:
            obj.x += obj.vx
            obj.y += obj.vy

            self.canvas.coords(obj.id, obj.x, obj.y)

        self.root.after(16, self.update_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    game = CelestialCandbox(root)
    root.mainloop()
