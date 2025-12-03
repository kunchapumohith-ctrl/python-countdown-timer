import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import threading
import winsound  # For alarm sound (Windows only)

running = False
paused = False
pause_time = 0

def start_timer():
    global running, paused, pause_time
    if running:
        return

    target_str = entry.get()
    try:
        target_time = datetime.strptime(target_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        messagebox.showerror("Invalid Format", "Please use format: YYYY-MM-DD HH:MM:SS")
        return

    running = True
    paused = False
    pause_time = 0

    def countdown():
        global running, paused, pause_time
        while running:
            if paused:
                time.sleep(0.1)
                continue

            now = datetime.now()
            remaining = target_time - now - timedelta(seconds=pause_time)

            if remaining.total_seconds() <= 0:
                label.config(text="00:00:00:00")
                running = False
                play_alarm()
                messagebox.showinfo("Done!", "⏳ Countdown Finished!")
                break

            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            label.config(text=f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}")
            time.sleep(1)

    threading.Thread(target=countdown, daemon=True).start()


def pause_timer():
    global paused, pause_start
    if running and not paused:
        paused = True
        pause_start = time.time()


def resume_timer():
    global paused, pause_time
    if running and paused:
        paused = False
        pause_time += int(time.time() - pause_start)


def reset_timer():
    global running, paused
    running = False
    paused = False
    label.config(text="00:00:00:00")


def play_alarm():
    for _ in range(5):
        winsound.Beep(1000, 500)


# ---------------- UI ------------------

root = tk.Tk()
root.title("Advanced Countdown Timer")
root.geometry("500x300")
root.config(bg="#1e1e1e")

title = tk.Label(root, text="Advanced Countdown Timer", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

label = tk.Label(root, text="00:00:00:00", font=("Arial", 40, "bold"), bg="#1e1e1e", fg="#00FF88")
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=25)
entry.insert(0, "2025-12-31 23:59:59")
entry.pack(pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

start_btn = tk.Button(frame, text="Start", font=("Arial", 14), width=8, command=start_timer)
start_btn.grid(row=0, column=0, padx=5)

pause_btn = tk.Button(frame, text="Pause", font=("Arial", 14), width=8, command=pause_timer)
pause_btn.grid(row=0, column=1, padx=5)

resume_btn = tk.Button(frame, text="Resume", font=("Arial", 14), width=8, command=resume_timer)
resume_btn.grid(row=0, column=2, padx=5)

reset_btn = tk.Button(frame, text="Reset", font=("Arial", 14), width=8, command=reset_timer)
reset_btn.grid(row=0, column=3, padx=5)

root.mainloop()
