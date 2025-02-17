import pyautogui
import time
import keyboard

def locate():
    x, y = pyautogui.position()
    print(f"Mouse coords: x = {x}, y = {y}");

is_running = True;

def stop_program():
    print("Q Pressed. Exiting loop.");
    global is_running;
    is_running = False;

keyboard.add_hotkey('q', stop_program);

while is_running:

    locate();
    time.sleep(0.5);