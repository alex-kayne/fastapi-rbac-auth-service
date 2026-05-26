from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.business import router as business_router
from app.routers.access import router as access_router

ALL_ROUTERS = (auth_router, users_router, business_router, access_router,)
