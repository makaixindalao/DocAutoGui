import pyautogui
import time
import cv2


def find_and_click_image(image_path, retries=30, interval=1):
    """
    查找屏幕上的图片并点击。

    :param image_path: 图片文件的路径
    :param wait_time: 点击后的等待时间，单位为秒
    :param retries: 最大重试次数
    :param interval: 每次重试之间的间隔时间，单位为秒
    :return: 如果点击成功返回True，否则返回False
    """
    for attempt in range(retries):
        # 查找屏幕上的图片位置
        try:
            location = pyautogui.locateCenterOnScreen(image_path)
        except pyautogui.ImageNotFoundException:
            location = None
        if location is not None:
            # 点击图片中心位置
            pyautogui.click(location)
            print("点击成功！")
            return True
        else:
            print(f"未找到图片，正在重试... (尝试 {attempt + 1}/{retries})")
            time.sleep(interval)  # 等待重试的间隔时间

    print("达到最大重试次数，点击失败。")
    return False


def screenshot(region=None):
    """
    截取屏幕指定范围的截图。

    :param region: 截图范围，格式为 (left, top, width, height)
                    如果为 None，则截取整个屏幕
    :return: 截取的图像对象
    """
    try:
        # 截取屏幕
        screenshot_image = pyautogui.screenshot(region=region)
        return screenshot_image
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def find_images_on_screen(image_path, confidence=0.8):
    # 使用 pyautogui.locateAllOnScreen 找到所有匹配的图像
    locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

    # 转换为位置数组 (x1, y1, x2, y2)
    positions = []
    for loc in locations:
        positions.append((loc.left, loc.top, loc.left + loc.width, loc.top + loc.height))

    return positions

def wait_for_image(image_path, timeout=60):
    """
    等待直到屏幕上出现指定的图片。
    """
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateOnScreen(image_path)
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        if time.time() - start_time > timeout:
            print.warning(f"超时未找到图像: {image_path}")
            return None
        print("页面加载中...")
        time.sleep(1)