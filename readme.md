# Time Management API & React UI

A simple employee time tracking system with FastAPI backend and React frontend. This project allows you to manage employees and their shifts.

---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React, Vite

---

## Setup Instructions

### Backend

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic pytest
```

3. Run the backend server:

```bash
uvicorn main:app --reload
```

The API will run at `http://localhost:8000`

Visit **Swagger UI** for interactive API docs:  
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Employees

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/employees/` | List all employees |
| POST | `/employees/` | Create a new employee |
| GET | `/employees/{employee_id}` | Get an employee by ID |
| PUT | `/employees/{employee_id}` | Update an employee |
| DELETE | `/employees/{employee_id}` | Delete an employee |

---

### Shifts

| Method | Endpoint                | Description |
|--------|-------------------------|-------------|
| POST | `/shifts/`              | Create a new shift for an employee |
| GET | `/shifts/{employee_id}` | List all shifts, filtered by `employee_id` |
| PUT | `/shifts/{shift_id}`    | Update a shift |
| DELETE | `/shifts/{shift_id}`    | Delete a shift |

---

## Example Requests

### 1. Create Employee

```bash
POST /employees/
Content-Type: application/json

{
  "name": "John Doe",
  "role": "Baker"
}
```

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "role": "Baker"
}
```

---

### 2. List Employees

```bash
GET /employees/
```

Response:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "role": "Baker"
  }
]
```

---

### 3. Create Shift

```bash
POST /shifts/
Content-Type: application/json

{
  "employee_id": 1,
  "start_time": "2025-11-17T08:00:00",
  "end_time": "2025-11-17T12:00:00",
  "shift_name": "Morning"
}
```

Response:

```json
{
  "id": 1,
  "employee_id": 1,
  "employee_name": "John Doe",
  "start_time": "2025-11-17T08:00:00",
  "end_time": "2025-11-17T12:00:00",
  "shift_name": "Morning"
}
```

---

### 4. List Shifts for an Employee

```bash
GET /shifts/?employee_id=1
```

Response:

```json
[
  {
    "id": 1,
    "employee_id": 1,
    "employee_name": "John Doe",
    "start_time": "2025-11-17T08:00:00",
    "end_time": "2025-11-17T12:00:00",
    "shift_name": "Morning"
  }
]
```

---

### 5. Update Shift

```bash
PUT /shifts/1
Content-Type: application/json

{
  "end_time": "2025-11-17T13:00:00"
}
```

Response:

```json
{
  "id": 1,
  "employee_id": 1,
  "employee_name": "John Doe",
  "start_time": "2025-11-17T08:00:00",
  "end_time": "2025-11-17T13:00:00",
  "shift_name": "Morning"
}
```

---

### 6. Delete Shift

```bash
DELETE /shifts/1
```

Response: **204 No Content**

---

## Testing

Run all tests:

```bash
pytest -q
```


---


## Notes

- SQLite is used as the database for simplicity.
- The frontend communicates with the backend via fetch API.
- Ensure CORS is enabled on FastAPI if frontend is served from a different port.

---

## Future Improvements

- Display existing shifts for each employee in the UI
- Inline error messages in the React form instead of alerts
- User authentication and authorization
- Persistent database storage beyond SQLite
- Dockerization

