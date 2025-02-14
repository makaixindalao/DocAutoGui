import ddddocr
import pic

# 创建 OCR 对象
def ocr_from_image(image_path):
    """
    从给定的图像路径进行 OCR 识别。

    :param image_path: 图像文件的路径
    :return: 识别到的文本
    """
    # 创建 OCR 对象
    ocr = ddddocr.DdddOcr()

    # 读取图像文件
    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    # 进行 OCR 识别
    result = ocr.classification(img_bytes)

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