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

class TransactionUpdate(BaseModel):
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        print(f"[SUCCESS] Created Project: {project.name}")
        return {"id": new_id, "message": "Project created successfully"}
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Creating Project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE projects SET name=?, client=?, status=?, budget=? WHERE id=?",
            (project.name, project.client, project.status, project.budget, project_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Project not found")
        
        conn.close()
        print(f"[UPDATE] Updated Project {project_id}")
        return {"message": "Project updated"}
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Updating Project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete related transactions first
        cursor.execute("DELETE FROM transactions WHERE project_id = ?", (project_id,))
        # Delete the project
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Project not found")
            
        conn.close()
        print(f"[DELETE] Deleted Project {project_id}")
        return {"message": "Project deleted"}
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Deleting Project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- TRANSACTION ENDPOINTS ---

@app.get("/api/projects/{project_id}/transactions")
def get_transactions(project_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE project_id = ?", (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[ERROR] Error Fetching Transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transactions")
def create_transaction(tx: TransactionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (project_id, description, amount, date) VALUES (?, ?, ?, ?)",
            (tx.project_id, tx.description, tx.amount, tx.date)
        )
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Added Transaction for Project {tx.project_id}")
        return {"message": "Transaction added"}
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Adding Transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/transactions/{tx_id}")
def update_transaction(tx_id: int, tx: TransactionUpdate):
    print(f"[UPDATE] Attempting to update Transaction {tx_id}...") 
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE transactions SET description=?, amount=?, date=? WHERE id=?",
            (tx.description, tx.amount, tx.date, tx_id)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            print(f"[WARN] Transaction {tx_id} not found")
            raise HTTPException(status_code=404, detail="Transaction not found")
            
        conn.close()
        print(f"[SUCCESS] Transaction {tx_id} Updated")
        return {"message": "Transaction updated"}
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Updating Transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/transactions/{tx_id}")
def delete_transaction(tx_id: int):
    print(f"[DELETE] Attempting to delete Transaction {tx_id}...") 
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            print(f"[WARN] Transaction {tx_id} not found")
            raise HTTPException(status_code=404, detail="Transaction not found")
            
        conn.close()
        print(f"[SUCCESS] Transaction {tx_id} Deleted")
        return {"message": "Transaction deleted"}
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        print(f"[ERROR] Error Deleting Transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)