import tkinter as tk
from tkinter import messagebox
import api_utils as api                     


BG_ROOT="#000"; BG_INPUT="#1c1c1c"; FG_HINT="#888"
BTN_GRAY="#6e6e6e"; BTN_GRAY_HOVER="#4e4e4e"; BTN_TXT="#d0d0d0"

class LoginView(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg=BG_ROOT)
        self.on_success = on_success
        self.mode = tk.StringVar(value="login")
        self._build()

    
    def _build(self):
        tk.Label(self, text="Insta", fg="white", bg=BG_ROOT,
                 font=("Brush Script MT", 40, "bold")).pack(pady=(40, 30))

        self.email    = self._make_entry("Email or login")
        self.password = self._make_entry("Password", show="*")

        self.action_btn = self._make_btn("Log in", self.handle_auth)
        self.action_btn.pack(pady=(0, 15))

        switch = tk.Frame(self, bg="#0d0d0d", bd=1, relief="solid",
                          padx=20, pady=10); switch.pack()
        self.switch_btn = tk.Button(
            switch, text="Don't have an account? Register",
            font=("Arial",10,"bold"), fg="#0095f6", bg="#0d0d0d",
            relief="flat", cursor="hand2", activeforeground="#0095f6",
            command=self.switch_mode)
        self.switch_btn.pack()

    
    def _make_entry(self, ph, show=""):
        e = tk.Entry(self, width=30, font=("Arial", 12),
                     bg=BG_INPUT, fg=FG_HINT, insertbackground="white",
                     relief="flat", highlightthickness=1,
                     highlightbackground="#333", highlightcolor="#888")
        e.insert(0, ph)
        e.bind("<FocusIn>",
               lambda _e: self._clear_ph(e, ph, show))
        e.bind("<FocusOut>",
               lambda _e: self._restore_ph(e, ph))
        e.pack(pady=6, ipady=6); return e

    def _make_btn(self, txt, cmd):
        return tk.Button(self, text=txt, command=cmd,
                         cursor="hand2", width=24, font=("Arial",11,"bold"),
                         bg=BTN_GRAY, fg=BTN_TXT,
                         activebackground=BTN_GRAY_HOVER,
                         activeforeground=BTN_TXT, relief="flat")

    def _clear_ph(self, ent, ph, show):
        if ent.get()==ph:
            ent.delete(0, tk.END); ent.config(fg="white", show=show)
    def _restore_ph(self, ent, ph):
        if not ent.get():
            ent.insert(0, ph); ent.config(fg=FG_HINT, show="")

    
    def handle_auth(self):
        email = self.email.get().strip(); pwd = self.password.get().strip()
        if not email or not pwd:
            messagebox.showwarning("Empty", "Provide email & password"); return

        route = "/api/login" if self.mode.get()=="login" else "/api/register"
        resp  = api.api_post(route, json={"email":email, "password":pwd})

        if resp.status_code in (200,201):
            if self.mode.get()=="login":
                api.save_token(resp.json()["token"])  
                api.load_token()
                api.CURRENT_USER_EMAIL = resp.json()["email"]
                self.on_success()
            else:
                messagebox.showinfo("Done","Registered – now log in.")
                self.switch_mode()
        else:
            messagebox.showerror("Error", resp.json().get("error","Auth failed"))

    def switch_mode(self):
        if self.mode.get()=="login":
            self.mode.set("register")
            self.action_btn.config(text="Register")
            self.switch_btn.config(text="Already have an account? Log in")
        else:
            self.mode.set("login")
            self.action_btn.config(text="Log in")
            self.switch_btn.config(text="Don't have an account? Register")
