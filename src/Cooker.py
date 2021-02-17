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

    def get_recipe(self):
        """
        doc:
        This method gets the necessary information from the provided url and creates the bs object necessary
        to parse the wep page.

        Desc:
        Attributes:
        Args:
        Notes:
        Returns:
        Raises:
        """
        sauce = requests.get(self.source_url)

    def cook_recipe(self):
        """
        doc:
        This method receives the created bs object and retrieves the necessary details.

        Desc:
        Attributes:
        Args:
        Notes:
        Returns:
        Raises:
        """
        pass
