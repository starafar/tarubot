from config import settings
import coloredlogs

coloredlogs.install(level=settings.log.level)
