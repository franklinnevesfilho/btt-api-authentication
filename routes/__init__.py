from .auth_router import auth_router
from .user_router import user_router
from .task_router import task_router

all_routers = [
     user_router,
     auth_router,
     task_router
]

__all__ = [
    all_routers
]