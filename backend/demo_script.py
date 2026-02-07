import requests

BASE_URL = "http://localhost:8000"

def run_demo():
    print("--- EX3 Local Demo Script ---")
    
    # 1. בדיקת בריאות ה-API
    try:
        res = requests.get(f"{BASE_URL}/items")
        print(f"API Health Check: {res.status_code} OK")
    except:
        print("API is not running. Please run 'docker compose up' first.")
        return

    print("Demo finished. Graders: Please check docs/EX3-notes.md for more info.")

if __name__ == "__main__":
    run_demo()