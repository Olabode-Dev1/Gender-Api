from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx

app = FastAPI()

# Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/classify")
async def classify(name: str = Query(...)):
    
    # Check empty name
    if not name.strip():
        return {
            "status": "error",
            "message": "Missing or empty name parameter"
        }

    # Call Genderize API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.genderize.io",
                params={"name": name}
            )
            data = response.json()
    except:
        return {
            "status": "error",
            "message": "Upstream service failure"
        }

    gender = data.get("gender")
    probability = data.get("probability")
    count = data.get("count")

    # Edge case
    if gender is None or count == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    # Confidence logic
    is_confident = probability >= 0.7 and count >= 100

    # Return final response
    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": count,
            "is_confident": is_confident,
            "processed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    }
