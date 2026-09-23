import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
import winreg
import shutil

def get_zomboid_workshop_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
    except Exception:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            winreg.CloseKey(key)
        except Exception:
            steam_path = None

    if steam_path:
        workshop_path = os.path.join(steam_path, "steamapps", "workshop", "content", "108600")
        if os.path.exists(workshop_path):
            return workshop_path
            
    common_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\workshop\content\108600",
        r"C:\Program Files\Steam\steamapps\workshop\content\108600",
        r"D:\Steam\steamapps\workshop\content\108600",
        r"D:\SteamLibrary\steamapps\workshop\content\108600",
        r"E:\SteamLibrary\steamapps\workshop\content\108600"
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
            
    return "/" 

def select_folder():
    start_dir = get_zomboid_workshop_path()
    folder_path = filedialog.askdirectory(title="Select the main mod folder", initialdir=start_dir)
    
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        btn_open.config(state=tk.DISABLED)
        status_label.config(text="Status: Waiting...", fg="#aaaaaa")

def process_audio():
    folder = folder_entry.get().strip()
    lufs = int(vol_slider.get())
    
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return
        
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showerror("Error", "FFmpeg not found!\n\nPlease make sure ffmpeg.exe is in the same folder as this tool.")
        return
        
    btn_run.config(state=tk.DISABLED, text="Processing...")
    btn_restore.config(state=tk.DISABLED)
    btn_open.config(state=tk.DISABLED)
    status_label.config(text="Status: Creating backups and normalizing...", fg="#f39c12")
    
    threading.Thread(target=run_ffmpeg, args=(folder, lufs), daemon=True).start()

def run_ffmpeg(folder, lufs):
    ogg_files_paths = []
    
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.ogg'):
                ogg_files_paths.append(os.path.join(root_dir, file))
    
    if not ogg_files_paths:
        root.after(0, lambda: status_label.config(text="Status: No .ogg files found!", fg="#e74c3c"))
        root.after(0, lambda: btn_run.config(state=tk.NORMAL, text="Apply Volume"))
        root.after(0, lambda: btn_restore.config(state=tk.NORMAL))
        return
        
    success_count = 0
    for file_path in ogg_files_paths:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        backup_path = file_path + ".bak"
        temp_path = os.path.join(dir_name, "temp_" + base_name)
        
        if not os.path.exists(backup_path):
            try:
                shutil.copy2(file_path, backup_path)
            except Exception as e:
                print(f"Failed to backup {base_name}: {e}")
                continue
        
        cmd = [
            "ffmpeg", "-y", "-i", backup_path,
            "-af", f"loudnorm=I={lufs}:LRA=7:TP=-2.0",
            "-c:a", "libvorbis", "-q:a", "4",
            temp_path
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(temp_path):
                os.replace(temp_path, file_path)
                success_count += 1
        except Exception as e:
            print(f"Failed to process {base_name}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    root.after(0, lambda: status_label.config(text=f"Status: Success! Processed {success_count} file(s).", fg="#2ecc71"))
    root.after(0, lambda: btn_run.config(state=tk.NORMAL, text="Apply Volume"))
    root.after(0, lambda: btn_restore.config(state=tk.NORMAL))
    root.after(0, lambda: btn_open.config(state=tk.NORMAL))

def restore_originals():
    folder = folder_entry.get().strip()
    
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return
        
    btn_run.config(state=tk.DISABLED)
    btn_restore.config(state=tk.DISABLED, text="Restoring...")
    btn_open.config(state=tk.DISABLED)
    status_label.config(text="Status: Restoring original files...", fg="#f39c12")
    
    threading.Thread(target=run_restore, args=(folder,), daemon=True).start()

def run_restore(folder):
    restored_count = 0
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.ogg.bak'):
                backup_path = os.path.join(root_dir, file)
                original_path = backup_path[:-4]
                
                try:
                    shutil.copy2(backup_path, original_path)
                    restored_count += 1
                except Exception as e:
                    print(f"Failed to restore {original_path}: {e}")

    if restored_count > 0:
        root.after(0, lambda: status_label.config(text=f"Status: Restored {restored_count} original file(s)!", fg="#3498db"))
    else:
        root.after(0, lambda: status_label.config(text="Status: No backups found to restore.", fg="#e74c3c"))
        
    root.after(0, lambda: btn_run.config(state=tk.NORMAL))
    root.after(0, lambda: btn_restore.config(state=tk.NORMAL, text="🔄 Restore Originals"))
    root.after(0, lambda: btn_open.config(state=tk.NORMAL))

def open_folder():
    folder = folder_entry.get().strip()
    if folder and os.path.exists(folder):
        os.startfile(folder)

# GUI Setup
root = tk.Tk()
root.title("Hex's PZ Volume Customizer")
root.geometry("520x400")
root.eval('tk::PlaceWindow . center')

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG = "#2d2d2d"
BTN_BG = "#27ae60"
BTN_OPEN_BG = "#8e44ad"
BTN_RESTORE_BG = "#c0392b"

root.config(bg=BG_COLOR)

tk.Label(root, text="Select Main Mod Folder (Auto-scans all subfolders):", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10)).pack(pady=(15, 2))

folder_frame = tk.Frame(root, bg=BG_COLOR)
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, width=45, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief=tk.FLAT)
folder_entry.pack(side=tk.LEFT, padx=5, ipady=4)
tk.Button(folder_frame, text="Browse", command=select_folder, bg="#3498db", fg=FG_COLOR, relief=tk.FLAT).pack(side=tk.LEFT)

