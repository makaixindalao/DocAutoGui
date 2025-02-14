from xml.etree.ElementTree import tostring

import pyautogui
import time
import os
import ai

from pynput.keyboard import Controller
keyboard = Controller()


def find_and_click_image(image_path, wait_time=3):
    """
    查找屏幕上的图片并点击。

    :param image_path: 图片文件的路径
    :param wait_time: 等待时间，单位为秒
    :return: 如果点击成功返回True，否则返回False
    """

    try:
        # 查找屏幕上的图片位置
        location = pyautogui.locateCenterOnScreen(image_path)
        if location is not None:
            # 点击图片中心位置
            pyautogui.click(location)
            print("点击成功！")
            return True
        else:
            print("未找到图片。")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False


def delay_txt():
    """
    删除文本框中的内容。
    """
    # 鼠标左键点击三下
    for _ in range(3):
        pyautogui.click()
        time.sleep(0.1)  # 每次点击之间的间隔

    # 按下删除键
    pyautogui.press('delete')


def wait_for_image(image_path, timeout=60):
    """
    等待直到屏幕上出现指定的图片。
    """

    start_time = time.time()
    while True:
        try:
            # 查找图像
            location = pyautogui.locateOnScreen(image_path)
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        if time.time() - start_time > timeout:
            print("超时未找到图像")
            return None
        # 等待一段时间再重试
        print("等待页面加载...")
        time.sleep(1)


def read_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        names = file.readlines()
    return [name.strip() for name in names]


def remove_name(file_path, name_to_remove):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != name_to_remove:
                file.write(line)


def input_text(x, y, txt):
    pyautogui.click(x, y)
    delay_txt()
    keyboard.type(txt)
    time.sleep(0.5)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [os.path.join(
        current_dir, 'pic', f'{i}.png') for i in range(1, 5)]

    names_file = os.path.join(current_dir, 'names.txt')
    names = read_names(names_file)

    for i, name in enumerate(names):
        print(f"运行第 {i + 1} 次")
        if i >= 167:
            break
        wait_for_image(image_paths[0])

        # 模拟点击
        print("点击大病历")
        pyautogui.click(422, 329)
        wait_for_image(image_paths[1])
        print("点击疾病")
        pyautogui.click(440, 396)
        time.sleep(1)
        print("选择皮疹")
        pyautogui.click(1000, 552)
        pyautogui.click(1040, 294)

        # 输入姓名并生成病历
        input_text(451, 769, name)
        pyautogui.click(759, 776)
        print("生成病历中, 姓名为", name)
        prompt = f"姓名为{name}生成一份随机病历, 诊断为皮疹，只包含主诉、现病史、既往史、个人史、家族史、体格检查、辅助检查、诊断，不要有性别、年龄、病历编号等其他信息, 回复纯文本，不要用md"
        result = ai.call_chatgpt_api(prompt)
        print(result)

        wait_for_image(image_paths[3])
        input_text(448, 837, "皮疹")
        input_text(656, 967, result)

        pyautogui.click(580, 1388)
        print("提交")
        wait_for_image(image_paths[2])
        time.sleep(1)
        find_and_click_image(image_paths[2])
        # pyautogui.click(813, 188)

        # 删除已处理的名字
        print("删除已处理的名字")
        remove_name(names_file, name)


if __name__ == "__main__":
    main()
