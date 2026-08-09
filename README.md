# 똑순이 - 알뜰 소비 도우미

API 없이도 무료 데모로 실행할 수 있습니다.

## 실행
PowerShell에서 프로젝트 폴더로 이동한 뒤:
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```
브라우저에서 http://127.0.0.1:5000 접속.

## 입력 항목
- 구매 대상
- 사용 예정 금액
- 구매 목적
- 지출 일정
- 현재 자산

API가 없으면 데모 응답으로 작동하고, 나중에 API를 연결하면 실제 AI 분석으로 전환됩니다.
