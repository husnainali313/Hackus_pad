import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import os
import sys

# Define our themes (all dark themes with different accent colors)
THEMES = {
    "Hacker (Default)": {
        "bg": "black",
        "fg": "#00FF00",  # Bright Green
        "select_bg": "#004400",
        "menu_bg": "black",
        "menu_fg": "#00FF00",
        "status_bg": "black",
        "status_fg": "#00FF00"
    },
    "Solarized Dark": {
        "bg": "#002b36",  # Dark blue-black
        "fg": "#839496",  # Grayish white
        "select_bg": "#073642",
        "menu_bg": "#002b36",
        "menu_fg": "#839496",
        "status_bg": "#002b36",
        "status_fg": "#839496"
    },
    "Deep Blue": {
        "bg": "#0a0a2a",  # Very dark blue
        "fg": "#4f9aff",  # Bright blue
        "select_bg": "#1a1a4a",
        "menu_bg": "#0a0a2a",
        "menu_fg": "#4f9aff",
        "status_bg": "#0a0a2a",
        "status_fg": "#4f9aff"
    },
    "Cyber Purple": {
        "bg": "#0a001a",  # Very dark purple
        "fg": "#bf00ff",  # Electric purple
        "select_bg": "#1a004a",
        "menu_bg": "#0a001a",
        "menu_fg": "#bf00ff",
        "status_bg": "#0a001a",
        "status_fg": "#bf00ff"
    },
    "Blood Moon": {
        "bg": "#1a0000",  # Very dark red
        "fg": "#ff3333",  # Bright red
        "select_bg": "#4d0000",
        "menu_bg": "#1a0000",
        "menu_fg": "#ff3333",
        "status_bg": "#1a0000",
        "status_fg": "#ff3333"
    }
}

def new_file():
    """Clears the text area for a new file."""
    if text_area.compare("end-1c", "==", "1.0"):
        return
    if text_area.edit_modified():
        if messagebox.askyesno("Hackus Pad", "Save current file?"):
            save_file()
    text_area.delete(1.0, tk.END)
    root.title("Hackus Pad - Untitled")
    text_area.edit_modified(False)

def open_file(filepath=None):
    """Opens a file and loads its content into the text area."""
    if filepath is None:
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Hackus Pad Files", "*.hackus"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
    else:
        file_path = filepath
        
    if not file_path:
        return
    try:
        with open(file_path, "r") as file:
            content = file.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, content)
        root.title(f"Hackus Pad - {file_path}")
        text_area.edit_modified(False)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")

def save_file():
    """Saves the current content to a file."""
    current_title = root.title()
    if "Untitled" in current_title:
        save_file_as()
        return

    file_path = current_title.replace("Hackus Pad - ", "")
    try:
        with open(file_path, "w") as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
        text_area.edit_modified(False)
        status_bar.config(text=f"Saved: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

def save_file_as():
    """Saves the current content to a new file. Now defaults to .hackus"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".hackus",  # THIS IS THE CRITICAL FIX
        filetypes=[
            ("Hackus Pad Files", "*.hackus"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )
    if not file_path:
        return
    try:
        with open(file_path, "w") as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
        root.title(f"Hackus Pad - {file_path}")
        text_area.edit_modified(False)
        status_bar.config(text=f"Saved: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

def change_theme(theme_name):
    """Applies the selected theme to the entire application."""
    theme = THEMES[theme_name]
    
    # Apply theme to all components
    root.configure(bg=theme["bg"])
    text_area.configure(
        bg=theme["bg"],
        fg=theme["fg"],
        selectbackground=theme["select_bg"]
    )
    menu_bar.configure(bg=theme["menu_bg"], fg=theme["menu_fg"])
    status_bar.configure(bg=theme["status_bg"], fg=theme["status_fg"])
    
    # Update all menus to maintain theme consistency
    for menu in [file_menu, theme_menu, options_menu]:
        menu.configure(bg=theme["menu_bg"], fg=theme["menu_fg"])
    
    # Update the current theme variable
    global current_theme
    current_theme = theme_name
    status_bar.config(text=f"Theme changed to: {theme_name}")

def change_font_color():
    """Opens a color chooser dialog to change the text color."""
    color_code = colorchooser.askcolor(
        title="Choose Font Color",
        initialcolor=text_area.cget("fg")
    )
    if color_code[1]:
        new_color = color_code[1]
        text_area.configure(fg=new_color)
        status_bar.config(text=f"Font color changed to {new_color}")

# Create the main window
root = tk.Tk()
root.title("Hackus Pad - Untitled")
root.geometry("800x600")

# Set default font style
font_style = ("Consolas", 12)
current_theme = "Hacker (Default)"

# Create a menu bar
menu_bar = tk.Menu(root, bg="black", fg="#00FF00")
root.config(menu=menu_bar)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="#00FF00")
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_file_as, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Themes menu
theme_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="#00FF00")
menu_bar.add_cascade(label="Themes", menu=theme_menu)

# Add all theme options to the menu
for theme_name in THEMES.keys():
    theme_menu.add_command(
        label=theme_name,
        command=lambda name=theme_name: change_theme(name)
    )

# Create Options menu
options_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="#00FF00")
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Change Font Color", command=change_font_color)

# Create the text area
text_area = tk.Text(
    root,
    bg="black",
    fg="#00FF00",
    insertbackground="#00FF00",
    font=font_style,
    relief=tk.FLAT,
    padx=10,
    pady=10,
    selectbackground="#004400"
)
text_area.pack(fill=tk.BOTH, expand=True)

# Create a status bar
status_bar = tk.Label(
    root,
    text="Ready - Hacker Theme Active",
    bg="black",
    fg="#00FF00",
    font=("Consolas", 10),
    anchor=tk.W
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Configure tags for the text area
text_area.tag_configure("found", background="#003300")

# Add keyboard shortcuts
root.bind('<Control-n>', lambda event: new_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-S>', lambda event: save_file_as())

# Apply the default theme
change_theme("Hacker (Default)")

# Check if a file path was provided as a command-line argument
if len(sys.argv) > 1:
    file_to_open = sys.argv[1]
    if os.path.exists(file_to_open):
        open_file(file_to_open)

# Start the application
root.mainloop()