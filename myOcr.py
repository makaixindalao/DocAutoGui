import pic
import os
import re
from cnocr import CnOcr

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

def ocr_from_image(image_path):
    """
    从给定的图像路径进行 OCR 识别。

    :param image_path: 图像文件的路径
    :return: 识别到的文本
    """
    ocr = CnOcr()
    result = ocr.ocr(image_path)

    result = extract_chinese_and_numbers(result)
    print(result)

    return result


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
    os.remove(temp_image_path)

    return result
