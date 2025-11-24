from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api_constants import API_PORT, API_HOST, ALLOWED_ORIGINS
from routers import db, action

# Run on the port
def start_api():
    app = FastAPI()

    # Add routes
    app.include_router(db.router)
    app.include_router(action.router)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
    