# Time Management API & React UI

A simple employee time tracking system with FastAPI backend and React frontend. This project allows you to manage employees and their shifts.

---

## Features

- CRUD for Employees
- Add Shifts for Employees
- Validations for shift overlaps (backend)
- Interactive React UI to add employees and shifts

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
pip install fastapi uvicorn sqlalchemy pydantic
```

3. Run the backend server:

```bash
uvicorn main:app --reload
```

The API will run at `http://localhost:8000`

---

### Frontend

1. Make sure Node.js and npm are installed:

```bash
node -v
npm -v
```

2. Navigate to the frontend directory:

```bash
cd time-tracking-ui
```

3. Install dependencies:

```bash
npm install
```

4. Start the frontend server:

```bash
npm run dev
```

The React app will run at `http://localhost:5173`

---

## API Endpoints

### Employees

- `GET /employees/` - List all employees
- `POST /employees/` - Create a new employee
- `GET /employees/{id}` - Get employee by ID
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Delete employee

### Shifts

- `GET /shifts/` - List all shifts
- `POST /shifts/` - Create a new shift for an employee
- `DELETE /shifts/{id}` - Delete a shift

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

