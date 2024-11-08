from library.presentors.rest.config import RestConfig
from library.presentors.rest.service import RestService

config = RestConfig()
app = RestService(config=config).create_application()
