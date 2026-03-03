"""Top-level API router."""

from fastapi import APIRouter

from app.api.routes.analytics import router as analytics_router
from app.api.routes.advanced import router as advanced_router
from app.api.routes.audit import router as audit_router
from app.api.routes.experiments import router as experiments_router
from app.api.routes.future import router as future_router
from app.api.routes.wellness import router as wellness_router
from app.api.routes.voice_clone import router as voice_clone_router
from app.api.routes.video import router as video_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.quantum import router as quantum_router
from app.api.routes.federated import router as federated_router
from app.api.routes.events import router as events_router
from app.api.routes.final_meta import router as final_meta_router
from app.api.routes.ultimate import router as ultimate_router
from app.api.routes.hundred import router as hundred_router
from app.api.routes.beyond import router as beyond_router
from app.api.routes.meta_transcendence import router as meta_transcendence_router
from app.api.routes.everything import router as everything_router
from app.api.routes.post_singularity import router as post_singularity_router
from app.api.routes.transcendent import router as transcendent_router
from app.api.routes.graph import router as graph_router
from app.api.routes.realtime import router as realtime_router
from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.projects import router as projects_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.teams import router as teams_router
from app.api.routes.mobile_backend import router as mobile_backend_router
from app.api.routes.platforms import router as platforms_router
from app.api.routes.enterprise import router as enterprise_router
from app.api.routes.mega import router as mega_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(projects_router)
api_router.include_router(tasks_router)
api_router.include_router(teams_router)
api_router.include_router(notifications_router)
api_router.include_router(analytics_router)
api_router.include_router(health_router)

api_router.include_router(graph_router)
api_router.include_router(audit_router)
api_router.include_router(experiments_router)
api_router.include_router(realtime_router)

api_router.include_router(future_router)

api_router.include_router(federated_router)
api_router.include_router(voice_clone_router)
api_router.include_router(video_router)
api_router.include_router(wellness_router)
api_router.include_router(quantum_router)
api_router.include_router(recommendations_router)
api_router.include_router(events_router)

api_router.include_router(advanced_router)

api_router.include_router(post_singularity_router)

api_router.include_router(transcendent_router)

api_router.include_router(everything_router)

api_router.include_router(final_meta_router)

api_router.include_router(ultimate_router)
api_router.include_router(hundred_router)
api_router.include_router(beyond_router)
api_router.include_router(meta_transcendence_router)
api_router.include_router(mobile_backend_router)
api_router.include_router(platforms_router)
api_router.include_router(enterprise_router)
api_router.include_router(mega_router)
