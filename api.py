from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from your Local Python Backend!"}

if __name__ == "__main__":
    # We run on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)