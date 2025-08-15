import subprocess
import time

class Adb:
    def __init__(self, indexDevices) -> None:
        self.indexDevices = indexDevices
    def LoginFB(self, user, pas):
        pas_safe = pas.replace("&", "\\&")

        # Mở app Facebook
        subprocess.call(f"adb -s {self.indexDevices} shell monkey -p com.facebook.katana -c android.intent.category.LAUNCHER 1")
        time.sleep(10)

        # Điền email
        subprocess.call(f"adb -s {self.indexDevices} shell input tap 801 351")
        time.sleep(2)
        subprocess.call(f"adb -s {self.indexDevices} shell input tap 801 351")
        subprocess.call(f"adb -s {self.indexDevices} shell input text {user}")
        # Chuyển sang trường password
        subprocess.call(f"adb -s {self.indexDevices} shell input keyevent 61")
        subprocess.call(f"adb -s {self.indexDevices} shell input keyevent 66")
        time.sleep(1)

        # Điền password
        subprocess.call(f"adb -s {self.indexDevices} shell input text {pas_safe}")
        time.sleep(1)

        # Đến Button để đăng nhập để đăng nhập
        subprocess.call(f"adb -s {self.indexDevices} shell input keyevent 61")
        time.sleep(1)
        subprocess.call(f"adb -s {self.indexDevices} shell input keyevent 61")
        time.sleep(1)

        # Nhấn Enter để đăng nhập
        subprocess.call(f"adb -s {self.indexDevices} shell input keyevent 66")
        time.sleep(10) # ENTER
        # Lướt fb
    def Scroll(self, steeps):
        for i in range(steeps):  # scroll 10 lần
            subprocess.call(f"adb -s {self.indexDevices} shell input swipe 500 1500 500 500 300")
            time.sleep(10)
adb = Adb(indexDevices="emulator-5554")
adb.Scroll(10)