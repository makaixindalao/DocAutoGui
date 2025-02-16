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
    level=logging.info,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler()
    ]
)


click_postion = [417, 439, 464, 485, 507, 529, 553, 575, 592,620]


def generate_random_date():
    start_date_str = "2023-10-10"
    end_date_str = "2024-10-10"
    # 将字符串转换为日期对象
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # 计算日期范围内的随机日期
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)  # 生成随机天数
    random_date = start_date + timedelta(days=random_days)  # 计算随机日期
    
    return random_date.strftime('%Y-%m-%d')  # 返回格式化字符串


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
        print("页面加载中...")
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


def compare_arrays(page_max):
    arr1 = None
    arr2 = None

    if page_max == 0:
        result = myOcr.get_line_str((480, 630, 40, 40))
        print(result[1])
        page_max = int(result[1])
        print(f"总页数为{page_max}")
        #page_max = int(myOcr.ocr_from_screenshot((495, 641, 15, 15)))

    for m in range(page_max):
        for _ in range(10):
            arr1 = myOcr.ocr_from_screenshot((580, 410, 40, 222))
            arr2 = myOcr.ocr_from_screenshot((755, 410, 40, 222))

            if len(arr1) is len(arr2):            
                break
            print("长度不一致, 重新识别")
        
        for i in range(len(arr1)):
            try:
                if int(arr1[i]) > int(arr2[i]):
                    print(f"未完成位置：{i}, 需要{arr1[i]}, 已提交{arr2[i]}")
                    return False, i, page_max
            except:
                print("识别错误，重新识别")
                return True, i, page_max
        pyautogui.click(537, 649)
    
    return True, 0, page_max

items = ["扁平苔藓", "剥脱性皮炎", "虫咬皮炎", "痤疮及酒渣鼻", "大疱性皮肤病", "代谢性皮肤病", "带状疱疹"]

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [os.path.join(
        current_dir, 'pic', f'{i}.png') for i in range(1, 20)]
    names_file = os.path.join(current_dir, 'names.txt')
    names = read_names(names_file)
    faultFlag = False

    page_max = 0
    
    for i, name in enumerate(names):
        if faultFlag:
            pyautogui.press('f5')   
            time.sleep(15)
            pic.find_and_click_image("pic/start.png")
            pic.find_and_click_image("pic/write.png")
            faultFlag = False

        print(f"运行第 {i + 1} 次")
        print("点击大类")
        if not pic.find_and_click_image(image_paths[10], retries = 60):
            faultFlag = True
            continue

        if not pic.find_and_click_image(image_paths[10]):
            faultFlag = True
            continue

        print("点击疾病")
        time.sleep(2)
        if not pic.find_and_click_image(image_paths[11]):
            faultFlag = True
            continue

        time.sleep(2)

        print("寻找未填写完成的项目")
        ret, postion, page_max = compare_arrays(page_max)
        if ret:
            break
        pyautogui.click(865, click_postion[postion])

        pyautogui.click(901, 296)

        # 时间
        print("输入时间")
        input_text(343, 771, generate_random_date())
        pyautogui.click(534, 715)

        #病历号
        print("输入病历号")
        input_text(311, 808, str(random.randint(1000000, 9999999)))

        #信息
        print("输入病人信息")
        input_text(384, 839, name)

        #诊断
        print("输入诊断")
        task = items[random.randint(0, 6)]
        input_text(343, 872, task)
        
        print(f"生成诊断中, 姓名为{name}")
        prompt = f"姓名为{name}生成一份随机诊治, 诊断为{task}，不要有性别、年龄、病历编号等其他信息, 回复纯文本, 不要用md"
        result = ai.call_chatgpt_api(prompt)
        print(result)

        print("输入生成内容")
        input_text(650, 1000, result)

        print("开始提交")
        pyautogui.click(225, 131)
        pyautogui.moveTo(225, 131)
        pyautogui.scroll(-1000)

        time.sleep(2)
        # if not pic.find_and_click_image("pic/commit.png"):
        pyautogui.click(450, 901)

        time.sleep(1)

        print("点击确认")
        if not pic.find_and_click_image(image_paths[2]):
            faultFlag = True
            continue

        time.sleep(3)

        pyautogui.click()

        print("删除已处理的名字")
        remove_name(names_file, name)
        
    print("任务完成")


if __name__ == "__main__":
    main()
