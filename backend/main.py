import uvicorn
from src.config import settings
from src import app

print(settings)
if __name__ == "__main__":
    uvicorn.run(
        "src:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT
    )
