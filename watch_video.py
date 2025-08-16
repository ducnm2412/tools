import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Danh sách thiết bị
devices = []

# Biến điều khiển
is_paused = False
is_running = False
current_threads = []

# --- Hàm lấy kích thước màn hình ---
def get_screen_size(device_id):
    result = subprocess.run(
        f'adb -s {device_id} shell wm size', shell=True, capture_output=True, text=True
    )
    output = result.stdout.strip()
    if "Physical size" in output:
        size_str = output.split("Physical size:")[-1].strip()
        width, height = map(int, size_str.split("x"))
        return width, height
    return 1080, 1920  # default nếu không lấy được

# --- Hàm thêm device ---
def add_device():
    device_id = device_entry.get().strip()
    if not device_id:
        messagebox.showerror("Lỗi", "Vui lòng nhập Device ID")
        return
    
    if device_id in devices:
        messagebox.showerror("Lỗi", f"Device {device_id} đã tồn tại!")
        return
    
    # Kiểm tra device có kết nối không
    result = subprocess.run(f'adb -s {device_id} shell echo "test"', shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        messagebox.showerror("Lỗi", f"Không thể kết nối với device {device_id}. Vui lòng kiểm tra kết nối ADB.")
        return
    
    devices.append(device_id)
    device_entry.delete(0, tk.END)
    update_device_list()
    log_text.insert(tk.END, f"Đã thêm device: {device_id}\n")
    log_text.see(tk.END)

# --- Hàm xóa device ---
def remove_device():
    device_id = device_entry.get().strip()
    if not device_id:
        messagebox.showerror("Lỗi", "Vui lòng nhập Device ID cần xóa")
        return
    
    if device_id not in devices:
        messagebox.showerror("Lỗi", f"Device {device_id} không tồn tại trong danh sách!")
        return
    
    devices.remove(device_id)
    device_entry.delete(0, tk.END)
    update_device_list()
    log_text.insert(tk.END, f"Đã xóa device: {device_id}\n")
    log_text.see(tk.END)

# --- Hàm cập nhật hiển thị danh sách devices ---
def update_device_list():
    if devices:
        device_list_text.config(state=tk.NORMAL)
        device_list_text.delete(1.0, tk.END)
        for i, device in enumerate(devices, 1):
            device_list_text.insert(tk.END, f"{i}. {device}\n")
        device_list_text.config(state=tk.DISABLED)
    else:
        device_list_text.config(state=tk.NORMAL)
        device_list_text.delete(1.0, tk.END)
        device_list_text.insert(tk.END, "Chưa có device nào")
        device_list_text.config(state=tk.DISABLED)

# --- Hàm scroll trên từng thiết bị ---
def scroll_device(device_id, times, delay, log_widget, pause_every=3, pause_duration=2):
    global is_paused, is_running
    
    width, height = get_screen_size(device_id)
    x_center = width // 2
    y_start = int(height * 0.8)
    y_end = int(height * 0.2)

    log_widget.insert(tk.END, f"[{device_id}] Bắt đầu scroll {times} lần\n")
    log_widget.see(tk.END)

    for i in range(1, times + 1):
        if not is_running:
            log_widget.insert(tk.END, f"[{device_id}] Đã dừng\n")
            log_widget.see(tk.END)
            return
            
        # Kiểm tra pause
        while is_paused and is_running:
            time.sleep(0.1)
            
        if not is_running:
            return
            
        subprocess.Popen(f'adb -s {device_id} shell input swipe {x_center} {y_start} {x_center} {y_end} 500', shell=True)
        log_widget.insert(tk.END, f"[{device_id}] Scroll lần {i}\n")
        log_widget.see(tk.END)
        time.sleep(delay)

        # Pause giữa các vòng
        if i % pause_every == 0 and i != times:
            log_widget.insert(tk.END, f"[{device_id}] Dừng {pause_duration}s giữa các vòng\n")
            log_widget.see(tk.END)
            time.sleep(pause_duration)

    log_widget.insert(tk.END, f"[{device_id}] Hoàn thành scroll\n")
    log_widget.see(tk.END)

# --- Hàm gọi khi nhấn nút "Start" ---
def start_scroll():
    global is_running, is_paused, current_threads
    
    if not devices:
        messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất một device trước khi bắt đầu scroll!")
        return
    
    try:
        times = int(times_entry.get())
        delay = float(delay_entry.get())
        pause_every = int(pause_every_entry.get())
        pause_duration = float(pause_duration_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        return

    # Reset trạng thái
    is_running = True
    is_paused = False
    current_threads.clear()
    
    # Cập nhật trạng thái button
    start_button.config(state="disabled")
    pause_button.config(state="normal")
    reset_button.config(state="normal")

    threads = []
    for device in devices:
        t = threading.Thread(target=scroll_device, args=(device, times, delay, log_text, pause_every, pause_duration))
        t.start()
        threads.append(t)
        current_threads.append(t)

    def check_threads():
        for t in threads:
            t.join()
        if is_running:  # Chỉ hiển thị thông báo nếu không bị reset
            messagebox.showinfo("Hoàn thành", "Đã scroll xong tất cả thiết bị!")
            # Reset trạng thái button
            start_button.config(state="normal")
            pause_button.config(state="disabled")
            reset_button.config(state="disabled")
    
    threading.Thread(target=check_threads).start()

# --- Hàm pause/resume ---
def toggle_pause():
    global is_paused
    
    if is_paused:
        is_paused = False
        pause_button.config(text="Pause")
        log_text.insert(tk.END, "Đã tiếp tục scroll...\n")
    else:
        is_paused = True
        pause_button.config(text="Resume")
        log_text.insert(tk.END, "Đã tạm dừng scroll...\n")
    
    log_text.see(tk.END)

# --- Hàm reset ---
def reset_scroll():
    global is_running, is_paused, current_threads
    
    is_running = False
    is_paused = False
    
    # Đợi tất cả thread kết thúc
    for thread in current_threads:
        if thread.is_alive():
            thread.join(timeout=1)
    
    current_threads.clear()
    
    # Reset trạng thái button
    start_button.config(state="normal")
    pause_button.config(state="disabled")
    reset_button.config(state="disabled")
    pause_button.config(text="Pause")
    
    log_text.insert(tk.END, "Đã reset và dừng tất cả scroll\n")
    log_text.see(tk.END)

# --- GUI ---
root = tk.Tk()
root.title("ADB Scroll Phone Farm")

# Frame cho quản lý devices
device_frame = tk.LabelFrame(root, text="Quản lý Devices", padx=10, pady=5)
device_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(device_frame, text="Device ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
device_entry = tk.Entry(device_frame, width=20)
device_entry.grid(row=0, column=1, padx=5, pady=5)

# Frame cho các button quản lý device
device_button_frame = tk.Frame(device_frame)
device_button_frame.grid(row=0, column=2, padx=5)

add_device_button = tk.Button(device_button_frame, text="Add Device", command=add_device)
add_device_button.pack(side=tk.LEFT, padx=2)

remove_device_button = tk.Button(device_button_frame, text="Remove Device", command=remove_device)
remove_device_button.pack(side=tk.LEFT, padx=2)

# Hiển thị danh sách devices
tk.Label(device_frame, text="Danh sách devices:").grid(row=1, column=0, columnspan=3, pady=(10,5), sticky="w")
device_list_text = tk.Text(device_frame, height=3, width=50, state=tk.DISABLED)
device_list_text.grid(row=2, column=0, columnspan=3, pady=5)

# Frame cho cài đặt scroll
scroll_frame = tk.LabelFrame(root, text="Cài đặt Scroll", padx=10, pady=5)
scroll_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(scroll_frame, text="Số lần scroll:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
times_entry = tk.Entry(scroll_frame)
times_entry.grid(row=0, column=1, padx=10, pady=5)
times_entry.insert(0, "9")

tk.Label(scroll_frame, text="Thời gian chờ sau mỗi lần (s):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
delay_entry = tk.Entry(scroll_frame)
delay_entry.grid(row=1, column=1, padx=10, pady=5)
delay_entry.insert(0, "0.5")

tk.Label(scroll_frame, text="Số lần trước khi dừng tạm:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
pause_every_entry = tk.Entry(scroll_frame)
pause_every_entry.grid(row=2, column=1, padx=10, pady=5)
pause_every_entry.insert(0, "3")

tk.Label(scroll_frame, text="Thời gian dừng tạm (s):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
pause_duration_entry = tk.Entry(scroll_frame)
pause_duration_entry.grid(row=3, column=1, padx=10, pady=5)
pause_duration_entry.insert(0, "2")

# Frame cho các button điều khiển
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

start_button = tk.Button(button_frame, text="Start Scroll", command=start_scroll)
start_button.pack(side=tk.LEFT, padx=5)

pause_button = tk.Button(button_frame, text="Pause", command=toggle_pause, state="disabled")
pause_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_scroll, state="disabled")
reset_button.pack(side=tk.LEFT, padx=5)

# Log text
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Khởi tạo hiển thị danh sách devices
update_device_list()

root.mainloop()
