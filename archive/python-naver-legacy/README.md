# 네이버 지도 API · Flask / 엑셀 메일 (레거시)

이 폴더는 **과거 실습·실험용** 코드입니다.  
현재 서비스는 저장소 루트의 **`index.html` + 카카오 API** (GitHub Pages)가 본제품입니다.

- `app.py` — 네이버 클라우드 지도 API + Flask (`templates/` 필요, 루트에는 없음)
- `send_email.py` — 엑셀 기반 Gmail SMTP 테스트 스크립트
- `requirements.txt` / `run.bat` — 로컬 실행 참고용

실행 전 환경 변수로 키를 넣으세요 (파일에 비밀번호를 적지 마세요).

### app.py (네이버)

- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`

### send_email.py (Gmail)

- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- 선택: `EXCEL_FILE`, `SENDER_EMAIL`, `RECEIVER_EMAIL`, `MAX_EMAILS`

Windows PowerShell 예:

```powershell
$env:NAVER_CLIENT_ID="..."
$env:NAVER_CLIENT_SECRET="..."
python app.py
```
