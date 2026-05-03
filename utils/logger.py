# utils/logger.py - Logging setup for Zecpath AI system activities.

import logging
import os

def setup_logger():
    """
    Setup logging configuration. Logs are written to ai_logs.log at the project root.
    """
    logger = logging.getLogger("zecpath_ai")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if logger is imported multiple times
    if not logger.handlers:
        # Save logs to file
        log_file = "ai_logs.log"
        handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Log format containing timestamp, log level, and message content
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Also print warning/error messages to stdout for visibility
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

logger = setup_logger()
