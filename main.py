from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import csv
import re

app = FastAPI()

# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/submit")
async def submit_data(req: Request):
    data = await req.json()
    text = data.get("text")
    print(f"✅ 收到前端发送数据: {text}")

    # 正则提取各字段
    school_match = re.search(r"^(.*?大学)", text)
    department_match = re.search(r"大学\s+(.*?研究[科院])", text)
    lab_match = re.search(r"(研究室|研究グループ|研究チーム|研究部門)\s*([^\s，,]+)", text)
    professor_match = re.search(r"教授\s*(\S+)", text)
    theme_match = re.search(r"研究方向[是为]([^\s，,。]*)", text)
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

    school = school_match.group(1) if school_match else ""
    department = department_match.group(1) if department_match else ""
    lab = lab_match.group(2) if lab_match else ""
    professor = professor_match.group(1) if professor_match else ""
    theme = theme_match.group(1) if theme_match else ""
    email = email_match.group(0) if email_match else ""

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 保存到 CSV
    with open("data.csv", "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, school, department, lab, professor, theme, email])

    return {"message": "提交成功"}

