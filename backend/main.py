import io
import csv
import redis.asyncio as redis_client
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# --- הגדרות אבטחה ו-JWT ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "my_super_secret_key_for_hit_project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- מודלים של בסיס הנתונים ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

class Pizza(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    size: str
    price: float
    delivery_method: str  # "pickup" or "delivery"
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class PizzaCreate(SQLModel):
    name: str
    size: str
    price: float
    delivery_method: str
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

# --- פונקציות עזר ---
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# --- חיבור לבסיס הנתונים ---
sqlite_url = "sqlite:///./pizza.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- הקמת האפליקציה ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- נתיבי משתמשים (Auth) ---
@app.post("/signup")
def signup(username: str, password: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=username, hashed_password=hash_password(password))
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- נתיבי פיצה (Pizza API) ---
@app.get("/items", response_model=List[Pizza])
def read_pizzas(session: Session = Depends(get_session)):
    pizzas = session.exec(select(Pizza)).all()
    return pizzas

@app.post("/items", response_model=Pizza)
async def create_pizza(
    pizza_in: PizzaCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    db_pizza = Pizza.from_orm(pizza_in)
    session.add(db_pizza)
    session.commit()
    session.refresh(db_pizza)
    
    try:
        r = redis_client.from_url("redis://redis:6379")
        await r.rpush("pizza_tasks", f"Order {db_pizza.id}: {db_pizza.name} for {current_user}")
        await r.close()
    except Exception as e:
        print(f"Redis Error: {e}")
    
    return db_pizza

# --- Enhancement: CSV Export ---
@app.get("/export-csv")
async def export_pizzas_csv(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    pizzas = session.exec(select(Pizza)).all()
    
    output = io.StringIO()
    output.write("sep=,\n") # הוראה לאקסל להשתמש בפסיק
    writer = csv.writer(output)
    
    # כותרות באנגלית בלבד
    writer.writerow(["Order_ID", "Pizza_Name", "Size", "Price_ILS", "Method", "City", "Address", "Phone"])
    
    method_map = {"איסוף עצמי": "Pickup", "משלוח": "Delivery"}
    
    for p in pizzas:
        method = method_map.get(p.delivery_method, p.delivery_method)
        writer.writerow([
            p.id, p.name, p.size, p.price, method,
            p.city or "-", p.address or "-", p.phone or "-"
        ])
    
    content = output.getvalue().encode('utf-8-sig')
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=pizza_report.csv"}
    )