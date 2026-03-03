"""Logging configuration."""

import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","request_id":"%(request_id)s"}',
    )
