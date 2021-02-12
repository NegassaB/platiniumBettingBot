import bs4 as bs
import requests
import logging

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class Cooker():
    """
    doc:
        quick summary.

    Desc:
    Attributes:
    Args:
    Notes:
    Returns:
    Raises:
    """
    def __init__(self, source_url):
        """
        doc:
        quick summary.

        Desc:
        Attributes:
        Args:
        Notes:
        Returns:
        Raises:
        """
        self.source_url = source_url
