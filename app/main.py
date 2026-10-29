from app.api.routes import main
from app.core.config import config
from app.core.exception import CustomException
from app.core.lifespan import lifespan
from app.middlewares.main import middleware
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI(
    title=f"{config.SERVICE_NAME} RESTful API",
    description=f"RESTful API for {config.SERVICE_NAME}",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    RequestValidationError, middleware.request_validation_exception_handler
)
app.add_exception_handler(CustomException, middleware.custom_exception_handler)
app.add_exception_handler(Exception, middleware.unhandled_exception_handler)
app.include_router(main.router, responses={422: {}})


@app.get("/", tags=["Defaults"])
async def root():
    app_info = {"name": f"Welcome to {config.SERVICE_NAME} RESTful API"}

    return app_info
