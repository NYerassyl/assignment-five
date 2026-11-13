from fastapi import FastAPI, Request
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse

from errors import DomainError
from routers import lessons, problems, users
from storage import store

DESCRIPTION = """
Educational FastAPI service for the WorldOfCodes REST API assignment.

It is independent from the production Express/PostgreSQL application and keeps
all data in memory. Restarting the process restores the seeded demo data.

## Demo authentication

Mutations and submissions read the `X-User-Id` header. Create a player first and use its returned ID. Unknown, missing or non-numeric headers are rejected.
"""

app = FastAPI()


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.get("/", tags=["meta"])
def service_index(request: Request):
    if "text/html" in request.headers.get("accept", ""):
        return FileResponse(Path(__file__).parent / "site" / "index.html")
    return {
        "service": "fastapi-backend",
        "storage": "in-memory",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health",
    }


@app.get("/api/health", tags=["meta"])
def health() -> dict:
    with store.lock:
        return {
            "status": "ok",
            "service": "fastapi-backend",
            "storage": "in-memory",
            "users": len(store.users),
            "lessons": len(store.lessons),
            "problems": len(store.problems),
            "submissions": len(store.submissions),
        }


app.include_router(users.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(lessons.progress_router, prefix="/api")
app.include_router(problems.router, prefix="/api")
app.include_router(problems.submissions_router, prefix="/api")
