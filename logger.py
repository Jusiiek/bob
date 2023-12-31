import logging


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'OK': '\033[92m',
        'INFO': '\033[0m'
    }
    RESET_CODE = '\033[0m'

    def format(self, record):
        log_msg = super().format(record)
        return f"{self.COLOR_CODES.get(record.levelname, '')}{log_msg}{self.RESET_CODE}"


logger = logging.getLogger('bob')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = ColoredFormatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
