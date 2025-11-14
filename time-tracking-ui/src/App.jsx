import React, { useState, useEffect } from "react";

export default function App() {
  const [employees, setEmployees] = useState([]);
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);

  const [shiftEmployeeId, setShiftEmployeeId] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const API_URL = "http://localhost:8000";

  // Fetch all employees
  const fetchEmployees = async () => {
    try {
      const res = await fetch(`${API_URL}/employees/`);
      const data = await res.json();
      setEmployees(data);
    } catch (err) {
      console.error("Error fetching employees", err);
    }
  };

  // Add a new employee
  const addEmployee = async () => {
    if (!name || !role) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/employees/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, role }),
      });
      if (!res.ok) throw new Error("Failed to create employee");
      const newEmployee = await res.json();
      setEmployees((prev) => [...prev, newEmployee]);
      setName("");
      setRole("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Add a new shift
  const addShift = async () => {
  if (!shiftEmployeeId || !startTime || !endTime) return;
  setLoading(true);
  try {
    const res = await fetch(`${API_URL}/shifts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        employee_id: parseInt(shiftEmployeeId),
        start_time: startTime,
        end_time: endTime,
      }),
    });

    const data = await res.json(); // <-- parse response

    if (!res.ok) {
      // If backend returned an error, show it
      alert(`Error adding shift: ${data.detail || JSON.stringify(data)}`);
      return;
    }

    alert("Shift added successfully!");
    setShiftEmployeeId("");
    setStartTime("");
    setEndTime("");
  } catch (err) {
    console.error(err);
    alert(`Error adding shift: ${err.message}`);
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    fetchEmployees();
  }, []);

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h1>Employee Manager</h1>

      {/* Add Employee Form */}
      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ marginRight: "0.5rem" }}
        />
        <input
          type="text"
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{ marginRight: "0.5rem" }}
        />
        <button onClick={addEmployee} disabled={loading}>
          {loading ? "Adding..." : "Add Employee"}
        </button>
      </div>

      {/* Add Shift Form */}
      <div style={{ marginBottom: "1rem" }}>
        <select value={shiftEmployeeId} onChange={(e) => setShiftEmployeeId(e.target.value)} style={{ marginRight: "0.5rem" }}>
          <option value="">Select Employee</option>
          {employees.map((emp) => (
            <option key={emp.id} value={emp.id}>{emp.name}</option>
          ))}
        </select>
        <input
          type="datetime-local"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          style={{ marginRight: "0.5rem" }}
        />
        <input
          type="datetime-local"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          style={{ marginRight: "0.5rem" }}
        />
        <button onClick={addShift} disabled={loading}>
          {loading ? "Adding..." : "Add Shift"}
        </button>
      </div>

      {/* Employee List */}
      <ul>
        {employees.map((emp) => (
          <li key={emp.id}>
            {emp.name} ({emp.role})
          </li>
        ))}
      </ul>
    </div>
  );
}
