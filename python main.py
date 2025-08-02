import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os
from datetime import datetime

# Simple, elegant color scheme
BG = "#FFFFFF"           # White background
ACCENT = "#4F46E5"       # Indigo for highlights
BTN_BG = "#E0E7FF"       # Light indigo for button backgrounds
TXT_FONT = ("Helvetica", 14)
HEADER_FONT = ("Helvetica", 28, "bold")
SUBHEADER_FONT = ("Helvetica", 22)
LINK_FONT = ("Helvetica", 12, "underline")

# Utility I/O
def load_users():
    if os.path.exists("users.json"):
        return json.load(open("users.json"))
    return {}

def save_users(u):
    json.dump(u, open("users.json", "w"))

def load_tasks(u):
    fn = f"{u}_tasks.json"
    if os.path.exists(fn):
        return json.load(open(fn))
    return []

def save_tasks(u, t):
    json.dump(t, open(f"{u}_tasks.json", "w"))

current_user = None

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("414x896")
        self.configure(bg=BG)
        self.users = load_users()
        self.frames = {}
        for F in (WelcomePage, LoginPage, SignUpPage, MenuPage,
                  CreateTaskPage, ViewTaskPage, UpdateTaskPage, DeleteTaskPage):
            frm = F(self)
            self.frames[F] = frm
            frm.place(relwidth=1, relheight=1)
        self.show(WelcomePage)

    def show(self, page):
        self.frames[page].tkraise()
        if hasattr(self.frames[page], 'refresh'):
            self.frames[page].refresh()

class CreateTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Create Task", font=HEADER_FONT, bg=BG, fg=ACCENT).pack(pady=20)
        self.title_entry = tk.Entry(self, font=TXT_FONT)
        self.title_entry.pack(pady=10, ipadx=20, ipady=5)
        self.title_entry.insert(0, "Title")
        self.desc_entry = tk.Entry(self, font=TXT_FONT)
        self.desc_entry.pack(pady=10, ipadx=20, ipady=5)
        self.desc_entry.insert(0, "Description")
        self.due_entry = tk.Entry(self, font=TXT_FONT)
        self.due_entry.pack(pady=10, ipadx=20, ipady=5)
        self.due_entry.insert(0, "Due Date (YYYY-MM-DD)")
        tk.Button(self, text="Save Task", font=TXT_FONT, bg=ACCENT, fg="white", relief="flat",
                  command=self.save_task).pack(pady=20)
        tk.Button(self, text="Back", font=TXT_FONT, bg="white", fg=ACCENT, relief="solid",
                  command=lambda: master.show(MenuPage)).pack(pady=10)

    def save_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due = self.due_entry.get()
        tasks = load_tasks(current_user)
        tasks.append({"title": title, "desc": desc, "due": due, "status": "Pending"})
        save_tasks(current_user, tasks)
        messagebox.showinfo("Success", "Task created!")
        self.master.show(MenuPage)

class ViewTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Your Tasks", font=HEADER_FONT, bg=BG, fg=ACCENT).pack(pady=20)
        self.listbox = tk.Listbox(self, font=TXT_FONT, width=40)
        self.listbox.pack(pady=10)
        tk.Button(self, text="Back", font=TXT_FONT, bg="white", fg=ACCENT, relief="solid",
                  command=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        tasks = load_tasks(current_user)
        for i, t in enumerate(tasks):
            self.listbox.insert(tk.END, f"{i+1}. {t['title']} - {t['status']}")

class UpdateTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Update Task", font=HEADER_FONT, bg=BG, fg=ACCENT).pack(pady=20)
        self.listbox = tk.Listbox(self, font=TXT_FONT, width=40)
        self.listbox.pack(pady=10)
        tk.Button(self, text="Edit Selected", font=TXT_FONT, bg=ACCENT, fg="white", relief="flat",
                  command=self.edit_task).pack(pady=10)
        tk.Button(self, text="Back", font=TXT_FONT, bg="white", fg=ACCENT, relief="solid",
                  command=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.tasks = load_tasks(current_user)
        for i, t in enumerate(self.tasks):
            self.listbox.insert(tk.END, f"{i+1}. {t['title']} - {t['desc']}")

    def edit_task(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        t = self.tasks[i]
        new_title = simpledialog.askstring("Edit Title", "New title:", initialvalue=t['title'])
        new_desc = simpledialog.askstring("Edit Description", "New description:", initialvalue=t['desc'])
        new_due = simpledialog.askstring("Edit Due Date", "New due date:", initialvalue=t['due'])
        self.tasks[i] = {"title": new_title, "desc": new_desc, "due": new_due, "status": t['status']}
        save_tasks(current_user, self.tasks)
        self.refresh()

class DeleteTaskPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Delete Task", font=HEADER_FONT, bg=BG, fg=ACCENT).pack(pady=20)
        self.listbox = tk.Listbox(self, font=TXT_FONT, width=40)
        self.listbox.pack(pady=10)
        tk.Button(self, text="Delete Selected", font=TXT_FONT, bg="red", fg="white", relief="flat",
                  command=self.delete_task).pack(pady=10)
        tk.Button(self, text="Back", font=TXT_FONT, bg="white", fg=ACCENT, relief="solid",
                  command=lambda: master.show(MenuPage)).pack(pady=10)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.tasks = load_tasks(current_user)
        for i, t in enumerate(self.tasks):
            self.listbox.insert(tk.END, f"{i+1}. {t['title']}")

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        del self.tasks[i]
        save_tasks(current_user, self.tasks)
        self.refresh()

class WelcomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="📝", font=("Helvetica", 48), bg=BG).pack(pady=(100, 10))
        tk.Label(self, text="Let’s Get", font=SUBHEADER_FONT, bg=BG, fg=ACCENT).pack()
        tk.Label(self, text="Started!", font=HEADER_FONT, fg=ACCENT, bg=BG).pack(pady=(0, 40))
        tk.Button(self, text="SIGN IN", font=TXT_FONT, bg=BTN_BG, relief="flat", width=20,
                  command=lambda: master.show(LoginPage)).pack(pady=10)
        tk.Label(self, text="OR SIGN IN WITH", bg=BG, font=TXT_FONT).pack(pady=5)
        tk.Button(self, text="G", font=("Helvetica", 24, "bold"), width=4, relief="flat").pack(pady=5)
        tk.Label(self, text="DIDN’T HAVE ACCOUNT?", bg=BG, font=TXT_FONT).pack(pady=(80, 0))
        tk.Button(self, text="SIGN UP NOW", font=TXT_FONT, bg=BG, fg=ACCENT, relief="flat",
                  command=lambda: master.show(SignUpPage)).pack()

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Welcome", font=SUBHEADER_FONT, bg=BG, fg=ACCENT).pack(pady=(100, 0))
        tk.Label(self, text="Back!", font=HEADER_FONT, fg=ACCENT, bg=BG).pack(pady=(0, 30))
        self.email = tk.Entry(self, font=TXT_FONT)
        self.email.pack(pady=5, ipady=5, ipadx=20)
        self.email.insert(0, "Email Address")
        self.password = tk.Entry(self, show="*", font=TXT_FONT)
        self.password.pack(pady=5, ipady=5, ipadx=20)
        self.password.insert(0, "Password")
        self.remember = tk.IntVar()
        tk.Checkbutton(self, text="Remember for 30 days", variable=self.remember, bg=BG, font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self, text="LOG IN", font=TXT_FONT, bg=ACCENT, fg="white", width=20, relief="flat",
                  command=self.login).pack(pady=10)
        tk.Label(self, text="Forgot Password?", font=LINK_FONT, fg="#3B82F6", bg=BG).pack()
        tk.Label(self, text="Don’t have an account?", bg=BG, font=TXT_FONT).pack(pady=(60, 0))
        tk.Button(self, text="Sign up", font=TXT_FONT, fg=ACCENT, bg=BG, relief="flat",
                  command=lambda: master.show(SignUpPage)).pack()

    def login(self):
        global current_user
        u = self.email.get()
        p = self.password.get()
        if u in self.master.users and self.master.users[u] == p:
            current_user = u
            self.master.show(MenuPage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

class SignUpPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Create an", font=SUBHEADER_FONT, bg=BG, fg=ACCENT).pack(pady=(100, 0))
        tk.Label(self, text="Account!", font=HEADER_FONT, fg=ACCENT, bg=BG).pack(pady=(0, 30))
        self.username = tk.Entry(self, font=TXT_FONT)
        self.username.pack(pady=5, ipady=5, ipadx=20)
        self.username.insert(0, "Username")
        self.email = tk.Entry(self, font=TXT_FONT)
        self.email.pack(pady=5, ipady=5, ipadx=20)
        self.email.insert(0, "Email Address")
        self.password = tk.Entry(self, show="*", font=TXT_FONT)
        self.password.pack(pady=5, ipady=5, ipadx=20)
        self.password.insert(0, "Password")
        self.confirm = tk.Entry(self, show="*", font=TXT_FONT)
        self.confirm.pack(pady=5, ipady=5, ipadx=20)
        self.confirm.insert(0, "Confirm Password")
        tk.Button(self, text="CREATE ACCOUNT", font=TXT_FONT, bg=ACCENT, fg="white", width=20, relief="flat",
                  command=self.register).pack(pady=20)
        tk.Button(self, text="Already have an account? Sign in", font=LINK_FONT, fg=ACCENT, bg=BG, relief="flat",
                  command=lambda: master.show(LoginPage)).pack()

    def register(self):
        u = self.username.get()
        p = self.password.get()
        cp = self.confirm.get()
        if p != cp:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if u in self.master.users:
            messagebox.showerror("Error", "User exists")
        else:
            self.master.users[u] = p
            save_users(self.master.users)
            messagebox.showinfo("Success", "Created")
            self.master.show(LoginPage)

class MenuPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        btns = [("Create Task ➕", CreateTaskPage),
                ("Update Task 🔄", UpdateTaskPage),
                ("Delete Task 🗑️", DeleteTaskPage),
                ("View Task 👁️", ViewTaskPage)]
        tk.Label(self, text="Menu", font=HEADER_FONT, bg=BG, fg=ACCENT).pack(pady=40)
        for (txt, pg) in btns:
            tk.Button(self, text=txt, font=TXT_FONT, bg=BTN_BG, width=25, relief="flat",
                      command=lambda p=pg: master.show(p)).pack(pady=10)
        tk.Button(self, text="Logout", font=TXT_FONT, bg="white", fg=ACCENT, relief="solid",
                  command=lambda: master.show(WelcomePage)).pack(pady=30)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
