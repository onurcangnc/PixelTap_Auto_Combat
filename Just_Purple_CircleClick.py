import cv2
import numpy as np
import pyautogui
import time

pyautogui.PAUSE = 0.005

# Görüntüyü yükleme ve HSV değerlerini belirleme
image_path = 'image.PNG'
image = cv2.imread(image_path)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Pembe rengin HSV değerlerini bulma
# Bu işlemi manuel olarak belirlemek için bazı piksel değerlerine bakmak gerekebilir
# Burada basit bir örnek vereceğim
lower_pink = np.array([140, 50, 50])
upper_pink = np.array([170, 255, 255])

# Ekran görüntüsü alma fonksiyonu
def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

# Pembe çemberi tespit etme fonksiyonu
def find_pink_circle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # En büyük konturu bul
    max_contour = max(contours, key=cv2.contourArea) if contours else None
    
    if max_contour is not None:
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        if radius > 10:  # Minimum çember boyutu, gereksinimlere göre ayarlanabilir
            return int(x), int(y), int(radius)
    return None, None, None

# Pembe çembere 23 defa tıklama fonksiyonu
def click_pink_circle():
    frame = capture_screen()
    x, y, radius = find_pink_circle(frame)
    if x and y:
        for _ in range(50):
            pyautogui.mouseDown(x, y)
            pyautogui.mouseUp(x, y)
        print(f"{x}, {y} konumuna 23 defa tıklandı.")
    else:
        print("Pembe çember bulunamadı.")

# Botu çalıştır
try:
    while True:
        click_pink_circle()
        time.sleep(1)  # Her 3 saniyede bir tekrar et
except KeyboardInterrupt:
    print("Bot durduruldu.")
