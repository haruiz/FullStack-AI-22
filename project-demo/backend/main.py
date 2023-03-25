import uvicorn
import os

if __name__ == "__main__":
    print(f"Starting server...{os.environ.get('PORT')}")
    uvicorn.run(
        "api:app", host="0.0.0.0", reload=False, port=int(os.environ.get("PORT", 8080))
    )  # run the fastapi app
