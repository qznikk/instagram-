import tkinter as tk
import api_utils as api
from views.login_view import LoginView
from views.main_view  import MainView

class InstaDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InstaDesktop")
        self.geometry("720x600")
        api.load_token()
        self.show_main() if api.TOKEN else self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        LoginView(self, self.show_main).pack(fill="both", expand=True)

    def show_main(self):
        self.clear()
        MainView(self, self.show_login).pack(fill="both", expand=True)

if __name__ == "__main__":
    InstaDesktop().mainloop()
