import tkinter as tk
from tkinter import ttk
import api_utils as api
from .profile_view import ProfileFeed
from .upload_view  import open_upload_dialog

class MainView(ttk.Notebook):
    def __init__(self, master, on_logout):
        super().__init__(master)
        self.on_logout = on_logout
        self._build_tabs()

    def _build_tabs(self):
        profile_tab = ttk.Frame(self); upload_tab = ttk.Frame(self)
        self.add(profile_tab, text="👤 Profile")
        self.add(upload_tab, text="📤 Upload")

        self.feed = ProfileFeed(profile_tab)
        self.feed.pack(fill="both", expand=True)

        tk.Label(upload_tab, text="Pick a photo & add a description").pack(pady=10)
        tk.Button(upload_tab, text="🖼️ Upload", width=20,
                  bg="#0095f6", fg="black", relief="flat",
                  command=lambda: open_upload_dialog(self, self.feed.load_posts)
        ).pack(pady=5)

        tk.Button(upload_tab, text="🚪 Logout", width=20,
                  bg="#ff4d4d", fg="black", relief="flat",
                  command=self.logout).pack(pady=10)

    def logout(self):
        api.clear_token()
        self.on_logout()
