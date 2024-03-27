import os

import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
print(GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)


def translate(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"请用中文翻译以下内容，不要遗漏细节，只返回翻译：{text}")
    return response.text


if __name__ == '__main__':
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    str = """
    Make the node "storage-node-13" available for scheduling new pods;Mark node as schedulable.
    """
    print(translate(str))
    pass
