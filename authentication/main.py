from fastapi import FastAPI
from ddtrace import tracer
from ddtrace.contrib.asgi import TraceMiddleware


app = FastAPI(
    docs_url="/docs",
    title="Practice Project",
    description="Practice project for setting up a project",
    openapi_url="/openapi.json",
    root_path="/api",
)


app.add_middleware(TraceMiddleware, tracer=tracer, tags={"service": "practice-api"})

@app.get("/")
async def read_root() -> dict:
    return {"message": "Successfully connected to the API"}