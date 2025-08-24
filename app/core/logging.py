"""
Модуль для настройки логирования.
"""
import logging
import sys


def setup_logging():
    """Настраивает базовую конфигурацию логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s в %(module)s.%(funcName)s: %(message)s",
        stream=sys.stdout,
    )
