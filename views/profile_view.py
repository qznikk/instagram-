# views/profile_view.py
import tkinter as tk, io
from PIL import Image, ImageTk
import api_utils as api
from datetime import datetime

THUMB_SIZE = 180
COLS       = 3
GAP        = 4

class ProfileFeed(tk.Frame):
    """Siatka jak na profilu Instagrama z opisami i datami."""
    def __init__(self, master):
        super().__init__(master, bg="#000")
        self.thumbs = []
        self.load_posts()

    def load_posts(self):
        for w in self.winfo_children():
            w.destroy()

        tk.Label(self, text=f"Logged in: {api.CURRENT_USER_EMAIL}",
                 fg="white", bg="#000", font=("Arial", 10, "bold")
                 ).pack(anchor="w", pady=10)

        resp = api.api_get("/api/images", auth=True)
        if resp.status_code != 200 or not resp.json():
            tk.Label(self, text="No photos yet.",
                     fg="white", bg="#000").pack(pady=20)
            return

        grid = tk.Frame(self, bg="#000")
        grid.pack()
        row = col = 0

        for img in resp.json():
            data = api.api_get(f"/uploads/{img['filename']}")
            if data.status_code == 200:
                pil = Image.open(io.BytesIO(data.content))

                w, h = pil.size
                side = min(w, h)
                left = (w - side) // 2
                top = (h - side) // 2
                pil = pil.crop((left, top, left + side, top + side))
                pil = pil.resize((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)

                tk_img = ImageTk.PhotoImage(pil)
                self.thumbs.append(tk_img)

                container = tk.Frame(grid, bg="#000")
                container.grid(row=row, column=col, padx=GAP, pady=GAP)

                lbl = tk.Label(container, image=tk_img, bg="#000", bd=0)
                lbl.pack()

                desc = img.get("description", "No description")
                uploaded_at = img.get("uploaded_at", "")
                try:
                    parsed_date = datetime.strptime(uploaded_at, "%Y-%m-%d %H:%M").strftime("%d %b %Y %H:%M")
                except Exception:
                    parsed_date = "Unknown date"

                tk.Label(container, text=desc, fg="white", bg="#000",
                         font=("Arial", 9)).pack(pady=(2, 0))
                tk.Label(container, text=parsed_date, fg="#666", bg="#000",
                         font=("Arial", 8)).pack()

                col += 1
                if col == COLS:
                    col = 0
                    row += 1
