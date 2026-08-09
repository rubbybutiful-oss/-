import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
client = OpenAI(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """너는 '똑순이'라는 알뜰 소비 도우미다.
사용자의 구매 목적, 예산, 지출 일정, 현재 자산을 고려해 무조건 구매를 권하지 않고
필요성, 대체 가능성, 충동구매 가능성을 함께 판단한다. 청소년에게도 이해하기 쉬운 한국어로 답한다."""

def offline_reply(messages):
    q = messages[-1]["content"].strip()
    return (
        "똑순이 무료 데모 분석입니다. 😊\n\n"
        f"입력 내용: {q}\n\n"
        "• 지출 일정: 가까운 시일 내 꼭 필요한 지출이 있다면 우선순위를 확인해 보세요.\n"
        "• 현재 자산: 가진 돈 전체가 아니라 앞으로 필요한 지출을 제외하고 판단하는 것이 좋아요.\n"
        "• 필요성: '지금 꼭 필요한가?'를 먼저 생각해 보세요.\n"
        "• 대체 가능성: 이미 가진 물건이나 더 저렴한 대안이 있는지 확인해 보세요.\n"
        "• 충동구매 위험: 할인·한정판매·마감 임박 같은 표현에 서두르고 있지는 않은지 확인해 보세요.\n\n"
        "※ 현재는 API 없이 실행되는 데모 버전입니다."
    )

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/recommend")
def recommend():
    data = request.get_json(silent=True) or {}
    item = data.get("item", "")
    budget = data.get("budget", "")
    purpose = data.get("purpose", "")
    schedule = data.get("schedule", "")
    assets = data.get("assets", "")
    prompt = f"""구매 대상: {item}
사용 가능 예산: {budget}
구매 목적: {purpose}
지출 일정: {schedule}
현재 자산: {assets}

이 정보를 바탕으로 알뜰 소비 분석을 해줘.
필요성, 지출 일정과 자산을 고려한 부담 정도, 대체 가능성, 충동구매 위험, 최종 조언을 간결하게 제시해줘."""

    if client:
        try:
            response = client.responses.create(
                model=MODEL, instructions=SYSTEM_PROMPT, input=prompt
            )
            answer = response.output_text.strip()
            if answer:
                return jsonify({"answer": answer, "mode": "api"})
        except Exception:
            pass

    return jsonify({"answer": offline_reply([{"role":"user","content":prompt}]), "mode":"offline"})

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error":"메시지가 없습니다."}), 400
    if client:
        try:
            response = client.responses.create(
                model=MODEL, instructions=SYSTEM_PROMPT, input=messages[-20:]
            )
            if response.output_text.strip():
                return jsonify({"answer":response.output_text.strip(), "mode":"api"})
        except Exception:
            pass
    return jsonify({"answer":offline_reply(messages), "mode":"offline"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
