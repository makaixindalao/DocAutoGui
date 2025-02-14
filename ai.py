from openai import OpenAI

# 从 key.txt 文件中读取 API 密钥
with open("key.txt", "r") as file:
    api_key = file.read().strip()

client = OpenAI(
    api_key=api_key,  # 使用从文件中读取的密钥
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
        model="gpt-4o-mini",
    )
    # 返回 ChatGPT 的回复内容
    return chat_completion.choices[0].message.content
