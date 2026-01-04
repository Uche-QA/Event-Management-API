# Event Management & RSVP System (API)

A robust FastAPI-based backend for managing events and guest lists. This system handles everything from image uploads for event flyers to automated guest list management with cascading deletes.

## 🎯 Project Purpose
This project was built to demonstrate backend API design, file handling, data integrity, and event-based relationships commonly found in real-world SaaS applications.


## 🚀 Features
* **Full CRUD Events:** Create, Read (List/Search/Filter), Update (Partial), and Delete events.
* **Image Handling:** Unique filename generation using UUIDs and physical file cleanup on deletion.
* **RSVP System:** Link guests to specific events with automated cleanup (Cascading Deletes).
* **Data Validation:** Strict date handling and Pydantic schema enforcement.
* **Scalable Listing:** Built-in pagination and case-insensitive search.

## 🛠️ Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic v2
* **Configuration:** Pydantic Settings & Dotenv



## 1. Environment Setup
### Clone the repository
```bash
git clone <your-repo-url>
cd RSVP
```
### Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
## 2. Installation 
# Install all dependencies from the requirements file
```bash
pip install -r requirements.txt
```
## 3. Configuration  
Create a .env file in the root directory and add your credentials:

## 4. Run the Application
```bash
uvicorn app.main:app --reload
```
## 🔌 API Reference

### Events
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /events/ | Create event with flyer upload |
| GET | /events/ | List events (?title, ?skip, ?limit) |
| GET | /events/{id} | Retrieve event details |
| PATCH | /events/{id} | Partially update an event |
| DELETE | /events/{id} | Delete event and flyer |

### RSVPs
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /events/{id}/rsvp | Add guest to event |
| GET | /events/{id}/rsvps | List event guests |
| DELETE | /rsvps/{id} | Remove guest |


📖 Interactive Documentation

Once the server is running, the following documentation is automatically generated:

Swagger UI: http://127.0.0.1:8000/docs - Great for testing endpoints.

ReDoc: http://127.0.0.1:8000/redoc - Clean, searchable documentation.


🗄️ Project Structure
RSVP/
├── uploads/          # Physical storage for event flyers
├── config.py         # Pydantic Settings & .env loading
├── database.py       # SQLAlchemy engine and session setup
├── main.py           # FastAPI routes and app initialization
├── models.py         # Database table definitions
├── schemas.py        # Pydantic data validation models
├── requirements.txt  # Project dependencies
└── .env              # Local environment variables (not in git)