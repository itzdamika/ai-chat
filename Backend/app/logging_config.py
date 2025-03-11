import os
import sys
import logging
import structlog

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Create log formatters
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# Create handlers
file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setFormatter(file_formatter)  # ✅ Correct formatter

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(message)s"))  # ✅ Avoids structlog error

# Prevent adding multiple handlers
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],  # ✅ No duplicate handlers
    )

# Configure structlog (correct setup)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.KeyValueRenderer()  # ✅ Avoids ANSI issues in logs
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# ✅ Use structlog's logger
logger = structlog.get_logger()
