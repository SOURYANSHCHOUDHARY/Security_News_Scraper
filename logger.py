import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levename)s -%(message)s"
)

logger = logging.getLogger(__name__)