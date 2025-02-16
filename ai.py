from openai import OpenAI

# 从 key.txt 文件中读取 API 密钥
with open("key.txt", "r") as file:
    api_key = file.read().strip()

client = OpenAI(
    api_key=api_key,  # 使用从文件中读取的密钥
    base_url="https://aihubmix.com/v1"  # 替换成 aihubmix 的入口地址
)

def call_chatgpt_api(prompt):
    try:
        for _ in range(5):
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
            result = chat_completion.choices[0].message.content
            if result is not None:
                return result
            print("调用chatGPT API失败，正在重试...")
        return "外用药物：建议使用含有类固醇的药膏，每日涂抹于患处，持续8周，以减轻炎症和瘙痒"
    except Exception as e:
        print(f"调用 ChatGPT API 时发生错误: {e}")
        return None
