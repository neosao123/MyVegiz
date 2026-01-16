
Folder Structure

app/
├── main.py                  👉 App entry point (starts FastAPI)
│
├── core/
│   └── config.py            👉 App configuration (DB URL, secrets)
│
├── db/
│   ├── base.py              👉 SQLAlchemy Base (table registry)
│   └── session.py           👉 Database connection/session
│
├── models/
│   ├── __init__.py
│   └── user.py              👉 Database table definition
│
├── schemas/
│   └── user.py              👉 Request/Response validation (Pydantic)
│
├── services/
│   └── user_service.py      👉 Business logic (DB operations)
│
├── api/
│   ├── dependencies.py      👉 Shared dependencies (DB session)
│   └── v1/
│       ├── router.py        👉 API version router
│       └── routes/
│           └── users.py     👉 User APIs (POST, GET)






HOW A REQUEST FLOWS 

Example: POST /api/v1/users

Postman / Browser
        ↓
users.py (API route)
        ↓
dependencies.py (DB session)
        ↓
user_service.py (logic)
        ↓
models/user.py (table)
        ↓
PostgreSQL
        ↑
UserResponse (schema)





Layer	    What it does

models	 > Database tables
schemas	 > API input/output
services > Business logic
routes	 > HTTP endpoints
db	 > Database connection
core	 > Configuration
main.py	 > App startup