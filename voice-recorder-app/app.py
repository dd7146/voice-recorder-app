import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
recording = False
fs = 44100  # Sample rate
audio_data = None  # Holds recorded audio data

# Function to start recording
def start_recording():
    global recording, audio_data
    recording = True
    audio_data = []
    
    def record():
        # Record audio in chunks and append to audio_data
        chunk = sd.rec(int(1 * fs), samplerate=fs, channels=2, dtype='float64')
        sd.wait()
        audio_data.append(chunk)
        if recording:
            record()  # Recursively record if still recording

    record()  # Start recording
    record_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Function to stop recording
def stop_recording():
    global recording
    recording = False
    record_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Info", "Recording Finished")

# Function to save the recording
def save_recording():
    if audio_data is not None:
        filepath = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if filepath:
            # Concatenate recorded chunks and save
            wavfile.write(filepath, fs, np.concatenate(audio_data, axis=0) * 32767)
            messagebox.showinfo("Info", "Recording saved successfully")
    else:
        messagebox.showwarning("Warning", "No recording found to save!")

# Button hover effects with animations
def on_enter(event):
    event.widget.config(bg="#d1e7fd")  # Lighten background color
    event.widget['width'] = 20  # Scale up button width

def on_leave(event):
    event.widget.config(bg="#ffffff")  # Revert to original background color
    event.widget['width'] = 15  # Scale down button width

# Create the Tkinter window
root = tk.Tk()
root.title("Voice Recorder")
root.geometry("300x250")
root.config(bg="#a0c4ff")  # Light blue background color

# GUI Components
label = tk.Label(root, text="Voice Recorder", font=("Helvetica", 16, "bold"), bg="#a0c4ff")
label.pack(pady=20)

# Create buttons using tk.Button
record_button = tk.Button(root, text="Start Recording", command=start_recording, width=15, font=("Helvetica", 12), bg="#ffffff")
record_button.pack(pady=10)
record_button.bind("<Enter>", on_enter)
record_button.bind("<Leave>", on_leave)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state=tk.DISABLED, width=15, font=("Helvetica", 12), bg="#ffffff")
stop_button.pack(pady=10)
stop_button.bind("<Enter>", on_enter)
stop_button.bind("<Leave>", on_leave)

save_button = tk.Button(root, text="Save Recording", command=save_recording, width=15, font=("Helvetica", 12), bg="#ffffff")
save_button.pack(pady=10)
save_button.bind("<Enter>", on_enter)
save_button.bind("<Leave>", on_leave)

# Run the Tkinter loop
root.mainloop()
