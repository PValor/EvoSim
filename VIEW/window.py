import tkinter as tk
from VIEW.display import Display


class App(tk.Tk):
    def __init__(self, f_data, f_kill_event, f_timestep=0.02):
        super().__init__()
        self.geometry("800x800")
        self.kill_event = f_kill_event

        self.frame = Display(self,
                             f_ref_data=f_data,
                             f_kill_event=self.kill_event,
                             f_timestep=f_timestep)
