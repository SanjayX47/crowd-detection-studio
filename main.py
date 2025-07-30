import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from dashboard import Dashboard

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry("600x350+450+250")
        self.root.configure(bg="#121212")

        # === App Logo ===
        self.logo = Image.open("assets/splash_logo.png").resize((180, 180))
        self.logo_img = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg="#121212")
        self.logo_label.pack(pady=20)

        # === Tagline ===
        self.tagline = tk.Label(self.root, text="Crowd Detection Pro+", fg="white",
                                bg="#121212", font=("Segoe UI", 16, "bold"))
        self.tagline.pack()

        self.subtitle = tk.Label(self.root, text="Powered by YOLOv8", fg="#AAAAAA",
                                 bg="#121212", font=("Segoe UI", 10))
        self.subtitle.pack(pady=5)

        # === Progress Bar ===
        self.progress = ttk.Progressbar(self.root, mode='determinate', length=300)
        self.progress.pack(pady=20)

        self.fade_in_logo()
        self.fill_progress()

    def fade_in_logo(self):
        """Simulate a fade-in effect by adjusting window transparency"""
        for i in range(0, 100, 5):
            self.root.attributes("-alpha", i/100)
            self.root.update()
            time.sleep(0.02)
        self.root.attributes("-alpha", 1)

    def fill_progress(self):
        """Fill progress bar before launching dashboard"""
        for i in range(0, 101, 5):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.05)
        self.launch_main()

    def launch_main(self):
        self.root.destroy()
        main_app = tk.Tk()
        Dashboard(main_app)
        main_app.mainloop()

if __name__ == "__main__":
    splash = tk.Tk()
    SplashScreen(splash)
    splash.mainloop()
