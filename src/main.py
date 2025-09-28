import uvicorn

from common import create_fastapi_app
from detector.detector_service_initializer import DetectorServiceInitializer
from detector.endpoint import main_router
from detector.doc import Tags

app = create_fastapi_app(
    initializer=DetectorServiceInitializer,
    title="Auto Analyzer",
    description="Automated analyzing service",
    version="0.1.0",
    team_name="core",
    team_url="https://invalid-address.ee",
    openapi_tags=Tags.get_docs(),
)

# Service routes
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ws="none", reload=False, log_level="debug")
