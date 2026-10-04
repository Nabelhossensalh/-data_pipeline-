import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# إعداد مسار src تلقائياً داخل بايثون دون الحاجة لأي أوامر خارجية
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import uvicorn


def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 تم تشغيل سيرفر مشروع البيانات الضخمة (Big Data - Phase 2)")
    print("  🌐 السيرفر يعمل على: http://127.0.0.1:8000")
    print("  📖 واجهة Swagger التفاعلية: http://127.0.0.1:8000/docs")
    print("=" * 60)

    # فتح المتصفح تلقائياً على صفحة الـ Swagger
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "final.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(SRC_DIR)],
    )
