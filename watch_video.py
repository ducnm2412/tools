import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Danh sách thiết bị (thay bằng ID thật)
devices = ["emulator-5554", "emulator-5556"]

# --- Hàm scroll trên từng thiết bị ---
def scroll_device(device_id, times, delay, log_widget, pause_every=3, pause_duration=2):
    log_widget.insert(tk.END, f"[{device_id}] Bắt đầu scroll {times} lần\n")
    log_widget.see(tk.END)
    for i in range(1, times + 1):
        subprocess.Popen(f'adb -s {device_id} shell input swipe 415 1172 225 430 300', shell=True)
        log_widget.insert(tk.END, f"[{device_id}] Scroll lần {i}\n")
        log_widget.see(tk.END)
        time.sleep(delay)

        # Nếu đã scroll đủ pause_every lần thì dừng tạm
        if i % pause_every == 0 and i != times:
            log_widget.insert(tk.END, f"[{device_id}] Dừng {pause_duration}s giữa các vòng\n")
            log_widget.see(tk.END)
            time.sleep(pause_duration)

    log_widget.insert(tk.END, f"[{device_id}] Hoàn thành scroll\n")
    log_widget.see(tk.END)

# --- Hàm gọi khi nhấn nút "Start" ---
def start_scroll():
    try:
        times = int(times_entry.get())
        delay = float(delay_entry.get())
        pause_every = int(pause_every_entry.get())
        pause_duration = float(pause_duration_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        return

    threads = []
    for device in devices:
        t = threading.Thread(target=scroll_device, args=(device, times, delay, log_text, pause_every, pause_duration))
        t.start()
        threads.append(t)

    # Thread kiểm tra khi tất cả scroll xong
    def check_threads():
        for t in threads:
            t.join()
        messagebox.showinfo("Hoàn thành", "Đã scroll xong tất cả thiết bị!")

    threading.Thread(target=check_threads).start()

# --- GUI ---
root = tk.Tk()
root.title("ADB Scroll Phone Farm")

tk.Label(root, text="Số lần scroll:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
times_entry = tk.Entry(root)
times_entry.grid(row=0, column=1, padx=10, pady=5)
times_entry.insert(0, "9")  # default

tk.Label(root, text="Thời gian chờ sau mỗi lần (s):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
delay_entry = tk.Entry(root)
delay_entry.grid(row=1, column=1, padx=10, pady=5)
delay_entry.insert(0, "0.5")  # default

tk.Label(root, text="Số lần trước khi dừng tạm:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
pause_every_entry = tk.Entry(root)
pause_every_entry.grid(row=2, column=1, padx=10, pady=5)
pause_every_entry.insert(0, "3")  # default

tk.Label(root, text="Thời gian dừng tạm (s):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
pause_duration_entry = tk.Entry(root)
pause_duration_entry.grid(row=3, column=1, padx=10, pady=5)
pause_duration_entry.insert(0, "2")  # default

start_button = tk.Button(root, text="Start Scroll", command=start_scroll)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

# --- ScrolledText để hiển thị log trạng thái ---
log_text = scrolledtext.ScrolledText(root, width=50, height=15)
log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
