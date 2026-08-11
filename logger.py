import sys
import json
import logging
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """Formateador de logs en formato JSON estructurado."""
    def format(self, record):
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_object, ensure_ascii=False)

def get_logger(name: str = "ai_video_studio") -> logging.Logger:
    """Configura y retorna un logger estructurado en formato JSON."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    return logger
