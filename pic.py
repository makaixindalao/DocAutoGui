ipmort pyautogui

def find_and_click_image(image_path, wait_time=3, retries=10, interval=0.5):
    """
    查找屏幕上的图片并点击。

    :param image_path: 图片文件的路径
    :param wait_time: 点击后的等待时间，单位为秒
    :param retries: 最大重试次数
    :param interval: 每次重试之间的间隔时间，单位为秒
    :return: 如果点击成功返回True，否则返回False
    """

    for attempt in range(retries):
        try:
            # 查找屏幕上的图片位置
            location = pyautogui.locateCenterOnScreen(image_path)
            if location is not None:
                # 点击图片中心位置
                pyautogui.click(location)
                print("点击成功！")
                time.sleep(wait_time)  # 点击后的等待时间
                return True
            else:
                print(f"未找到图片，正在重试... (尝试 {attempt + 1}/{retries})")
                time.sleep(interval)  # 等待重试的间隔时间
        except Exception as e:
            print(f"发生错误: {e}")
            return False

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