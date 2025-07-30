import tkinter as tk
from tkinter import filedialog, messagebox
from detection import CrowdDetector
import threading
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Crowd Detection Studio Light Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f4")

        self.detector = CrowdDetector(update_callback=self.update_ui)

        self.running = False
        self.crowd_limit = 0

        # === Control Panel ===
        control_frame = tk.Frame(self.root, bg="#ffffff", height=50)
        control_frame.pack(fill="x", pady=5)

        self.start_btn = tk.Button(control_frame, text="Start Detection", bg="#4CAF50", fg="white",
                                   command=self.start_detection)
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = tk.Button(control_frame, text="Stop Detection", bg="#F44336", fg="white",
                                  command=self.stop_detection)
        self.stop_btn.pack(side="left", padx=10)

        tk.Label(control_frame, text="Crowd Limit:", bg="#ffffff").pack(side="left", padx=10)
        self.limit_entry = tk.Entry(control_frame, width=5)
        self.limit_entry.pack(side="left", padx=5)

        self.video_btn = tk.Button(control_frame, text="Open Video", bg="#2196F3", fg="white",
                                   command=self.open_video)
        self.video_btn.pack(side="left", padx=10)

        # === Main Layout ===
        content_frame = tk.Frame(self.root, bg="#f4f4f4")
        content_frame.pack(expand=True, fill="both")

        # Video Feed
        self.video_label = tk.Label(content_frame, bg="black")
        self.video_label.grid(row=0, column=0, padx=5, pady=5)

        # Heatmap Feed
        self.heatmap_label = tk.Label(content_frame, bg="black")
        self.heatmap_label.grid(row=0, column=1, padx=5, pady=5)

        # Graph
        fig, self.ax = plt.subplots(figsize=(4, 3))
        self.ax.set_facecolor("#f4f4f4")
        self.ax.set_title("Crowd Count Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Count")
        self.crowd_data = []
        self.time_data = []
        self.graph_canvas = FigureCanvasTkAgg(fig, master=content_frame)
        self.graph_canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)

        # Logs
        self.log_text = tk.Text(content_frame, bg="#ffffff", fg="#000000", width=40, height=10)
        self.log_text.grid(row=1, column=1, padx=5, pady=5)

        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

    def start_detection(self):
        try:
            self.crowd_limit = int(self.limit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for crowd limit.")
            return

        self.running = True
        threading.Thread(target=self.detector.detect_webcam, args=(self.stop_flag,)).start()

    def stop_detection(self):
        self.running = False

    def stop_flag(self):
        return not self.running

    def open_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
        if path:
            self.running = True
            threading.Thread(target=self.detector.detect_video, args=(path, self.stop_flag)).start()

    def update_ui(self, frame, heatmap, count):
        # Check crowd limit
        if count > self.crowd_limit > 0:
            messagebox.showwarning("Crowd Alert", f"Crowd limit exceeded! Count: {count}")

        # Video
        if frame is not None:
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = ImageTk.PhotoImage(Image.fromarray(img_rgb))
            self.video_label.configure(image=img_pil)
            self.video_label.image = img_pil

        # Heatmap
        if heatmap is not None:
            heat_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
            heat_pil = ImageTk.PhotoImage(Image.fromarray(heat_rgb))
            self.heatmap_label.configure(image=heat_pil)
            self.heatmap_label.image = heat_pil

        # Graph
        self.crowd_data.append(count)
        self.time_data.append(len(self.crowd_data))
        self.ax.clear()
        self.ax.plot(self.time_data, self.crowd_data, color="blue")
        self.ax.set_title("Crowd Count Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Count")
        self.graph_canvas.draw()

        # Logs
        self.log_text.insert(tk.END, f"Crowd Count: {count}\n")
        self.log_text.see(tk.END)
