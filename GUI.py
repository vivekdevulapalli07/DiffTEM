# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 03:44:33 2024

@author: devi
"""
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import ttkbootstrap as ttkb
import d_spacing as ds

# GUI setup

# GUI setup using TkinterDnD2 for drag-and-drop support
root = TkinterDnD.Tk()  # Change to TkinterDnD.Tk()
root.title("CIF File d-spacing Calculator")
root.geometry("500x300")

# Apply ttkbootstrap theming if necessary
style = ttkb.Style(theme="cosmo")

# Create a main frame
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Instruction Label
label = ttk.Label(
    main_frame,
    text="Drag and drop or click to select a CIF file",
    font=("Helvetica", 14),
    wraplength=400
)
label.pack(pady=20)

# Button to open file dialog
open_button = ttk.Button(
    main_frame,
    text="Select CIF File",
    command=ds.open_file_dialog,
    style="Accent.TButton"
)
open_button.pack(pady=10)

# Enable drag-and-drop (requires tkdnd)
try:
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', ds.on_drop)
except tk.TclError as e:
    label.config(text="Drag and drop feature not supported on this platform")

def disable_closing_root():
    pass  # Just override with a no-op

#root.protocol("WM_DELETE_WINDOW", disable_closing_root)

# Main event loop
root.mainloop()
