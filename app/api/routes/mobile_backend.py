"""Composed routes for mobile backend modules."""

from fastapi import APIRouter

from app.mobile.admin.routes import router as admin_router
from app.mobile.auth.routes import router as auth_router
from app.mobile.chat.routes import router as chat_router
from app.mobile.media.routes import router as media_router
from app.mobile.profile.routes import router as profile_router
from app.mobile.push.routes import router as push_router
from app.mobile.social.routes import router as social_router
from app.mobile.sync.routes import router as sync_router

router = APIRouter(tags=["mobile-backend"])
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(social_router)
router.include_router(chat_router)
router.include_router(push_router)
router.include_router(sync_router)
router.include_router(media_router)
router.include_router(admin_router)
