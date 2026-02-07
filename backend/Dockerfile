# 1. באיזו מערכת הפעלה להשתמש? פייתון גרסה 3.9
FROM python:3.9-slim

# 2. הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# 3. העתקת קובץ הדרישות והתקנתן
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. העתקת כל שאר הקבצים (הקוד שלנו) לתוך הקונטיינר
COPY . .

# 5. הפקודה שתריץ את האפליקציה כשהקונטיינר עולה
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]