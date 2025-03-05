from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routes import dashboard

# Initialize FastAPI application with a base path for API versioning
app = FastAPI(root_path="/apis/v1")

# Add session middleware to handle user sessions
# The secret key is used for signing the session cookies
app.add_middleware(SessionMiddleware, secret_key="!@#$%^&*()")

# Configure CORS (Cross-Origin Resource Sharing) settings
allow_all = ['*']  # Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,  # Allow all origins
    allow_credentials=True,   # Allow cookies to be included in requests
    allow_methods=allow_all,  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=allow_all   # Allow all HTTP headers
)

# Include routes from the dashboard module
app.include_router(dashboard.router)


@app.get("/health")
async def health():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: A simple message indicating the service is operational
    """
    return {"message": "OK"}