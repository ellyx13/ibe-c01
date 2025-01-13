
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from modules.v1.users.routers import router as users_router
from contextlib import asynccontextmanager
from modules.v1.users.services import create_default_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start commands when the app starts
    await create_default_admin()
    yield
    # Start commands when the app stops


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)  

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "My Auth API",
        version = "1.0",
        description = "An API with an Authorize Button",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        methods = [method.lower() for method in getattr(route, "methods")]
        for method in methods:
            openapi_schema["paths"][path][method]["security"] = [
                {
                    "Bearer Auth": []
                }
            ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  