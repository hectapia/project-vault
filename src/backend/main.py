from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db_connection

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---

class TransactionCreate(BaseModel):
    project_id: int
    description: str
    amount: float
    date: str

class ProjectCreate(BaseModel):
    name: str
    client: str
    status: str
    budget: float

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Vault Backend Running"}

@app.get("/api/projects")
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/projects")
def create_project(project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO projects (name, client, status, budget) VALUES (?, ?, ?, ?)",
            (project.name, project.client, project.status, project.budget)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, "message": "Project created successfully"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE projects SET name=?, client=?, status=?, budget=? WHERE id=?",
        (project.name, project.client, project.status, project.budget, project_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Project updated"}

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete related transactions first
    cursor.execute("DELETE FROM transactions WHERE project_id = ?", (project_id,))
    # Delete the project
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    return {"message": "Project deleted"}

# --- TRANSACTION ENDPOINTS ---

@app.get("/api/projects/{project_id}/transactions")
def get_transactions(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE project_id = ?", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/transactions")
def create_transaction(tx: TransactionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (project_id, description, amount, date) VALUES (?, ?, ?, ?)",
        (tx.project_id, tx.description, tx.amount, tx.date)
    )
    conn.commit()
    conn.close()
    return {"message": "Transaction added"}

if __name__ == "__main__":
    import uvicorn
    # IMPORTANT: reload=True helps during dev, but remove for production
    uvicorn.run(app, host="127.0.0.1", port=8000)