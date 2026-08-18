@echo off
cd /d "C:\Users\Venkatesh\Desktop\student support and learning platform\backend"
"C:\Users\Venkatesh\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt
"C:\Users\Venkatesh\AppData\Local\Programs\Python\Python314\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8001
