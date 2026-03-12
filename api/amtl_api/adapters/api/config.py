import gzip
import logging
import logging.handlers
import shutil
from logging import handlers
from os import remove
from sys import stdout

from .settings import LogConfig, Settings

api_settings: Settings = Settings()
log_config: LogConfig = LogConfig()


# log config
class StdFormatter(logging.Formatter):

    fmt = log_config.FORMAT

    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
              'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}

    def format(self, record):
        formatter = logging.Formatter(self.fmt, datefmt=log_config.DATE_FORMAT)
        if record.levelname:
            record.levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}\033[0m"
        if hasattr(record, "asctime") and record.asctime:
            record.asctime = f"{self.COLORS.get(record.levelname, '')}{record.asctime}\033[0m"

        return formatter.format(record)


log_format = logging.Formatter(log_config.FORMAT, datefmt=log_config.DATE_FORMAT)
logger = logging.getLogger(log_config.LOGGER_NAME)
logger.setLevel(log_config.LOGGING_LEVEL)


# file log handler
def namer(name):
    return "".join((name, ".gz"))


def rotator(source, dest):
    with open(source, 'rb') as f_in:
        with gzip.open(dest, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    remove(source)


fh = handlers.RotatingFileHandler(
    log_config.LOG_PATH,
    maxBytes=log_config.LOGGING_MAX_LOG_SIZE,
    backupCount=log_config.LOGGING_BACKUP_COUNT
)

fh.setFormatter(log_format)
fh.setLevel(log_config.LOGGING_LEVEL)
fh.rotator = rotator
fh.namer = namer
logger.addHandler(fh)

# stream handler
if api_settings.IS_DEBUG:
    sh = logging.StreamHandler(stream=stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(StdFormatter())
    logger.addHandler(sh)
    logger.warning(f"Debug mode: {api_settings.IS_DEBUG}")
else:
    logger.info(f"Debug mode: {api_settings.IS_DEBUG}")
