import tkinter as tk
import time
from VIEW.display import Display


class App(tk.Tk):
    def __init__(self, f_data, f_kill_event, f_timestep=0.02):
        super().__init__()
        self.geometry("800x800")
        self.kill_event = f_kill_event

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame = Display(self, f_data, f_kill_event, f_timestep=f_timestep)

        self.mainloop()

    def on_closing(self):
        self.kill_event.set()
        time.sleep(0.5)
        self.destroy()
