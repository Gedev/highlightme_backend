import logging


class IgnoreMtimeFilter(logging.Filter):
    def filter(self, record):
        return 'first seen with mtime' not in record.getMessage()