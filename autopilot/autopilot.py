import pyautogui


def apply(speed, stages, stage):
    limit, action = stages[stage]

    if action == 'accelerate':
        if speed > limit:
            pyautogui.keyUp('z')
            pyautogui.keyUp('s')
            return stage+1
        pyautogui.keyUp('s')
        pyautogui.keyDown('z')
    elif action == 'break':
        if speed < limit:
            pyautogui.keyUp('z')
            pyautogui.keyUp('s')
            return stage+1
        pyautogui.keyUp('z')
        pyautogui.keyDown('s')
    elif action == 'idle':
        if speed < limit:
            return stage+1
        pyautogui.keyUp('z')
        pyautogui.keyUp('s')

    return stage


def fromJSON(json):
    stages = []
    for item in json:
        limit, action = int(json[item]['limit']),  json[item]['action']
        stages.append((limit, action))
    return stages