default_path = get_zomboid_workshop_path()
if default_path != "/":
    folder_entry.insert(0, default_path)

tk.Label(root, text="Physical File Loudness (-45 Quiet | -28 Normal | -12 Loud):", bg=BG_COLOR, fg="#f39c12", font=("Arial", 9, "bold")).pack(pady=(15, 2))
vol_slider = tk.Scale(root, from_=-45, to=-12, resolution=1, orient=tk.HORIZONTAL, bg=BG_COLOR, fg=FG_COLOR, highlightthickness=0, length=300)
vol_slider.set(-28)
vol_slider.pack(pady=5)

tk.Label(root, text="Note: Processing takes less than 30 seconds depending on the audio files.", bg=BG_COLOR, fg="#aaaaaa", font=("Arial", 8, "italic")).pack(pady=2)

# TIP TEXT
tk.Label(root, text="Tip: Click 'Open Folder' to test the audio in Windows before launching the game!", bg=BG_COLOR, fg="#3498db", font=("Arial", 8, "bold")).pack(pady=(5, 0))

action_frame = tk.Frame(root, bg=BG_COLOR)
action_frame.pack(pady=10)

btn_run = tk.Button(action_frame, text="Apply Volume", command=process_audio, bg=BTN_BG, fg=FG_COLOR, font=("Arial", 10, "bold"), relief=tk.FLAT, activebackground="#2ecc71")
btn_run.grid(row=0, column=0, padx=5, ipadx=10, ipady=5)

btn_restore = tk.Button(action_frame, text="🔄 Restore Originals", command=restore_originals, bg=BTN_RESTORE_BG, fg=FG_COLOR, font=("Arial", 10, "bold"), relief=tk.FLAT, activebackground="#e74c3c")
btn_restore.grid(row=0, column=1, padx=5, ipadx=10, ipady=5)

btn_open = tk.Button(action_frame, text="📁 Open Folder", command=open_folder, bg=BTN_OPEN_BG, fg=FG_COLOR, font=("Arial", 10, "bold"), relief=tk.FLAT, state=tk.DISABLED)
btn_open.grid(row=0, column=2, padx=5, ipadx=10, ipady=5)

status_label = tk.Label(root, text="Status: Waiting...", bg=BG_COLOR, fg="#aaaaaa", font=("Arial", 9, "italic"))
status_label.pack()

root.mainloop()
