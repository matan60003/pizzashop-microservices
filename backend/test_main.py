from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_read_home():
    # בדיקה שהעמוד הראשי עובד
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Pizza Shop API!"}

def test_get_items():
    # בדיקה שניתן לקבל את רשימת הפיצות
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_create_pizza():
    # בדיקה של הוספת פיצה חדשה (POST)
    new_pizza = {
        "name": "Fungi",
        "size": "Small",
        "toppings": ["Mushrooms"]
    }
    response = client.post("/items", json=new_pizza)
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Fungi"

    def test_export_csv_unauthorized():
    # בדיקה שאי אפשר להוציא CSV בלי להתחבר
    response = client.get("/export-csv")
    assert response.status_code == 401