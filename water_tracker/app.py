from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import time

app = Flask(__name__)

# 假設使用字典模擬喝水記錄
records = [
    {"id": 1, "date": "2024-12-08", "amount": 1500},
    {"id": 2, "date": "2024-12-07", "amount": 2000},
]

# 通知功能（模擬）
notifications = []


# 主頁：顯示喝水記錄列表
@app.route("/")
def index():
    return render_template("index.html", records=records)


# 新增喝水記錄
@app.route("/record/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        new_record = {
            "id": len(records) + 1,
            "date": request.form["date"],
            "amount": int(request.form["amount"]),
        }
        records.append(new_record)
        return redirect(url_for("index"))
    return render_template("add_record.html")


# 編輯喝水記錄
@app.route("/record/edit/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = next((r for r in records if r["id"] == record_id), None)
    if not record:
        return "記錄不存在", 404

    if request.method == "POST":
        record["date"] = request.form["date"]
        record["amount"] = int(request.form["amount"])
        return redirect(url_for("index"))

    return render_template("edit_record.html", record=record)


# 刪除喝水記錄
@app.route("/record/delete/<int:record_id>")
def delete_record(record_id):
    global records
    records = [r for r in records if r["id"] != record_id]
    return redirect(url_for("index"))


# 背景通知功能
def notify_daily():
    while True:
        current_time = datetime.now()
        if current_time.hour == 20:  # 假設每天晚上 8 點通知
            notifications.append("請記得記錄今日的喝水量！")
        time.sleep(3600)  # 每小時檢查一次


# 啟動通知線程
notification_thread = threading.Thread(target=notify_daily, daemon=True)
notification_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
