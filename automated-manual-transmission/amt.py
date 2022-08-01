import pyautogui


def apply(gearbox, gear, speed, rpm):
    # dont do anything when neutral or rear
    if gear > 5:
        return 0
    current_gear = gearbox.get(str(gear))
    current_gear_min = int(current_gear.get('min'))
    current_gear_max = int(current_gear.get('max'))

    if speed > current_gear_max:
        # gear up
        pyautogui.keyDown('shift')
        pyautogui.keyUp('shift')
        return 1
    elif speed < current_gear_min:
        # gear down
        pyautogui.keyDown('ctrl')
        pyautogui.keyUp('ctrl')
        return -1
    return 0
