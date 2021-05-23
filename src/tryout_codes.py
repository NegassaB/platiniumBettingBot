import pickle
import unicodedata
import bs4 as bs
from peewee import ImproperlyConfigured
import requests
import datetime
import pytz

AA_TIMEZONE = pytz.timezone('Africa/Addis_Ababa')
right_now = datetime.datetime.now(tz=AA_TIMEZONE)
print(right_now)

v_file = open('data/pickled_data/pickled_viptips.xyz', 'rb')
v_pickled = pickle.load(v_file)
h_file = open('data/pickled_data/pickled_history.xyz', 'rb')
h_pickled = pickle.load(h_file)

viptips = bs.BeautifulSoup(v_pickled.content, "html5lib")
history = bs.BeautifulSoup(h_pickled.content, "html5lib")

# actual_vip_site = requests.get("https://xxviptips.blogspot.com/")
# actual_vip_sauce = bs.BeautifulSoup(actual_vip_site.content, "html5lib")
table_data = []

for table in history.select("table", limit=12):
    print(table)
# for table in actual_vip_sauce.select("table"):
# for table in viptips.select("table"):
#     print(table)
    rows = table.select("tr")
    league = unicodedata.normalize("NFKD", rows[0].get_text(strip=True))
    match, info1, info2 = [unicodedata.normalize("NFKD", td.get_text(strip=True)) for td in rows[1].select("td")]
    # for td in rows[1].select('td'):
    #     print(td.get_text(strip=True))
    rate_star = " ".join(["⭐️"] * len(rows[2].select("img")))
    _, final_score = [unicodedata.normalize("NFKD", td.get_text(strip=True)) for td in rows[3].select('td')]
    # final_score_title, final_score = [
    #     "no results yet" if td.get_text(strip=True) == "" else td.get_text(strip=True) for td in rows[3].select('td')
    # ]
    # table_data.append(
    #     {"league": league, "match": match, "info1": info1, "info2": info2, "rate_star": rate_star, "final_score": final_score}
    # )
    table_data.append([league, match, info1, info2, rate_star, final_score])

    # print(f"{league}, {match}, {info1}, {info2}, {rate_star}, {final_score_title} -- {final_score}")

print(f"table data is -- {table_data}")

for match in table_data:
    print(match)
    temp = match.pop()
    if "\xa0" in temp:
        print(temp)

# print(markdown_strings.table_from_rows([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]))

# match_table = markdown_strings.table_row(
#     ["league & time", "match", "threeway", "odds", "rating", "final result"]
# )
match_table = "**League & Time | Match | Threeway | Odds | Rating | Final result**"
separator = "|——————————————————————-—————————-—|"
match_table = "".join([match_table, "\n", separator])
# match_table = "".join([match_table, "\n", markdown_strings.table_delimiter_row(6, column_lengths=[20, 20, 10, 10, 30, 5])])
for match in table_data:
    match_table = "".join([match_table, "\n", "```", str(match), ", ", "```"])

# match_table = ["".join([match_table, "\n", markdown_strings.table_row(match)]) for match in table_data]
print(f"{match_table}")
match_table = None

# for match in table_data:
#     for match_detail in match:
#         if "\xa0" in match_detail:
#             match_detail = unicodedata.normalize('NFKD', match_detail)
#     match_table = "".join([match_table, "\n", markdown_strings.table_row(match)])
#         # if unicodedata.is_normalized('NFD', match_detail):
#         #     print(match_detail)
#             # new_match_detail = unicodedata.normalize("\xa0", match_detail)
#             # print(new_match_detail)


# markdown_strings.header("main title", 1)

# table = markdown_strings.table_row(["league", "match", "threeway", "odds", "rating", "final result"])
# table = table + markdown_strings.table_delimiter_row(6, column_lengths=[6, 6, 6, 6, 6, 20])
# print(table)

# markdown_strings.table([["1", "2", "3"], ["4", "5", "6"]])
