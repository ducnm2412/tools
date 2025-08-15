import subprocess
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from concurrent.futures import ThreadPoolExecutor, as_completed

# Danh sách thiết bị (thay bằng ID thật)
devices = ["emulator-5554", "emulator-5556"]

# --- Hàm scroll trên từng thiết bị ---
def scroll_device(device_id, times, delay, log_widget):
    try:
        log_widget.insert(tk.END, f"[{device_id}] Bắt đầu scroll {times} lần\n")
        log_widget.see(tk.END)
        for i in range(1, times + 1):
            subprocess.Popen(f'adb -s {device_id} shell input swipe 415 1172 255 430 300', shell=True)
            log_widget.insert(tk.END, f"[{device_id}] Scroll lần {i}\n")
            log_widget.see(tk.END)
            time.sleep(delay)
        log_widget.insert(tk.END, f"[{device_id}] Hoàn thành scroll\n")
        log_widget.see(tk.END)
    except Exception as e:
        log_widget.insert(tk.END, f"[{device_id}] Lỗi: {e}\n")
        log_widget.see(tk.END)

# --- Hàm gọi khi nhấn nút "Start" ---
def start_scroll():
    try:
        times = int(times_entry.get())
        delay = float(delay_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        return

    # Sử dụng ThreadPoolExecutor
    max_threads = len(devices)  # 1 thread cho mỗi thiết bị
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scroll_device, device, times, delay, log_text): device for device in devices}

        # Thread giám sát hoàn tất để thông báo
        def check_completion():
            for future in as_completed(futures):
                # Chỉ cần chờ tất cả future hoàn thành
                pass
            messagebox.showinfo("Hoàn thành", "Đã scroll xong tất cả thiết bị!")

        # Chạy thread giám sát để không block GUI
        threading.Thread(target=check_completion).start()

# --- GUI ---
root = tk.Tk()
root.title("ADB Scroll Phone Farm")

tk.Label(root, text="Số lần scroll:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
times_entry = tk.Entry(root)
times_entry.grid(row=0, column=1, padx=10, pady=5)
times_entry.insert(0, "5")  # default

tk.Label(root, text="Thời gian chờ sau mỗi lần (s):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
delay_entry = tk.Entry(root)
delay_entry.grid(row=1, column=1, padx=10, pady=5)
delay_entry.insert(0, "0.5")  # default

start_button = tk.Button(root, text="Start Scroll", command=start_scroll)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# --- ScrolledText để hiển thị log trạng thái ---
log_text = scrolledtext.ScrolledText(root, width=50, height=15)
log_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
