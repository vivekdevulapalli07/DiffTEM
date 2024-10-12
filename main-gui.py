import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from tkinterdnd2 import TkinterDnD, DND_FILES
import d_spacing as ds
import zone_axis_angle as za

class DSpacingCalculator:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("CIF File d-spacing Calculator")
        self.window.geometry("500x300")
        
        self.main_frame = ttk.Frame(self.window, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = ttk.Label(
            self.main_frame,
            text="Drag and drop or click to select a CIF file",
            font=("Helvetica", 14),
            wraplength=400
        )
        self.label.pack(pady=20)
        
        self.open_button = ttk.Button(
            self.main_frame,
            text="Select CIF File",
            command=self.open_file_dialog,
            style="Accent.TButton"
        )
        self.open_button.pack(pady=10)
        
        try:
            self.window.drop_target_register(DND_FILES)
            self.window.dnd_bind('<<Drop>>', self.on_drop)
        except tk.TclError:
            self.label.config(text="Drag and drop feature not supported on this platform")

    def open_file_dialog(self):
        ds.open_file_dialog()

    def on_drop(self, event):
        ds.on_drop(event)

class ZoneAxisCalculator:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Zone Axis Angle Calculator")
        self.window.geometry("400x500")
        
        self.main_frame = ttk.Frame(self.window, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.system_var = tk.StringVar(value="Cubic")
        self.system_label = ttk.Label(self.main_frame, text="Select Crystal System")
        self.system_label.pack(pady=10)
        self.system_cubic = ttk.Radiobutton(self.main_frame, text="Cubic", variable=self.system_var, value="Cubic")
        self.system_hexagonal = ttk.Radiobutton(self.main_frame, text="Hexagonal", variable=self.system_var, value="Hexagonal")
        self.system_cubic.pack()
        self.system_hexagonal.pack()

        self.zone1_label = ttk.Label(self.main_frame, text="Enter the first zone axis:")
        self.zone1_label.pack(pady=10)

        self.x1, self.x2, self.x3, self.x4 = [ttk.Entry(self.main_frame, width=5) for _ in range(4)]
        self.y1, self.y2, self.y3, self.y4 = [ttk.Entry(self.main_frame, width=5) for _ in range(4)]

        for entry in [self.x1, self.x2, self.x3, self.x4]:
            entry.pack(pady=5)

        self.zone2_label = ttk.Label(self.main_frame, text="Enter the second zone axis:")
        self.zone2_label.pack(pady=10)

        for entry in [self.y1, self.y2, self.y3, self.y4]:
            entry.pack(pady=5)

        self.result_label = ttk.Label(self.main_frame, text="Angle between zone axes: ", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.calculate_button = ttk.Button(
            self.main_frame,
            text="Calculate Angle",
            command=self.calculate_angle,
            style="Accent.TButton"
        )
        self.calculate_button.pack(pady=10)

    def calculate_angle(self):
        za.calculate_and_display_angle(
            self.system_var, 
            self.x1, self.x2, self.x3, self.x4, 
            self.y1, self.y2, self.y3, self.y4, 
            self.result_label
        )

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Crystallography Tools")
        self.master.geometry("400x300")

        self.style = ttkb.Style(theme="cosmo")

        self.main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.main_frame,
            text="Crystallography Tools",
            font=("Helvetica", 18, "bold"),
            wraplength=400
        )
        self.title_label.pack(pady=20)

        self.d_spacing_button = ttk.Button(
            self.main_frame,
            text="CIF File d-spacing Calculator",
            command=self.open_d_spacing_calculator,
            style="Accent.TButton"
        )
        self.d_spacing_button.pack(pady=10, fill=tk.X)

        self.zone_axis_button = ttk.Button(
            self.main_frame,
            text="Zone Axis Angle Calculator",
            command=self.open_zone_axis_calculator,
            style="Accent.TButton"
        )
        self.zone_axis_button.pack(pady=10, fill=tk.X)

    def open_d_spacing_calculator(self):
        DSpacingCalculator(self.master)

    def open_zone_axis_calculator(self):
        ZoneAxisCalculator(self.master)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MainApplication(root)
    root.mainloop()
