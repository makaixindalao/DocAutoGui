import pyautogui
import time
import os
import ai
import pic
import logging
from pynput.keyboard import Controller

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler()
    ]
)

keyboard = Controller()


def delay_txt():
    """
    删除文本框中的内容。
    """
    for _ in range(3):
        pyautogui.click()
        time.sleep(0.1)
    pyautogui.press('delete')


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
            logging.warning(f"超时未找到图像: {image_path}")
            return None
        logging.info("页面加载中...")
        time.sleep(1)


def read_names(file_path):
    """
    从文件中读取姓名列表。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        names = file.readlines()
    return [name.strip() for name in names]


def remove_name(file_path, name_to_remove):
    """
    从文件中删除指定的姓名。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != name_to_remove:
                file.write(line)


def input_text(x, y, txt):
    """
    在指定位置输入文本。
    """
    pyautogui.click(x, y)
    delay_txt()
    keyboard.type(txt)
    time.sleep(0.5)


def click_and_wait(image_path, x, y, timeout=60):
    """
    点击指定位置并等待图像出现。
    """
    pyautogui.click(x, y)
    return wait_for_image(image_path, timeout)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [os.path.join(
        current_dir, 'pic', f'{i}.png') for i in range(1, 5)]
    names_file = os.path.join(current_dir, 'names.txt')
    names = read_names(names_file)
    faultFlag = False 

    coustem_y = 418
    coustem_text = "药疹"
    coustem_num = 7
    page = 2

    for i, name in enumerate(names):
        if faultFlag:
            coustem_num += 1
            pyautogui.press('f5')
            faultFlag = False
        if i >= coustem_num:
                break
        
        logging.info(f"运行第 {i + 1} 次")
        if not wait_for_image(image_paths[0]):
            faultFlag = True
            continue

        logging.info("点击大病历")
        if not click_and_wait(image_paths[1], 422, 329):
            faultFlag = True
            continue

        logging.info("点击疾病")
        pyautogui.click(440, 396)
        time.sleep(1)
        if page > 1:
            for _ in range(page - 1):
                pyautogui.click(671, 649)
                time.sleep(0.5)
        logging.info(f"选择{coustem_text}")
        pyautogui.click(1000, coustem_y)
        pyautogui.click(1040, 294)

        input_text(451, 769, name)
        pyautogui.click(759, 776)
        logging.info(f"生成病历中, 姓名为{name}")
        prompt = f"姓名为{name}生成一份随机病历, 诊断为{coustem_text}，只包含主诉、现病史、既往史、个人史、家族史、体格检查、辅助检查、诊断，不要有性别、年龄、病历编号等其他信息, 回复纯文本, 不要用md"
        result = ai.call_chatgpt_api(prompt)
        logging.info(result)

        if not wait_for_image(image_paths[3]):
            faultFlag = True
            continue

        input_text(448, 837, coustem_text)
        input_text(656, 967, result)

        pyautogui.click(580, 1388)
        logging.info("提交")
        if not wait_for_image(image_paths[2]):
            faultFlag = True
            continue

        time.sleep(1)
        pic.find_and_click_image(image_paths[2])

        logging.info("删除已处理的名字")
        remove_name(names_file, name)
    logging.info("任务完成")


if __name__ == "__main__":
    main()
