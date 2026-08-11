import json
import logging
from logger import get_logger, JSONFormatter

def test_json_formatter():
    formatter = JSONFormatter()
    record = logging.LogRecord("test", logging.INFO, "path", 10, "Mensaje de prueba", (), None)
    formatted = formatter.format(record)
    
    data = json.loads(formatted)
    assert data["level"] == "INFO"
    assert data["message"] == "Mensaje de prueba"
    assert "timestamp" in data

def test_get_logger():
    logger = get_logger("test_module")
    assert logger.name == "test_module"
    assert len(logger.handlers) >= 1
