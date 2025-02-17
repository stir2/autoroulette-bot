from termcolor import colored;
import pyautogui;
import keyboard;
import random;
import time;
import math;
import sys;

# Initialize vars
duration_lower_bound: float = 0.05;
duration_upper_bound: float = 0.1;
click_x: int = 0;
click_y: int = 0;
wager: int = 15;
is_running: bool = True;
best_wager: int;
rolls: int = 0;

# ↓↓ CHANGE THESE VARIABLES ↓↓
tokens: int = 210;
# currency = "tokens";
currency = "money";

# Check if the bid was successful; Red pixel for won wager
def is_red(x=34, y=213, threshold=200):
    screenshot = pyautogui.screenshot()
    rgb = screenshot.getpixel((x, y))
    return rgb[0] >= threshold and rgb[1] < 100 and rgb[2] < 100

# Move the cursor to random position inside a specified rectangle
def move_to_bounds(x1: int, y1: int, x2: int, y2: int):
    global click_x;
    global click_y;
    click_x = random.randint(x1, x2);
    click_y = random.randint(y1, y2);
    duration: float = random.uniform(duration_lower_bound, duration_upper_bound);
    pyautogui.moveTo(click_x, click_y, duration); 

# Click a set amount of times at a specified location
def click_times(num: int):
    pyautogui.click(click_x, click_y, num, 0.075);
    time.sleep(0.010);
 
# Calculate the best wager for any amount of tokens while asessing risk
def find_best_wager(tokens: int):
    t: int = tokens;

    # Calculate the chance that an iteration will fail depending on the wager
    def fail_chance(t: int, w: int):
        return 1 / (2 ** (math.floor(math.log(t / w, 2))));

    # Calculate the average tokens gained by a specific wager before failure
    def avg_gain(t: int, w: int):
        f: float = fail_chance(t, w);
        return (w) * (1 - f) * (1 - 2 * f) / (f);

    max: float = 0;
    global best_wager;
    best_wager = 0;
    for i in range(1, (int)(t * 0.5)):
        gain = avg_gain(t, i);
        if(gain > max):
            max = gain;
            best_wager = i;

    return best_wager;

# Bet on red, wager amount of clicks on the red button
def place_wager(wager: int):
    move_to_bounds(875, 770, 975, 810);
    time.sleep(0.010);
    click_times(wager);
    time.sleep(0.05);

# Click once on the roll button
def roll():
    move_to_bounds(700, 965, 1275, 1005);
    time.sleep(0.010);
    click_times(1);

# Click once on the clear button
def clear():
    move_to_bounds(1236, 877, 1288, 895);
    time.sleep(0.010);
    click_times(1);

# Stop the loop and exit
def stop_program():
    print("Q Pressed. Exiting loop.");
    global is_running;
    is_running = False;
    sys.exit(0)

keyboard.add_hotkey('q', stop_program);

money = tokens / 100;
wager = find_best_wager(tokens);
money_wager = wager / 100;

while is_running:
    clear();
    time.sleep(0.010);
    place_wager(wager);
    time.sleep(0.010);
    roll();
    rolls += 1;
    time.sleep(10);

    money_wager = wager / 100;
    prev_wager: int = wager;
    prev_money_wager: int = wager / 100;
    global result_text;
    global currency_symbol;
    global prev_wager_text;
    if(currency == "money"):
        currency_symbol = "$";
        prev_wager_text = prev_money_wager;
    else:
        currency_symbol = "";
        prev_wager_text = prev_wager;

    if(is_red()):
        tokens += wager;
        money = tokens / 100;
        wager = find_best_wager(tokens);
        money_wager = wager / 100;
        result_text = colored("[WON +" + currency_symbol + str(prev_wager_text) + "]", "green");
    else:
        tokens -= wager;
        money = tokens / 100;
        wager *= 2;
        money_wager = wager / 100;
        result_text = colored("[LOST -" + currency_symbol + str(prev_wager_text) + "]", "red");

    if(currency == "tokens"):
        print(result_text + "\t Tokens: " + colored(str(tokens), "blue") + "\t Wager: " + colored(str(wager), "blue") + "\t" + colored("(Iteration #" + str(rolls) + ")", "black"));
    else:
        print(result_text + "\t Money: $" + colored(str(money), "blue") + "\t Wager: " + colored("$" + str(money_wager), "blue") + "\t" + colored("(Iteration #" + str(rolls) + ")", "black"));