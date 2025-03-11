import os
import sys
import logging
import structlog

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Basic logging configuration for console output
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(message)s"
)

def init_logging() -> None:
    """
    Configures structured logging with both console and file handlers.
    """
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(file_handler)
    
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Initialize logging immediately on import
init_logging()
logger = structlog.get_logger()
