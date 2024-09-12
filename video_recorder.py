import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import signal

# Global variables for recording options
recording_options = {
    'filename': 'output.mp4',
    'resolution': '1024x600',
    'preset': 'fast',
    'crf': '18',
    'monitor': ':0.0'
}

# Function to start recording
def start_recording():
    global process
    filename = recording_options['filename']
    if os.path.exists(filename):
        os.remove(filename)  # Remove old file if it exists

    # Command to start recording
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'x11grab',
        '-s', recording_options['resolution'],  # Screen resolution
        '-i', recording_options['monitor'],  # Screen index
        '-c:v', 'libx264',
        '-preset', recording_options['preset'],
        '-crf', recording_options['crf'],
        filename
    ]
    
    try:
        # Start the recording process
        process = subprocess.Popen(command)
    except FileNotFoundError:
        messagebox.showerror("Error", "ffmpeg not found. Please install ffmpeg.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return
    
    # Update GUI state
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Function to stop recording
def stop_recording():
    global process
    if process:
        try:
            process.send_signal(signal.SIGINT)  # Gracefully stop ffmpeg
            process.wait()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("Recording Stopped", "The video has been recorded successfully.")
    else:
        messagebox.showwarning("Warning", "No recording process found.")

# Function to populate monitor options
def populate_monitors():
    # Simulate monitors list (for actual use, populate dynamically)
    monitors = [':0.0', ':0.1']  # Add more if necessary
    return monitors

# Function to populate resolution options
def populate_resolutions():
    # Common screen resolutions
    resolutions = [
        '1920x1080',
        '1280x720',
        '1024x768',
        '800x600',
        '640x480'
    ]
    return resolutions

# Function to populate preset options
def populate_presets():
    # Common presets for libx264
    presets = [
        'ultrafast',
        'superfast',
        'veryfast',
        'faster',
        'fast',
        'medium',
        'slow',
        'slower',
        'veryslow'
    ]
    return presets

# Function to open options dialog
def open_options():
    options_window = tk.Toplevel(root)
    options_window.title("Recording Options")
    
    tk.Label(options_window, text="Filename:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    filename_entry = tk.Entry(options_window)
    filename_entry.grid(row=0, column=1, padx=10, pady=5)
    filename_entry.insert(0, recording_options['filename'])

    tk.Label(options_window, text="Resolution:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    resolution_combobox = ttk.Combobox(options_window, values=populate_resolutions())
    resolution_combobox.grid(row=1, column=1, padx=10, pady=5)
    resolution_combobox.set(recording_options['resolution'])

    tk.Label(options_window, text="Preset:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    preset_combobox = ttk.Combobox(options_window, values=populate_presets())
    preset_combobox.grid(row=2, column=1, padx=10, pady=5)
    preset_combobox.set(recording_options['preset'])

    tk.Label(options_window, text="CRF:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    crf_entry = tk.Entry(options_window)
    crf_entry.grid(row=3, column=1, padx=10, pady=5)
    crf_entry.insert(0, recording_options['crf'])
    
    tk.Label(options_window, text="Monitor:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    monitor_combobox = ttk.Combobox(options_window, values=populate_monitors())
    monitor_combobox.grid(row=4, column=1, padx=10, pady=5)
    monitor_combobox.set(recording_options['monitor'])

    def save_options():
        recording_options['filename'] = filename_entry.get()
        recording_options['resolution'] = resolution_combobox.get()
        recording_options['preset'] = preset_combobox.get()
        recording_options['crf'] = crf_entry.get()
        recording_options['monitor'] = monitor_combobox.get()
        options_window.destroy()

    save_button = tk.Button(options_window, text="Save", command=save_options)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

# Function to open about dialog
def open_about():
    messagebox.showinfo("About", "Video Recorder v1.0\nCreated with Tkinter and ffmpeg.")

# Initialize the main window
root = tk.Tk()
root.title("Video Recorder")


# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add 'Options' menu
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Configure Recording Options", command=open_options)
options_menu.add_command(label="About", command=open_about)

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create tabs
record_frame = ttk.Frame(notebook)
notebook.add(record_frame, text="Record")

play_frame = ttk.Frame(notebook)
notebook.add(play_frame, text="Play")

# Create and pack buttons in the "Record" tab
start_button = tk.Button(record_frame, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(record_frame, text="Stop Recording", command=stop_recording, state=tk.DISABLED)
stop_button.pack(pady=10)

# The "Play" tab can be used for other functionalities or left empty

# Global variable to manage the recording process
process = None

# Run the Tkinter event loop
root.mainloop()
