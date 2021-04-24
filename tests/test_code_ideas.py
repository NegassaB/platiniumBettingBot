import requests
import bs4 as bs

"""
they changed it, they fucking changed it.
Find a way to simply display the site on the channel or bot, don't save it, don't parse it, don't do anything to it.
Just simply get it and transfer it to the user of the bot.
"""


def result_spice():
    def pick_out(row):
        for pickings in row.find_all('td'):
            val = pickings.text.strip()
            if len(val) != 0:
                list_of_vals.append(val)
            else:
                print(val)

    sauce = requests.get("https://hsitoriiquebet.blogspot.com/")
    # sauce = requests.get("https://viiiiiptips.blogspot.com/")
    soup = bs.BeautifulSoup(sauce.content, 'html.parser')
    meaty_list = []
    list_of_keys = ["time", "teams", "odds", "win/lose", "country", "3ways", "correct_score"]
    list_of_vals = []
    table = soup.find("table")
    all_rows = table.find_all('tr')
    _, _ = all_rows.pop(0), all_rows.pop(-1)
    while len(all_rows) != 0:
        row1, row2 = all_rows.pop(0), all_rows.pop(0)
        pick_out(row1)
        pick_out(row2)
        print(list_of_vals)
        meaty_list.append(dict(zip(list_of_keys, list_of_vals)))
        list_of_vals.clear()
    print("================================================================================")
    print(meaty_list)
