import cv2
import numpy as np
import pyautogui
import time
import logging
import keyboard

# Configuration
pyautogui.PAUSE = 0.005
IMAGE_PATH = 'image.PNG'
LOWER_PINK = np.array([140, 50, 50])
UPPER_PINK = np.array([170, 255, 255])
CLICK_COUNT = 24
SLEEP_INTERVAL = 1
BRIGHT_YELLOW_PATH = './images/brightyellow.PNG'
COMBAT_PATH = './images/combat.PNG'
COMBAT2_PATH = './images/combat2.PNG'
NEW_GAME_PATH = './images/newgame.PNG'
EXIT_PATH = './images/exit.PNG'
NOTFOUND_PATH = './images/notfound.PNG'
NOTFOUND2_PATH = './images/notfound2.PNG'
MAX_RUNTIME = 8 * 60 * 60  # 8 hours in seconds
CONFIDENCE_LEVEL = 0.8

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Capture screen function
def capture_screen():
    try:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
    except Exception as e:
        logging.error(f"Failed to capture screen: {e}")
        return None

# Find pink circle function
def find_pink_circle(frame):
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_PINK, UPPER_PINK)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        max_contour = max(contours, key=cv2.contourArea) if contours else None
        if max_contour is not None:
            (x, y), radius = cv2.minEnclosingCircle(max_contour)
            if radius > 10:
                return int(x), int(y), int(radius)
        return None, None, None
    except Exception as e:
        logging.error(f"Error in find_pink_circle: {e}")
        return None, None, None

# Click pink circle function
def click_pink_circle():
    frame = capture_screen()
    if frame is None:
        return

    x, y, radius = find_pink_circle(frame)
    if x is not None and y is not None:
        for _ in range(CLICK_COUNT):
            pyautogui.mouseDown(x, y)
            pyautogui.mouseUp(x, y)
        logging.info(f"Clicked {CLICK_COUNT} times at position ({x}, {y}).")
    else:
        logging.warning("Pink circle not found.")

# Find and click image function with error handling
def find_and_click_image(image_path):
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
        if location is not None:
            pyautogui.click(location)
            logging.info(f"Clicked on {image_path}")
            return True
        return False
    except pyautogui.ImageNotFoundException:
        logging.warning(f"Image {image_path} not found on screen.")
        return False
    except Exception as e:
        logging.error(f"Error in find_and_click_image for {image_path}: {e}")
        return False

# Check if images are not found
def check_not_found_images():
    not_found = pyautogui.locateCenterOnScreen(NOTFOUND_PATH, confidence=CONFIDENCE_LEVEL)
    not_found2 = pyautogui.locateCenterOnScreen(NOTFOUND2_PATH, confidence=CONFIDENCE_LEVEL)
    return not_found or not_found2

# Global control variables
paused = False

# Pause/Continue handler
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        logging.info("Script paused.")
    else:
        logging.info("Script continued.")

# Exit handler
def exit_script():
    logging.info("Exiting script.")
    exit()

# Main bot function
def main():
    global paused
    start_time = time.time()
    clicked = find_and_click_image(BRIGHT_YELLOW_PATH)
    
    if not clicked:
        if find_and_click_image(COMBAT_PATH):
            time.sleep(1)  # Wait for 1 second after clicking combat.PNG
            if find_and_click_image(COMBAT2_PATH):
                time.sleep(4)  # Wait for 1 second after clicking combat2.PNG

                # Check for notfound images and wait until they disappear
                while check_not_found_images():
                    logging.info("Waiting for notfound images to disappear...")
                    time.sleep(3)

    time.sleep(3)  # Additional 3 seconds wait before starting the main loop

    try:
        while True:
            # Check for global key presses
            if keyboard.is_pressed('esc'):
                exit_script()
            if keyboard.is_pressed('p'):
                toggle_pause()
                while paused:
                    time.sleep(1)
                    if keyboard.is_pressed('c'):
                        toggle_pause()
            
            if not paused:
                click_pink_circle()
                time.sleep(SLEEP_INTERVAL)
                
                # Check runtime
                elapsed_time = time.time() - start_time
                if elapsed_time >= MAX_RUNTIME:
                    find_and_click_image(EXIT_PATH)
                    break
                
                if not find_pink_circle(capture_screen())[0]:  # Check if pink circle is not found
                    if find_and_click_image(NEW_GAME_PATH):
                        break
                    if find_and_click_image(EXIT_PATH):
                        break
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")

if __name__ == "__main__":
    main()
