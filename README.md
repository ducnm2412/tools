# 📱 ADB Scroll Phone Farm

Ứng dụng desktop để tự động scroll trên nhiều thiết bị Android thông qua ADB, được thiết kế đặc biệt cho phone farm.

## ✨ Tính năng chính

- 🎯 **Quản lý devices linh hoạt**: Thêm/xóa device ID một cách dễ dàng
- 🔄 **Scroll tự động**: Tự động scroll với cài đặt tùy chỉnh
- ⏸️ **Pause/Resume**: Tạm dừng và tiếp tục quá trình scroll
- 🔄 **Reset**: Dừng hoàn toàn và khởi động lại
- 📊 **Log real-time**: Theo dõi tiến trình scroll trên từng device
- 🎛️ **Cài đặt tùy chỉnh**: Số lần scroll, thời gian chờ, pause giữa các vòng

## 🚀 Cách sử dụng

### 1. Cài đặt dependencies

```bash
# Cài đặt Python packages
pip install -r requirements.txt

# Hoặc cài đặt PyInstaller để build app
pip install pyinstaller
```

### 2. Chạy ứng dụng

```bash
# Chạy trực tiếp từ source code
python watch_video.py

# Hoặc build thành app và chạy
python build_app.py
```

### 3. Sử dụng giao diện

1. **Thêm Device**: Nhập Device ID (ví dụ: `emulator-5554`) → Click "Add Device"
2. **Cài đặt Scroll**: Điều chỉnh các thông số theo ý muốn
3. **Bắt đầu**: Click "Start Scroll" để bắt đầu
4. **Điều khiển**: Sử dụng "Pause", "Resume", "Reset" khi cần

## 🛠️ Build thành ứng dụng desktop

### Sử dụng script tự động

```bash
# Chạy script build
python build_app.py
```

Script này sẽ:

- Tự động cài đặt PyInstaller
- Build ứng dụng thành file executable
- Tạo script cài đặt
- Hướng dẫn sử dụng

### Build thủ công

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build ứng dụng
pyinstaller --onefile --windowed --name "ADB_Scroll_Phone_Farm" watch_video.py
```

## 📁 Cấu trúc project

```
tools/
├── watch_video.py          # Source code chính
├── build_app.py            # Script build ứng dụng
├── requirements.txt        # Dependencies
├── README.md              # Hướng dẫn này
├── dist/                  # Thư mục chứa file executable (sau khi build)
│   └── ADB_Scroll_Phone_Farm
└── install.sh             # Script cài đặt (Linux/macOS)
```

## 🔧 Yêu cầu hệ thống

### Bắt buộc

- **Python 3.6+**
- **ADB (Android Debug Bridge)**
- **Thiết bị Android** được kết nối qua USB hoặc emulator

### Khuyến nghị

- **Windows 10+** / **macOS 10.14+** / **Ubuntu 18.04+**
- **RAM**: 4GB+
- **Storage**: 100MB+ (cho app)

## 📱 Kết nối thiết bị

### 1. Bật USB Debugging

- Vào **Settings** → **Developer options**
- Bật **USB debugging**
- Kết nối thiết bị qua USB

### 2. Kiểm tra kết nối ADB

```bash
# Liệt kê devices
adb devices

# Kết quả mong đợi:
# List of devices attached
# emulator-5554    device
# ABCD1234         device
```

### 3. Thêm device vào app

- Copy Device ID từ kết quả `adb devices`
- Paste vào ô "Device ID" trong app
- Click "Add Device"

## ⚙️ Cài đặt nâng cao

### Tùy chỉnh thời gian scroll

- **Số lần scroll**: Tổng số lần scroll trên mỗi device
- **Thời gian chờ**: Khoảng cách giữa các lần scroll (giây)
- **Pause mỗi N lần**: Tạm dừng sau mỗi N lần scroll
- **Thời gian pause**: Thời gian tạm dừng (giây)

### Tối ưu hiệu suất

- Sử dụng delay ≥ 0.5s để tránh quá tải
- Pause mỗi 3-5 lần scroll để giảm tải
- Không nên scroll quá nhiều lần liên tục

## 🐛 Xử lý lỗi thường gặp

### Lỗi "Không thể kết nối với device"

- Kiểm tra USB cable
- Bật USB debugging
- Chạy `adb kill-server && adb start-server`

### Lỗi "ADB chưa được cài đặt"

- Tải Android SDK Platform Tools
- Thêm vào PATH
- Restart terminal/command prompt

### App không chạy sau khi build

- Kiểm tra antivirus (có thể block file .exe)
- Chạy với quyền Administrator
- Kiểm tra Windows Defender

## 📞 Hỗ trợ

Nếu gặp vấn đề:

1. Kiểm tra log trong app
2. Chạy `adb devices` để kiểm tra kết nối
3. Kiểm tra Python version: `python --version`
4. Kiểm tra ADB version: `adb version`

## 📄 License

Project này được phát hành dưới MIT License.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

---

**Lưu ý**: Đảm bảo tuân thủ các quy định và điều khoản sử dụng của các nền tảng khi sử dụng ứng dụng này.
