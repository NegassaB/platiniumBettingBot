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
        [ ] - request.get the url data
        [ ] - get the sauce
        [ ] - gather all the tables from the sauce
        [ ] - gather all the rows
        [ ] - find a way to identify the td with the stars
        [ ] - count the number of star imgs inside the td with the stars
        [ ] - return the table
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
        This method fetches from the url provided using requests using the headers set.

        Desc:
            It gets the necessary information from the provided url via requests and the headers set.
            If successful it will updated the self.sauce object with requests.Response.
            If it fails it will raise the necessary status and exit.
        Attributes:
        Args:
            self
        Notes:
        Returns:

        Raises:
            ConnectionError, Timeout, TooManyRedirects from the module
            requests.
        """
        agent_str = "Mozilla/5.0 (Linux; Android 10; SM-A207F Build/QP1A.190711.020) " + \
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.82 Mobile Safari/537.36 OPT/2.9"
        req_headers = {
            "User-Agent": agent_str
        }
        try:
            self.sauce = requests.get(self.source_url, headers=req_headers)
            self.sauce.raise_for_status()
        except (
            exceptions.ConnectionError,
            exceptions.Timeout,
            exceptions.TooManyRedirects
        ) as e:
            logger.exception(f"exception hit -- {e}")

    def cook_sauce(self):
        """
        fix: this doesn't work for combo tips, crashes during the retrival of match, threeway, odds

        cook_sauce: creates beautiful soup object and parses the necessary details out of it.

        Desc: When called, this method will take in the sauce created in get_sauce() and
              proceed to create a beautiful soup object from it and parse all the tables found in the website.
              Lastly it returns all the tables found in sauce as a list of lists.

        Returns:
            [List]: named viptips_match_list that contains lists. Each list inside viptips_match_list
                    represents one match found in the website.
        """
        viptips_match_list = list()
        self.get_sauce()
        self.soup = bs.BeautifulSoup(self.sauce.content, 'html5lib')

        for table in self.soup.select('table'):
            rows = table.select('tr')
            league = rows[0].get_text(strip=True)
            match, threeway, odds = [td.get_text(strip=True) for td in rows[1].select('td')]
            rate_star = " ".join([":star:"] * len(rows[2].select('img')))
            _, final_score = [td.get_text(strip=True) for td in rows[3].select('td')]
            viptips_match_list.append(
                [league, match, threeway, odds, rate_star, final_score]
            )
        return viptips_match_list
