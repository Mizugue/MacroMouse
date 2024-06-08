import tkinter
import time
from tkinter import messagebox, Menu
import pyautogui
import threading

class Macromouse:
    def __init__(self):
        self.root = tkinter.Tk()
        self.setup_ui()


    def setup_ui(self):
        icon_path = 'icon.ico'
        self.BACKGROUND_COLOR = "#0000CD"
        self.FONT = ("Comic Sans MS", 20)

        self.root.title("MacroMouse")
        self.root.iconbitmap(icon_path)
        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        menubar = Menu(self.root)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)


        self.create_frame1()
        self.create_images_widgets()
        self.create_buttons()

        self.root.mainloop()

    def create_images(self):
        self.image1 = tkinter.PhotoImage(file="img1.png")
        self.image2 = tkinter.PhotoImage(file="img2.png")
        self.image3 = tkinter.PhotoImage(file="macro.png")

    def create_images_widgets(self):
        self.create_images()
        tkinter.Label(self.root, image=self.image3, bg=self.BACKGROUND_COLOR).place(rely=0, relx=0, relheight=0.25,
                                                                                relwidth=0.7)
        tkinter.Label(self.root, image=self.image2, bg=self.BACKGROUND_COLOR).place(rely=0, relx=0.7, relheight=0.2)
        tkinter.Label(self.frame1, image=self.image1).place(rely=0.54, relx=0)

    def create_frame1(self):
        self.frame1 = tkinter.Frame(self.root, bd=1, highlightbackground='#00BFFF', highlightthickness=5)
        self.frame1.place(relx=0, rely=0.26, relwidth=1, relheight=0.8)

        tkinter.Label(self.frame1, text="Keys for execution in proper order", font=self.FONT).place(rely=0.02,
                                                                                                    relx=0.25)
        tkinter.Label(self.frame1, text="\U0001F9C0" * 21, font=self.FONT).place(rely=0.24, relx=0)
        tkinter.Label(self.frame1, text="\U0001F9C0" * 21, font=self.FONT).place(rely=0.47, relx=0)
        tkinter.Label(self.frame1, text="Working time", font=self.FONT).place(rely=0.32, relx=0.38)
        tkinter.Label(self.frame1, text="Actions per second", font=self.FONT).place(rely=0.55, relx=0.35)
        tkinter.Label(self.frame1, text="🪤 By mzg 🐀", font=("Comic Sans MS", 15)).place(rely=0.8680, relx=0.75)


        self.entries = []
        self.create_entry()

        self.tempo = tkinter.Entry(self.frame1, font=("Arial", 15), justify='center', bg="lightgray")
        self.tempo.place(relx=0.45, rely=0.40, relwidth=0.1, relheight=0.05)

        self.speed = tkinter.Entry(self.frame1, font=("Arial", 15), justify='center', bg="lightgray")
        self.speed.place(relx=0.45, rely=0.63, relwidth=0.1, relheight=0.05)

    def create_entry(self):
        default_width = 0.07
        default_height = 0.05
        if len(self.entries) < 11:
            entry = tkinter.Entry(self.frame1, font=("Helvetica", 15), justify='center', bg="lightgray")
            if self.entries:
                last_entry = self.entries[-1]
                x_offset = last_entry.winfo_x() + last_entry.winfo_width() + 10
                entry.place(x=x_offset, rely=0.1, relwidth=default_width, relheight=default_height)
            else:
                entry.place(relx=0.02, rely=0.1, relwidth=default_width, relheight=default_height)
            self.entries.append(entry)
        else:
            messagebox.showwarning("Warning", "Maximum number of entries reached.")

    def create_buttons(self):
        tkinter.Button(self.frame1, background='green', text='Start', font=self.FONT, foreground='white', activeforeground="green",
                       command=self.check_macro).place(relx=0.4, rely=0.75, relheight=0.06, relwidth=0.2)

        tkinter.Button(self.frame1, text='+', font=self.FONT, command=self.add_entry, activeforeground="green").place(relx=0.46, rely=0.18, relheight=0.05, relwidth=0.075)


    def add_entry(self):
        self.create_entry()

    def check_macro(self):
        try:
            keys = [entry.get() for entry in self.entries if entry.get()]
            duration = float(self.tempo.get()) if self.tempo.get() else 1
            speed = float(self.speed.get()) if self.speed.get() else None
        except:
            messagebox.showerror("Error", "Speed and duration shall be integers")

        if not keys:
            messagebox.showerror("Error", "Fill in at least one key.")
            return

        if duration < 0:
            messagebox.showerror("Error", "The working time must be greater than or equal to zero.")
            return

        if duration == 0:
            messagebox.showwarning("Warning", "The macro will run indefinitely.")

        if speed == 0:
            messagebox.showerror("Error", "The speed shall be greater than 0.")
            return
        elif not speed:
            messagebox.showerror("Error", "The speed shall be inserted.")
            return

        self.root.destroy()
        pyautogui.PAUSE = 1 / speed

        def run_macro():
            if duration == 0:
                while True:
                    pyautogui.press(keys)
            else:
                start_time = time.time()
                end_time = start_time + duration
                while time.time() < end_time:
                    for action in keys:
                        if action.startswith("m:"):
                            mouse_action = action.split(":")[1]
                            if mouse_action == "r":
                                pyautogui.click(button="right")
                            elif mouse_action == "l":
                                pyautogui.click(button="left")
                        else:
                            pyautogui.press(action)
                        time.sleep(1 / speed)

        threading.Thread(target=run_macro).start()

    def show_help(self):
        help_window = tkinter.Toplevel(self.root)
        help_window.title("Help")
        help_window.iconbitmap('icon.ico')
        help_window.configure(bg="white")

        help_text = tkinter.Text(help_window, font=("Helvetica", 20))
        help_text.pack(expand=True, fill=tkinter.BOTH)

        keys = pyautogui.KEYBOARD_KEYS
        keys.append("m:r")
        keys.append("m:l")

        help_text.insert(tkinter.END, "\n" * 4)
        help_text.insert(tkinter.END, " ⌨ Keyboard <-> Mouse 🖱 \n".rjust(45))
        help_text.insert(tkinter.END, "\n" * 3)
        help_text.insert(tkinter.END, "Keys \n".rjust(47))

        for key in keys:
                help_text.insert(tkinter.END, f"{key.rjust(45)}\n")

        help_text.config(state=tkinter.DISABLED)

        help_window.update_idletasks()
        help_window.resizable(False, False)
        width = help_window.winfo_reqwidth()
        height = help_window.winfo_reqheight()
        x_offset = (help_window.winfo_screenwidth() - width) // 2
        y_offset = (help_window.winfo_screenheight() - height) // 2
        help_window.geometry(f"{width - 500}x{height - 200}+{x_offset}+{y_offset}")


if __name__ == "__main__":
    Macromouse()
