'''
Author: makaixin makaixindalao@163.com
Date: 2025-02-14 09:26:00
LastEditors: makaixin makaixindalao@163.com
LastEditTime: 2025-02-14 09:55:32
FilePath: \Doctor\ai.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from openai import OpenAI

client = OpenAI(
    # 将这里换成您在 aihubmix API keys 拿到的密钥
    api_key="sk-QWzsIjR963Je9cpjF003Ce06362a412eAe6dDfD437267e43",
    base_url="https://aihubmix.com/v1"  # 替换成 aihubmix 的入口地址
)


def call_chatgpt_api(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    # 返回 ChatGPT 的回复内容
    return chat_completion.choices[0].message.content
