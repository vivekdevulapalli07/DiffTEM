import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import ttkbootstrap as ttkb
from ase.io import read
import numpy as np

# Function to calculate d-spacing for cubic system
def cubic_d_spacing(a, h, k, l):
    return a / np.sqrt(h**2 + k**2 + l**2)

# Function to calculate d-spacing for hexagonal system
def hexagonal_d_spacing(a, c, h, k, l):
    return a / np.sqrt((4/3) * (h**2 + h*k + k**2) + (c/a)**2 * l**2)

# Function to calculate d-spacings and generate the table
def calculate_d_spacings(crystal_system, a, c=None):
    cubic_close_packed_planes = [(1, 1, 1), (2, 0, 0), (2, 2, 0), (3, 1, 1), (2, 2, 2)]
    hexagonal_close_packed_planes = [(1, 0, -1, 1), (1, 0, -1, 0), (1, 1, -2, 0), (1, 1, -2, 1)]
    d_spacings_table = []
    
    if crystal_system == 'cubic':
        for h, k, l in cubic_close_packed_planes:
            d = cubic_d_spacing(a, h, k, l)
            inverse_d = 10 / (d)  # Convert to nm⁻¹
            d_spacings_table.append([f"({h}, {k}, {l})", f"{d:.4f}", f"{inverse_d:.4f}"])
    
    elif crystal_system == 'hexagonal':
        if c is None:
            raise ValueError("For hexagonal system, 'c' parameter is required.")
        for h, k, i, l in hexagonal_close_packed_planes:
            d = hexagonal_d_spacing(a, c, h, k, l)
            inverse_d = 10 / (d)  # Convert to nm⁻¹
            d_spacings_table.append([f"({h}, {k}, {i}, {l})", f"{d:.4f}", f"{inverse_d:.4f}"])
    
    return d_spacings_table

# Function to display the table in a new window
def display_table(d_spacings_table, crystal_system):
    # Define headers
    headers = ["Plane (hkl)" if crystal_system == 'cubic' else "Plane (hkil)", "d-spacing (Å)", "Inverse d-spacing (nm⁻¹)"]
    
    # Create a new window for the table
    table_window = tk.Toplevel()
    table_window.title("d-spacing Table")
    
    # Protocol to handle closing the table window without affecting main window
    table_window.protocol("WM_DELETE_WINDOW", table_window.destroy)

    # Create a frame for the table and scrollbar
    frame = ttk.Frame(table_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a treeview widget
    tree = ttk.Treeview(frame, columns=headers, show="headings", height=10)
    
    # Define the column properties
    for col in headers:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    # Insert data into the treeview
    for row in d_spacings_table:
        tree.insert("", "end", values=row)
    
    # Add a vertical scrollbar to the treeview
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    
    # Pack the treeview and scrollbar
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)


# Function to process the CIF file
def process_cif(filepath):
    try:
        # Read CIF file using ASE
        structure = read(filepath)
        lattice = structure.get_cell_lengths_and_angles()
        
        # Extract lattice parameters
        a = lattice[0]
        b = lattice[1]
        c = lattice[2]
        
        # Check for crystal system based on lattice parameters
        if a == b == c:
            crystal_system = 'cubic'
        elif a == b and a != c:
            crystal_system = 'hexagonal'
        else:
            raise ValueError("Only cubic and hexagonal systems are supported.")
        
        # Calculate and display the table
        if crystal_system == 'hexagonal':
            d_spacings = calculate_d_spacings(crystal_system, a, c)
        else:
            d_spacings = calculate_d_spacings(crystal_system, a)
        
        display_table(d_spacings, crystal_system)
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process CIF file: {e}")

# Function to open file dialog and select CIF file
def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("CIF files", "*.cif")])
    if file_path:
        process_cif(file_path)

# Function to handle drag and drop
def on_drop(event):
    file_path = event.data
    if file_path.startswith('{') and file_path.endswith('}'):
        file_path = file_path[1:-1]  # Remove curly braces on Windows paths
    process_cif(file_path)

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
    command=open_file_dialog,
    style="Accent.TButton"
)
open_button.pack(pady=10)

# Enable drag-and-drop (requires tkdnd)
try:
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
except tk.TclError as e:
    label.config(text="Drag and drop feature not supported on this platform")

def disable_closing_root():
    pass  # Just override with a no-op

#root.protocol("WM_DELETE_WINDOW", disable_closing_root)

# Main event loop
root.mainloop()
