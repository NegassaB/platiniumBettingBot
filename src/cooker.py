import bs4 as bs
import requests
from requests import exceptions
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
        The Cooker class that will be responsible for getting the content from the website.

        Desc:
        Attributes:
        Args:
            self
            source_url:- the url that will be used to garner the content from.
        Notes:
        Returns:
        Raises:
        """
        self.source_url = source_url

    def get_recipe(self):
        """
        doc:
        This method fetches from the url provided using requests.

        Desc:
            It gets the necessary information from the provided url.
        Attributes:
        Args:
            self
        Notes:
        Returns:

        Raises:
            ConnectionError, Timeout, TooManyRedirects from the module requests.
        """
        try:
            self.sauce = requests.get(self.source_url)
            self.sauce.raise_for_status()
        except (exceptions.ConnectionError, exceptions.Timeout, exceptions.TooManyRedirects) as e:
            logger.exception(f"exception hit -- {e}")

    def cook_recipe(self):
        """
        todo:
            1. table is a ResultSet, extract data from it according to the td & tr
            2. find a way to get the data by row
            3. save that to db

        doc:
            takes in the sauce created in get_recipe() & create bs object from it and retrieve the necessary details.

        Desc:
            When called, this method will take in the sauce created in get_recipe() and proceed to create
            a bs object from it and retrieve the necessary details.
        Attributes:
        Args:
            self
        Notes:
        Returns:
        Raises:
        """
        self.soup = bs.BeautifulSoup(self.sauce.content, 'html.parser')
        table = self.soup.find("table")
        return table
