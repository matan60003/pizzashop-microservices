import asyncio
import redis.asyncio as redis
import random

# הגדרות חיבור ל-Redis בתוך דוקר
REDIS_URL = "redis://redis:6379"

async def mock_processing(task_id: str):
    """סימולציה של עיבוד משימה עם סיכוי לשגיאה לצורך בדיקת Retries"""
    # הוספת flush=True כדי לוודא שהלוג מופיע בטרמינל מיד
    print(f"--- [Worker] Starting task: {task_id} ---", flush=True)
    
    if random.random() < 0.2:  # 20% סיכוי לשגיאה
        raise Exception("Temporary Processing Failure!")
    
    await asyncio.sleep(2)  # סימולציה של עבודה
    print(f"--- [Worker] Task {task_id} Completed Successfully! ---", flush=True)

async def worker():
    # יצירת חיבור ל-Redis
    r = redis.from_url(REDIS_URL)
    print("Worker is online. Waiting for pizza tasks in Redis...", flush=True)
    
    try:
        while True:
            # שליפת משימה מהתור ב-Redis (Blocking Pop)
            task = await r.blpop("pizza_tasks", timeout=5)
            
            if task:
                _, task_data = task
                task_str = task_data.decode("utf-8")
                
                # מנגנון Retries בסיסי
                for attempt in range(3):
                    try:
                        await mock_processing(task_str)
                        break 
                    except Exception as e:
                        print(f"--- [Worker] Attempt {attempt + 1} failed: {e}. Retrying... ---", flush=True)
                        await asyncio.sleep(1)
    finally:
        await r.close()

if __name__ == "__main__":
    asyncio.run(worker())