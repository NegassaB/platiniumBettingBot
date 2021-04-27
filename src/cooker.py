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


class Chef():
    """
    todo:
        * chef module is the one that does the cooking, cooker module is the stove. Doesn't matter
            what you put on it, it will cook it. But it's the chef that decides what to cook, how to cook,
            what to add etc. Thus chef module is responsible for passing the ingredients (source urls),
            adding the necessary spices, getting the result, passing it onto the waiters to serve (waiter module)
    Chef [summary]
    """
    def __init__(self):
        pass


class Cooker():
    """
    doc:
    Cooker [summary]

    Returns:
        [type]: [description]
    """
    def __init__(self, source_url):
        """
        doc:
        The Cooker class that will be responsible for getting the content from
        the website.

        __init__: This is used to initialize the Cooker object with all the
        necessary attributes.

        Args:
            source_url (String): the url that will be used to garner the
            content from.
        """
        self.source_url = source_url

    def get_sauce(self):
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
            ConnectionError, Timeout, TooManyRedirects from the module
            requests.
        """
        try:
            self.sauce = requests.get(self.source_url)
            self.sauce.raise_for_status()
        except (
            exceptions.ConnectionError,
            exceptions.Timeout,
            exceptions.TooManyRedirects
        ) as e:
            logger.exception(f"exception hit -- {e}")

    def cook_sauce(self):
        """
        doc:
        cook_sauce: takes in the sauce created in get_sauce() & create
            bs object from it and retrieve the necessary details.

            When called, this method will take in the sauce created in
            get_sauce() and proceed to create a bs object from it and
            retrieve the necessary details. The way it does that is by getting
            the table from the bs object and then parsing all the rows out of
            that bs object into the 'all_rows' ResultSet object.
            From that it pops the 1st and last rows and proceeds to get into a
            while loop that will pop two rows at once and insert the data from
            those rows into a tuple that will contain them.

        Returns:
            [type]: [description]
        """
        self.soup = bs.BeautifulSoup(self.sauce.content, 'html.parser')
        # todo: perhaps return the entire table
        resp_table = self.soup.find("table")
        print(resp_table)
        all_tr = resp_table.find_all("tr")
        return resp_table
