from fastapi import FastAPI
import uvicorn

from api.adjudication import router as adjudication_router
from api.care_coordination import router as care_coordination_router
from api.coding_translator import router as coding_translator_router
from api.fraud_detection import router as fraud_detection_router
from api.prior_auth import router as prior_auth_router
from api.synthetic_data import router as synthetic_data_router


app = FastAPI(title="Medical Claims Validation API")

app.include_router(adjudication_router)
app.include_router(prior_auth_router)
app.include_router(coding_translator_router)
app.include_router(fraud_detection_router)
app.include_router(synthetic_data_router)
app.include_router(care_coordination_router)

@app.get("/")
async def root():
    return {"message": "Medical Claims Validation API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)