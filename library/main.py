from library.config import Config
from library.presentors.rest.service import get_fastapi_app

config = Config()
app = get_fastapi_app(config=config)
