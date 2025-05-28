import tkinter as tk, os, requests
from tkinter import filedialog, messagebox
import api_utils as api

def open_upload_dialog(root, refresh_cb):
    if not api.TOKEN:
        messagebox.showerror("Session","Log in again."); return

    path = filedialog.askopenfilename(
        title="Choose image", filetypes=[("Images","*.jpg *.jpeg *.png")]
    )
    if not path: return

    win = tk.Toplevel(root); win.title("Add description"); win.bg="#f8f8f8"
    tk.Label(win,text="Description:",bg="#f8f8f8").pack(pady=5)
    entry = tk.Entry(win, width=40); entry.pack(pady=5)

    def send():
        with open(path,"rb") as f:
            resp = requests.post(f"{api.API_URL}/api/upload",
                files={"file":(os.path.basename(path),f)},
                data={"description":entry.get()},
                headers={"Authorization":f"Bearer {api.TOKEN}"})
        if resp.status_code==200:
            messagebox.showinfo("OK","Uploaded"); win.destroy(); refresh_cb()
        elif resp.status_code==401:
            api.clear_token()
            messagebox.showerror("Session","Token expired. Log in again.")
            win.destroy(); refresh_cb()
        else:
            messagebox.showerror("Err",resp.text)
    tk.Button(win,text="Upload",bg="#0095f6",fg="black",
              width=15,command=send).pack(pady=10)
