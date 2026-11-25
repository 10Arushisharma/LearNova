from fastapi import APIRouter
from app.api.v1 import auth, users, learning, gamification, quests, challenges, sandbox, mentor, projects, leaderboard, notifications, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["gamification"])
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(sandbox.router, prefix="/sandbox", tags=["sandbox"])
api_router.include_router(mentor.router, prefix="/mentor", tags=["mentor"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
