import pyautogui

print("请将鼠标移动到禁止点击区域的左上角，然后按下 Enter 键...")
input()
left, top = pyautogui.position()
print(f"左上角坐标: ({left}, {top})")

print("请将鼠标移动到禁止点击区域的右下角，然后按下 Enter 键...")
input()
right, bottom = pyautogui.position()
print(f"右下角坐标: ({right}, {bottom})")

print(f"禁止点击区域: 左上角 ({left}, {top}), 右下角 ({right}, {bottom})")



