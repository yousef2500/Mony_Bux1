import subprocess
import time
import threading
import os
import requests
from collections import deque

# إعدادات
SCRIPT_NAME = "bot.py"   # اسم سكربتك الأساسي
TIMEOUT = 300            # 5 دقائق بدون مخرجات = إعادة التشغيل

# بيانات بوت تليجرام
BOT_TOKEN = "7784987344:AAEIY3r5FAMQ7FhgBlA5o_KAvZMm7xPMO9g"
CHAT_ID = "5887438800"

last_output_time = time.time()
send_buffer = deque()

def send_to_telegram(message):
    """إرسال رسالة إلى تليجرام"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        # لو فيه مشكلة في الارسال هتظهر بس في الترمنال (مش هنبعتها لتليجرام)
        print("خطأ في إرسال الرسالة:", e)

def monitor_output(process):
    """مراقبة أي مخرجات للسكربت"""
    global last_output_time

    # Thread داخلي لإرسال الرسائل كل 7 ثواني بشكل مجمع
    def sender_loop():
        while True:
            time.sleep(7)
            if send_buffer:
                combined = "\n".join(list(send_buffer))
                send_buffer.clear()
                # قص الرسالة لأقصى حجم 4000 حرف (حد تليجرام)
                send_to_telegram(combined[:4000])

    threading.Thread(target=sender_loop, daemon=True).start()

    for line in iter(process.stdout.readline, b''):
        decoded = line.decode(errors="ignore").strip()
        # شيلنا الطباعة على الترمنال
        last_output_time = time.time()
        send_buffer.append(decoded)

while True:
    print(f"\n🟢 Starting {SCRIPT_NAME}...")
    send_to_telegram(f"تم تشغيل {SCRIPT_NAME}")

    process = subprocess.Popen(
        ["python3", SCRIPT_NAME],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        env={**os.environ, "PYTHON_FORCE_COLOR": "1"}
    )

    last_output_time = time.time()

    # بدء مراقبة المخرجات
    t = threading.Thread(target=monitor_output, args=(process,))
    t.daemon = True
    t.start()

    # حلقة لمراقبة حالة البرنامج
    while True:
        time.sleep(5)
        if process.poll() is not None:
            print("🔴 Script exited. Restarting...\n")
            send_to_telegram(f"{SCRIPT_NAME} توقف، يتم إعادة التشغيل...")
            break

        if time.time() - last_output_time > TIMEOUT:
            print("⚠️ No output for 5 minutes. Killing and restarting...\n")
            send_to_telegram(f"{SCRIPT_NAME} لم يطبع أي شيء لمدة 5 دقائق، يتم إعادة التشغيل...")
            process.kill()
            break

    time.sleep(5)