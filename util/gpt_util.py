import openai
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))
openai.api_key = os.environ.get("GPT_KEY")


def get_gpt_answer(question, model="gpt-3.5-turbo-1106"):
    content = (
            "경계성 지능장애를 가진 사람이 질문하는거야. 너는 질문의 문제를 파악하고 행동에 대해 해도 되는지, 안되는지 보수적으로 답변해야해."
            + "질문: " + question
            + ". 다음과 같은 json 양식으로 답해줘. python json.loads 했을 때 정상적으로 작동하는 답변 보내줘."
            + "isOkay는 질문에 대해 의미 그대로 가능하면 true, 불가능하면 false, keyword는 질문의 문제상황 요약으로 보호자가 문제상황을 파악해야 해, answer는 경계성 "
              "지능장애인에게 알맞은 친절하고 자세한두괄식의 답변"
            + "{'isOkay': boolean type,"
            + "'keyword':'',"
            + "'answer':''}"
    )
    messages = [{"role": "assistant", "content": content}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message["content"]
