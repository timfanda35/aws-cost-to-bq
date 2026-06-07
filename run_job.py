import logging
import os
import sys

from dotenv import load_dotenv
load_dotenv()

from src.log import configure_logging
from src.pipeline import run_pipeline

configure_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    partition = os.environ.get("PARTITION") or None

    logger.info("job.started", extra={
        "log_event": "job.started",
        "partition": partition,
    })

    try:
        result = run_pipeline(partition=partition)
        logger.info("job.complete", extra={
            "log_event": "job.complete",
            "run_id": result.get("run_id"),
        })
        sys.exit(0)
    except Exception as exc:
        logger.error("job.failed", extra={
            "log_event": "job.failed",
            "error": str(exc),
        }, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
