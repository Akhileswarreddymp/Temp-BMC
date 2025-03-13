from fastapi import FastAPI
from ddtrace import tracer
from ddtrace.contrib.asgi import TraceMiddleware
from authentication.models.api.otp_validation import SuccessResponse
from authentication.routers.user_verification import router as otp_route

app = FastAPI(
    docs_url="/docs",
    title="Partner App",
    description="Partner onboarding and authentication",
    openapi_url="/openapi.json",
)


app.add_middleware(TraceMiddleware, tracer=tracer)
app.include_router(otp_route)


@app.get("/",tags=["Health"])
async def read_root() -> dict:
    return SuccessResponse(
        message= "Successfully connected to the API"
    )
