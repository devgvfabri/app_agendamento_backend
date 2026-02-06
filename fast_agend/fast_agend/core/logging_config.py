import logging

import logging

def setup_logging():
    external_loggers = ["sqlalchemy.engine", "uvicorn", "uvicorn.access"]
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        force=True
    )

    for logger_name in external_loggers:
        logging.getLogger(logger_name).propagate = True