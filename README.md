# Event Registration API

A simple backend where students register for an event and organizers view the registrations. Built with Python, FastAPI and SQLite.

## How to run

1. Install the libraries:
   pip install fastapi uvicorn "pydantic[email]"
2. Start the server:
   uvicorn main:app --reload
3. Open http://127.0.0.1:8000/docs to test the API in the browser.

## Endpoints

| Method | URL | What it does | Responses |
|---|---|---|---|
| POST | /register | Registers a student (name, email, optional college) | 201 success, 409 duplicate email, 409 event full, 422 invalid data |
| GET | /registrations | Lists all registrations | 200 |
| GET | /registrations/{id} | Shows one registration | 200, 404 not found |

Example request for POST /register:

{
  "name": "Priya",
  "email": "priya@gmail.com",
  "college": "ABC College"
}

## Design decisions

- **Why SQLite:** It stores the whole database in a single file and needs no installation, since Python includes it.
- **How duplicates are handled:** The email column is marked UNIQUE, so SQLite raises an IntegrityError when the same email is inserted twice. The code catches this error and returns 409 "Already registered".
- **How the capacity limit works:** Before inserting, the code counts the existing registrations. If the count has reached MAX_CAPACITY (50), it returns 409 "Event Is Full" and nothing is inserted.

## Known limitation

If two students register at the exact same moment for the last seat, both could get in, because the seat count and the insert are separate steps. A fix would be to do them together safely in one database transaction.
