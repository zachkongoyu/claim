from fastapi import FastAPI
import uvicorn

from claim.mcp.server.verification import mcp as verification_mcp

app = FastAPI(title="Medical Claims Validation API")

app.mount("/mcp", verification_mcp.sse_app())

@app.get("/")
async def root():
    return {"message": "Medical Claims Validation API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)