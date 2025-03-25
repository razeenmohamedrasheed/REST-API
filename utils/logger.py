import logging

# Logger configuration
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)  # Set logging level

# Create handlers
file_handler = logging.FileHandler("app.log")  # Log to a file
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()  # Log to console
console_handler.setLevel(logging.INFO)

# Create log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
