from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

ALL_ROUTERS = (auth_router, users_router,)
