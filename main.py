import pyautogui
import time
import os
import ai
import pic
import random
import logging
import myOcr
import paddle

from pynput.keyboard import Controller
from datetime import datetime, timedelta

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler()
    ]
)

click_positions = [386, 406, 426, 451, 475, 495, 519, 542, 564, 585]
keyboard = Controller()
items = ["扁平苔藓", "剥脱性皮炎", "虫咬皮炎", "痤疮及酒渣鼻", "大疱性皮肤病", "代谢性皮肤病", "带状疱疹"]

def generate_random_date():
    start_date = datetime.strptime("2023-10-10", '%Y-%m-%d')
    end_date = datetime.strptime("2024-10-10", '%Y-%m-%d')
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

def delay_txt():
    for _ in range(3):
        pyautogui.click()
        time.sleep(0.1)
    pyautogui.press('delete')

def wait_for_image(image_path, timeout=60):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateOnScreen(image_path)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        if time.time() - start_time > timeout:
            logging.warning(f"超时未找到图像: {image_path}")
            return None
        print("页面加载中...")
        time.sleep(1)

def read_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [name.strip() for name in file.readlines()]

def remove_name(file_path, name_to_remove):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(line for line in lines if line.strip() != name_to_remove)

def input_text(x, y, txt):
    pyautogui.click(x, y)
    delay_txt()
    keyboard.type(txt)
    time.sleep(0.5)

def click_and_wait(image_path, x, y, timeout=60):
    pyautogui.click(x, y)
    return wait_for_image(image_path, timeout)

def compare_arrays(page_max):
    if page_max == 0:
        result = myOcr.get_line_str((485, 606, 40, 30))
        page_max = int(result[1])
        print(f"总页数为{page_max}")

    for _ in range(page_max):
        for _ in range(10):
            arr1 = myOcr.ocr_from_screenshot((580, 376, 40, 222))
            arr2 = myOcr.ocr_from_screenshot((755, 376, 40, 222))
            if len(arr1) == len(arr2):
                break
            print("长度不一致, 重新识别")

        for i in range(len(arr1)):
            try:
                if int(arr1[i]) > int(arr2[i]):
                    print(f"未完成位置：{i}, 需要{arr1[i]}, 已提交{arr2[i]}")
                    return False, i, page_max
            except ValueError:
                print("识别错误，重新识别")
                return False, i, page_max
        pyautogui.click(540, 613)
        time.sleep(1)

    return True, 0, page_max

def write_page1(name):
    print("输入姓名")
    input_text(316, 739, name)

    if not pic.find_and_click_image("pic/find.png"):
        return False
    
    wait_for_image("pic/find_result.png")

    task = random.choice(items)
    print(f"生成诊断中, 姓名为{name}")
    prompt = f"姓名为{name}生成一份随机病例, 诊断为{task}，不要有性别、年龄、病历编号等其他信息, 回复纯文本, 不要用md"
    result = ai.call_chatgpt_api(prompt)
    print(result)

    print("输入生成内容")
    input_text(445, 888, result)

    return True

def write_page2(name):
    print("输入时间")
    input_text(352, 740, generate_random_date())
    pyautogui.click(419, 700)

    print("输入病历号")
    input_text(333, 769, str(random.randint(1000000, 9999999)))

    print("输入病人信息")
    input_text(356, 806, name)

    print("输入诊断")
    task = random.choice(items)
    input_text(361, 840, task)

    print(f"生成诊断中, 姓名为{name}")
    prompt = f"姓名为{name}生成一份随机诊治, 诊断为{task}，不要有性别、年龄、病历编号等其他信息, 回复纯文本, 不要用md"
    result = ai.call_chatgpt_api(prompt)
    print(result)

    print("输入生成内容")
    input_text(332, 950, result)

    return True

#疾病位置
position1 = (314, 365)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [os.path.join(current_dir, 'pic', f'{i}.png') for i in range(1, 20)]
    names_file = os.path.join(current_dir, 'names.txt')
    names = read_names(names_file)
    faultFlag = False
    page_max = 0
    task = 1

    for i, name in enumerate(names):
        if faultFlag:
            pyautogui.press('f5')
            time.sleep(15)
            pic.find_and_click_image("pic/start.png")
            pic.find_and_click_image("pic/write.png")
            faultFlag = False

        print(f"运行第 {i + 1} 次")
        print("点击大类")

        if task == 1:
            firstImage = "pic/1.png"
        elif task == 2:
            firstImage = "pic/11.png"
        if not pic.find_and_click_image(firstImage, retries=60):
            faultFlag = True
            continue

        print("点击疾病")
        time.sleep(3)
        pyautogui.click(position1)
        time.sleep(5)

        print("寻找未填写完成的项目")
        ret, position, page_max = compare_arrays(page_max)
        if ret:
            break
        pyautogui.click(872, click_positions[position])
        pyautogui.click(908, 265)

        ret = False
        if task == 1:
            ret = write_page1(name)
        elif task == 2:
            ret = write_page2(name)

        if not ret:
            faultFlag = True
            continue

        print("开始提交")
        pyautogui.click(225, 100)
        pyautogui.moveTo(225, 100)
        pyautogui.scroll(-1000)
        time.sleep(4)

        if not pic.find_and_click_image("pic/commit.png"):
            pyautogui.click(450, 916)
        time.sleep(4)

        print("点击确认")
        if not pic.find_and_click_image(image_paths[2]):
            pyautogui.click(680, 190)
        time.sleep(3)
        pyautogui.click()

        print("删除已处理的名字")
        remove_name(names_file, name)

    print("任务完成")

if __name__ == "__main__":
    main()