from fastapi import FastAPI

app = FastAPI()

@app.get("/msg")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.0", port=8000, log_level="info", reload=True)