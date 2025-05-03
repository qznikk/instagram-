import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
from PIL import Image, ImageTk
import io

API_URL = "http://127.0.0.1:3000"
TOKEN_FILE = "token.txt"
TOKEN = None
CURRENT_USER_EMAIL = None
thumbnail_refs = []

def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)

def load_token():
    global TOKEN
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            TOKEN = f.read().strip()

def logout():
    global TOKEN, CURRENT_USER_EMAIL
    TOKEN = None
    CURRENT_USER_EMAIL = None
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    messagebox.showinfo("Wylogowano", "Zostałeś wylogowany.")
    show_login_screen()

def handle_auth():
    global CURRENT_USER_EMAIL
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    if not email or not password:
        messagebox.showwarning("Błąd", "Podaj email i hasło.")
        return

    payload = {"email": email, "password": password}
    route = "/api/login" if mode.get() == "login" else "/api/register"
    response = requests.post(f"{API_URL}{route}", json=payload)

    if response.status_code in [200, 201]:
        if mode.get() == "login":
            token = response.json()["token"]
            CURRENT_USER_EMAIL = response.json()["email"]
            save_token(token)
            load_token()
            show_main_screen()
        else:
            messagebox.showinfo("Sukces", "Rejestracja zakończona. Możesz się zalogować.")
            switch_mode()
    else:
        error = response.json().get("error", "Błąd logowania/rejestracji.")
        messagebox.showerror("Błąd", error)

def upload_file_with_description():
    file_path = filedialog.askopenfilename(
        title="Wybierz zdjęcie",
        filetypes=[("Obrazy", "*.jpg *.jpeg *.png")]
    )
    if not file_path:
        return

    desc_window = tk.Toplevel(root)
    desc_window.title("Dodaj opis")
    tk.Label(desc_window, text="Opis zdjęcia:").pack(pady=5)
    desc_entry = tk.Entry(desc_window, width=50)
    desc_entry.pack(pady=5)

    def submit():
        description = desc_entry.get()
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {'Authorization': f"Bearer {TOKEN}"}
                data = {'description': description}
                r = requests.post(f"{API_URL}/api/upload", files=files, data=data, headers=headers)
                if r.status_code == 200:
                    messagebox.showinfo("Sukces", "Plik został wysłany.")
                    desc_window.destroy()
                    load_profile_posts()
                else:
                    messagebox.showerror("Błąd", f"Błąd: {r.status_code} - {r.text}")
        except Exception as e:
            messagebox.showerror("Wyjątek", str(e))

    tk.Button(desc_window, text="Wyślij", command=submit).pack(pady=10)

def show_full_image_window(img_data):
    try:
        response = requests.get(f"{API_URL}/uploads/{img_data['filename']}")
        if response.status_code == 200:
            window = tk.Toplevel(root)
            window.title("Zdjęcie")

            pil_img = Image.open(io.BytesIO(response.content))
            max_size = (800, 600)
            pil_img.thumbnail(max_size)
            tk_img = ImageTk.PhotoImage(pil_img)

            label_img = tk.Label(window, image=tk_img)
            label_img.image = tk_img
            label_img.pack(pady=10)

            tk.Label(window, text=f"📝 {img_data['description']}", fg="gray").pack()
            tk.Label(window, text=f"📅 {img_data['uploaded_at']}", fg="blue").pack(pady=5)
        else:
            messagebox.showerror("Błąd", "Nie udało się załadować zdjęcia.")
    except Exception as e:
        messagebox.showerror("Wyjątek", str(e))

def load_profile_posts():
    for widget in profile_frame.winfo_children():
        widget.destroy()

    email_label = tk.Label(profile_frame, text=f"Zalogowany jako: {CURRENT_USER_EMAIL}", font=("Arial", 10, "bold"))
    email_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    headers = {'Authorization': f"Bearer {TOKEN}"}
    r = requests.get(f"{API_URL}/api/images", headers=headers)
    if r.status_code == 200:
        images = r.json()
        if not images:
            tk.Label(profile_frame, text="Brak zdjęć do wyświetlenia.").grid(row=1, column=0, columnspan=3, pady=10)
            return

        row, col = 1, 0
        for img in images:
            try:
                img_response = requests.get(f"{API_URL}/uploads/{img['filename']}")
                if img_response.status_code == 200:
                    pil_img = Image.open(io.BytesIO(img_response.content))
                    pil_img.thumbnail((150, 150))
                    tk_img = ImageTk.PhotoImage(pil_img)

                    frame = tk.Frame(profile_frame, bd=1, relief=tk.RAISED)
                    frame.grid(row=row, column=col, padx=10, pady=10)
                    img_label = tk.Label(frame, image=tk_img, cursor="hand2")
                    img_label.pack()
                    img_label.bind("<Button-1>", lambda e, data=img: show_full_image_window(data))

                    def on_enter(event, f=frame): f.config(relief=tk.SOLID, bd=2)
                    def on_leave(event, f=frame): f.config(relief=tk.RAISED, bd=1)
                    img_label.bind("<Enter>", on_enter)
                    img_label.bind("<Leave>", on_leave)

                    thumbnail_refs.append(tk_img)

                    col += 1
                    if col == 3:
                        col = 0
                        row += 1
            except Exception as e:
                tk.Label(profile_frame, text="❌ Błąd ładowania miniatury.").grid(row=row, column=col, padx=10, pady=10)
    else:
        tk.Label(profile_frame, text="Błąd podczas pobierania zdjęć.").grid(row=1, column=0, columnspan=3)

def show_login_screen():
    clear_window()
    global email_entry, password_entry, action_button, switch_button

    tk.Label(root, text="Email:").pack(pady=(20, 0))
    email_entry = tk.Entry(root, width=30)
    email_entry.pack()

    tk.Label(root, text="Hasło:").pack(pady=(10, 0))
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack()

    action_button = tk.Button(root, text="Zaloguj się", width=25, command=handle_auth)
    action_button.pack(pady=15)

    switch_button = tk.Button(root, text="Nie masz konta? Zarejestruj się", command=switch_mode)
    switch_button.pack()

def show_main_screen():
    clear_window()

    notebook = ttk.Notebook(root)
    upload_tab = ttk.Frame(notebook)
    profile_tab = ttk.Frame(notebook)
    notebook.add(upload_tab, text="📤 Upload")
    notebook.add(profile_tab, text="👤 Profil")
    notebook.pack(expand=True, fill='both')

    tk.Label(upload_tab, text="Wybierz zdjęcie i dodaj opis").pack(pady=10)
    tk.Button(upload_tab, text="🖼️ Wybierz i wyślij", command=upload_file_with_description).pack(pady=5)
    tk.Button(upload_tab, text="🚪 Wyloguj", command=logout).pack(pady=10)

    global profile_frame
    profile_frame = tk.Frame(profile_tab)
    profile_frame.pack(fill='both', expand=True, pady=10)
    load_profile_posts()

def switch_mode():
    if mode.get() == "login":
        mode.set("register")
        action_button.config(text="Zarejestruj się")
        switch_button.config(text="Masz już konto? Zaloguj się")
    else:
        mode.set("login")
        action_button.config(text="Zaloguj się")
        switch_button.config(text="Nie masz konta? Zarejestruj się")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# === START ===
root = tk.Tk()
root.title("InstaDesktop")
root.geometry("720x600")

mode = tk.StringVar(value="login")
load_token()

if TOKEN:
    show_main_screen()
else:
    show_login_screen()

root.mainloop()
