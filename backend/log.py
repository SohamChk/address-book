import logging
from datetime import datetime

from backend.config import get_settings

settings = get_settings()
logging.basicConfig(format="[%(asctime)s]: %(message)s",
                        level=logging.INFO if int(settings.DEBUG) else logging.ERROR)

log = logging.getLogger('backend')

log_dict = {}
log_dict['request_id'] = ''
log_dict['endpoint'] = ''
log_dict['user'] = ''