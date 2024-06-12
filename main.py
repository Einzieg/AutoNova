import os
import sys
import cv2
import time
import random
import logging
import numpy as np
import pygetwindow as gw
import pyautogui

# 创建控制台处理器
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

# 创建文件处理器
file_handler = logging.FileHandler(filename='autonova.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

# 将处理器添加到根记录器中
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def resource_path(relative_path):
    """获取资源文件的绝对路径，打包后也适用"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 确保有一个名为 "Space" 的窗口，并获取其位置和大小
window = gw.getWindowsWithTitle('Space Armada')
if window:
    window = window[0]  # 选择第一个窗口
    # window.resizeTo(1920, 960)
    # window.moveTo(0, 0)
    window.maximize()
    window.activate()  # 将窗口置顶
else:
    raise Exception("未找到窗口，请检查是否已打开游戏窗口。")

# 加载怪物模板图像
monster_templates = [cv2.imread(resource_path('novaimgs/lv4_boss.png'), cv2.IMREAD_GRAYSCALE),
                     cv2.imread(resource_path('novaimgs/lv5_monster.png'), cv2.IMREAD_GRAYSCALE),
                     cv2.imread(resource_path('novaimgs/lv6_monster.png'), cv2.IMREAD_GRAYSCALE)]

# 加载残骸图标
debris_templates = [cv2.imread(resource_path('novaimgs/gather_wreckage.png'), cv2.IMREAD_GRAYSCALE),
                    cv2.imread(resource_path('novaimgs/gather_mineral.png'), cv2.IMREAD_GRAYSCALE)]

# 加载攻击图标
attack_icon = cv2.imread(resource_path('novaimgs/button_attack.png'), cv2.IMREAD_GRAYSCALE)
# 加载选择全部图标
select_all_icon = cv2.imread(resource_path('novaimgs/button_selectall.png'), cv2.IMREAD_GRAYSCALE)
# 加载确定图标
confirm_icon = cv2.imread(resource_path('novaimgs/button_confirm.png'), cv2.IMREAD_GRAYSCALE)
# 加载空间站图标
space_station_icon = cv2.imread(resource_path('novaimgs/to_station.png'), cv2.IMREAD_GRAYSCALE)
# 加载星系图标
star_system_icon = cv2.imread(resource_path('novaimgs/to_galaxy.png'), cv2.IMREAD_GRAYSCALE)

# 加载采集图标
collect_icon = cv2.imread(resource_path('novaimgs/button_collect.png'), cv2.IMREAD_GRAYSCALE)
# 加载关闭图标
close_icon = cv2.imread(resource_path('novaimgs/button_close.png'), cv2.IMREAD_GRAYSCALE)
# 加载主页图标
home_icon = cv2.imread(resource_path('novaimgs/button_home.png'), cv2.IMREAD_GRAYSCALE)
# 加载星系图标
galaxy_icon = cv2.imread(resource_path('novaimgs/in_nebula.png'), cv2.IMREAD_GRAYSCALE)

# 禁止点击区
no_click_zones = [
    (0, 35, 454, 375),  # 左上角人物、任务区
    (0, 913, 1024, 1026),  # 下方聊天栏
]

# 获取窗口位置和大小
window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height


# 根据图片返回屏幕坐标
def get_coordinate(img, confidence, offset=3):
    screenshot = pyautogui.screenshot(region=(window_left, window_top, window_width, window_height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # confidence = 0.65
    if max_val >= confidence:
        icon_w, icon_h = img.shape[::-1]
        icon_center_x = max_loc[0] + icon_w // 2
        icon_center_y = max_loc[1] + icon_h // 2
        # 加入随机偏移
        random_offset_x = random.randint(-offset, offset)
        random_offset_y = random.randint(-offset, offset)
        screen_x = window_left + icon_center_x + random_offset_x
        screen_y = window_top + icon_center_y + random_offset_y
        logging.info(f"匹配成功，坐标 [{screen_x}, {screen_y}]，随机偏移 [{random_offset_x}, {random_offset_y}]")

        for zone in no_click_zones:
            if zone[0] <= screen_x <= zone[2] and zone[1] <= screen_y <= zone[3]:
                logging.info(f"匹配失败，坐标 [{screen_x}, {screen_y}] 在禁止点击区")
                return None
        return screen_x, screen_y


# ------------------------------------------------------------------------
# 依次匹配怪物模板
def find_monster_coordinates(confidence=0.65):
    for template in monster_templates:
        coords = get_coordinate(template, confidence)
        if coords is not None:
            return coords
    logging.info("未找到怪物<<<")
    return None


# 匹配怪物
def find_monsters():
    logging.info("正在寻找怪物>>>")
    coordinates = find_monster_coordinates()
    if coordinates:
        x, y = coordinates
        pyautogui.mouseDown(x, y)
        time.sleep(0.3)
        pyautogui.mouseUp(x, y)
        time.sleep(3)


# 点击攻击
def attack_monsters():
    logging.info("正在匹配攻击图标>>>")
    screen_x, screen_y = get_coordinate(attack_icon, 0.6)
    pyautogui.click(screen_x, screen_y)
    time.sleep(3)


# 选择全部
def select_all():
    logging.info("正在匹配选择全部图标>>>")
    screen_x, screen_y = get_coordinate(select_all_icon, 0.6)
    pyautogui.click(screen_x, screen_y)
    time.sleep(3)


# 确定
def confirm():
    logging.info("正在匹配确定图标>>>")
    screen_x, screen_y = get_coordinate(confirm_icon, 0.6)
    pyautogui.click(screen_x, screen_y)
    time.sleep(3)


# 刷怪流程
def attack_process():
    logging.info("开始刷怪流程>>>")
    try:
        find_monsters()
        attack_monsters()
        select_all()
        confirm()
        logging.info("刷怪流程结束<<<")
        time.sleep(120)
    except TypeError:
        logging.info("未匹配,流程结束<<<")


# ------------------------------------------------------------------------
# 依次匹配残骸图标
def find_debris_coordinates(confidence=0.65):
    for template in debris_templates:
        coords = get_coordinate(template, confidence)
        if coords is not None:
            return coords
    logging.info("未找到残骸<<<")
    return None


def find_debris():
    logging.info("正在寻找残骸>>>")
    coordinates = find_debris_coordinates()
    if coordinates:
        x, y = coordinates
        # 进行点击操作
        pyautogui.mouseDown(x, y)
        time.sleep(0.3)
        pyautogui.mouseUp(x, y)
        time.sleep(3)


def collect():
    logging.info("正在匹配采集图标>>>")
    screen_x, screen_y = get_coordinate(collect_icon, 0.65)
    pyautogui.mouseDown(screen_x, screen_y)
    time.sleep(0.3)
    pyautogui.mouseUp(screen_x, screen_y)
    time.sleep(3)


def debris_process():
    logging.info("开始采集残骸流程>>>")
    for i in range(5):
        try:
            find_debris()
            collect()
            logging.info("采集残骸<<<")
            time.sleep(60)
        except TypeError:
            logging.info("未匹配<<<")


# ------------------------------------------------------------------------


# 空间站
def space_station():
    logging.info("正在匹配空间站图标>>>")
    try:
        screen_x, screen_y = get_coordinate(space_station_icon, 0.65)
        pyautogui.click(screen_x, screen_y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配空间站图标<<<")


# 星系
def star_system():
    logging.info("正在匹配星系图标>>>")
    try:
        screen_x, screen_y = get_coordinate(star_system_icon, 0.65)
        pyautogui.click(screen_x, screen_y)
        time.sleep(10)
    except TypeError:
        logging.info("未匹配星系图标<<<")


def close():
    logging.info("正在匹配关闭图标>>>")
    try:
        screen_x, screen_y = get_coordinate(close_icon, 0.65)
        pyautogui.click(screen_x, screen_y)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配关闭图标<<<")


def home():
    logging.info("正在匹配主页图标>>>")
    try:
        screen_x, screen_y = get_coordinate(home_icon, 0.65)
        pyautogui.click(screen_x, screen_y)
        time.sleep(3)
    except TypeError:
        logging.info("未匹配主页图标<<<")


# 缩小窗口
def zoom_out():
    logging.info("正在缩小窗口>>>")
    window_center_x = window_left + window_width // 2
    window_center_y = window_top + window_height // 2
    pyautogui.moveTo(window_center_x, window_center_y)
    scroll_amount = -500
    for i in range(30):
        pyautogui.scroll(scroll_amount)


# 放大窗口
def zoom_in():
    window_center_x = window_left + window_width // 2
    window_center_y = window_top + window_height // 2
    pyautogui.moveTo(window_center_x, window_center_y)
    scroll_amount = 500
    for i in range(5):
        pyautogui.scroll(scroll_amount)


# 重置视角流程
def reset_process():
    logging.info("正在重置视角>>>")
    close()
    home()
    space_station()
    star_system()
    zoom_out()
    time.sleep(3)


# TODO 禁止点击区域（需考虑屏幕比例） 完成
# TODO 操作面板（移除命令行）（点击开始、停止、日志打印）
# TODO 自动拉取更新


if __name__ == '__main__':
    logging.info("开始执行>>>")
    try:
        while True:
            time.sleep(3)
            # reset_process()
            attack_process()
            debris_process()
            time.sleep(60)
    except Exception as e:
        logging.error(f"主函数执行异常, 错误为: {e}", exc_info=True)
