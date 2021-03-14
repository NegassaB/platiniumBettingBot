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
    todo:
        1.

    doc:
    Cooker [summary]

    Returns:
        [type]: [description]
    """
    def __init__(self, source_url):
        """
        docs:
        The Cooker class that will be responsible for getting the content from
        the website.

        __init__: This is used to initialize the Cooker object with all the
        necessary attributes.

        Args:
            source_url (String): the url that will be used to garner the
            content from.
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
            ConnectionError, Timeout, TooManyRedirects from the module
            requests.
        """
        try:
            self.sauce = requests.get(self.source_url)
            self.sauce.raise_for_status()
        except (exceptions.ConnectionError, exceptions.Timeout, exceptions.TooManyRedirects) as e:
            logger.exception(f"exception hit -- {e}")

    def cook_recipe(self):
        """
        doc:
        cook_recipe: takes in the sauce created in get_recipe() & create
            bs object from it and retrieve the necessary details.

            When called, this method will take in the sauce created in
            get_recipe() and proceed to create a bs object from it and
            retrieve the necessary details. The way it does that is by getting
            the table from the bs object and then parsing all the rows out of
            that bs object into the 'all_rows' ResultSet object.
            From that it pops the 1st and last rows and proceeds to get into a
            while loop that will pop two rows at once and insert the data from
            those rows into a tuple that will contain them.

        Returns:
            [type]: [description]
        """
        """
        """
        def pick_out(row):
            """
            This methods is used to pick out texts from the row. These include
            the tiem, teams and odds.

            Args:
                row (NavigableString): The row that contains the texts
                that are required.

            Returns:
                list: a list_of_vals populated with the values in each row.
            """
            for pickings in row.find_all('td'):
                val = pickings.text.strip()
                if len(val) != 0:
                    list_of_vals.append(pickings.text.strip())

        self.soup = bs.BeautifulSoup(self.sauce.content, 'html.parser')
        self.meaty_list = []
        list_of_keys = ["time", "teams", "odds", "country", "3ways"]
        list_of_vals = []
        table = self.soup.find("table")
        all_rows = table.find_all('tr')
        _, _ = all_rows.pop(0), all_rows.pop(-1)
        while len(all_rows) != 0:
            row1, row2 = all_rows.pop(0), all_rows.pop(0)
            pick_out(row1)
            pick_out(row2)
            self.meaty_list.append(dict(zip(list_of_keys, list_of_vals)))
            list_of_vals.clear()

    @classmethod
    def connect(none):
        pass
