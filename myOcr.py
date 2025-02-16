import time
import pic
import os
import re
import paddlehub as hub
import cv2

# 提取中文和数字，返回数字数组
def extract_chinese_and_numbers(ocr_data):
    extracted_numbers = []  # 用于存储提取的数字

    for item in ocr_data:
        text = re.split(r'（', item['text'])[0]  # 去掉“（”及之后的字符
        # 使用正则表达式提取中文和数字
        matches = re.findall(r'[\u4e00-\u9fa5]+|[0-9]+', text)

        for match in matches:
            if match.isdigit():  # 检查是否为数字
                extracted_numbers.append(match)  # 添加到数字数组

    return extracted_numbers  # 返回中文文本和数字数组

def denoise_image(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 设置放大倍数
    scale_factor = 2  # 放大两倍

    # 获取原始图像的尺寸
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)

    # 放大图像
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    # 将彩色图像转换为灰度图像
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # # 使用高斯模糊降噪
    blurred_image = cv2.GaussianBlur(resized_image, (1, 1), 0)

    # 将降噪后的图像覆盖原始图像
    cv2.imwrite(image_path, blurred_image)

def ocr_from_image(image_path):
    """
    从给定的图像路径进行 OCR 识别。

    :param image_path: 图像文件的路径
    :return: 识别到的文本
    """
    denoise_image(image_path)
    ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效
    result = ocr.recognize_text(images=[cv2.imread(image_path)])
    text_array = [item['text'] for item in result[0]['data']]
    print(text_array)

    return text_array


def ocr_from_screenshot(region=None):
    """
    从屏幕截图中进行 OCR 识别。

    :param region: 截图范围，格式为 (left, top, width, height)
                    如果为 None，则截取整个屏幕
    :return: 识别到的文本
    """
    # 截取屏幕截图
    screenshot_image = pic.screenshot(region)

    # 保存截图到临时文件
    temp_image_path = "pic/temp.png"
    screenshot_image.save(temp_image_path)

    # 进行 OCR 识别
    result = ocr_from_image(temp_image_path)

    # 删除临时文件
    # os.remove(temp_image_path)

    return result

def get_line_str(region):
    """
    从屏幕截图中进行 OCR 识别。

    :param region: 截图范围，格式为 (left, top, width, height)
                    如果为 None，则截取整个屏幕
    :return: 识别到的文本
    """
    # 截取屏幕截图
    screenshot_image = pic.screenshot(region)

    # 保存截图到临时文件
    temp_image_path = "pic/temp.png"
    screenshot_image.save(temp_image_path)

    # 进行 OCR 识别
    ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效
    result = ocr.recognize_text(images=[cv2.imread(temp_image_path)])
    
    texts = [item['text'] for item in result[0]['data']]
    # texts = [item['text'] for item in data]

    # 拼装成字符串
    result = ''.join(texts)
    print(result)
    # 删除临时文件
    # os.remove(temp_image_path)

    return result