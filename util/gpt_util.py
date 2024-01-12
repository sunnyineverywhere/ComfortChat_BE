import openai
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))
openai.api_key = os.environ.get("GPT_KEY")


def get_gpt_answer(question, model="gpt-3.5-turbo-0613"):
    content = (
            "경계성 지능장애를 가진 사람이 질문하는거야."
            + question
            + ". 다음과 같은 json 양식으로 답해줘."
            + "isOkay는 해도 되는지 안되는지에 대한 여부, keyword는 네 답변의 주의점 중심 짧은 요약 + answer는 경계성 지능장애인에게 알맞은 친절하고 자세한 답변"
            + "{\n'isOkay': boolean type,"
            + "'keyword':'',"
            + "'answer':''\n}"
    )
    messages = [{"role": "assistant", "content": content}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message["content"]
