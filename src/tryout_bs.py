import pickle
import unicodedata
import bs4 as bs
import requests

v_file = open('data/pickled_data/pickled_viptips.xyz', 'rb')
v_pickled = pickle.load(v_file)
h_file = open('data/pickled_data/pickled_history.xyz', 'rb')
h_pickled = pickle.load(h_file)

viptips = bs.BeautifulSoup(v_pickled.content, "html5lib")
history = bs.BeautifulSoup(h_pickled.content, "html5lib")

# actual_vip_site = requests.get("https://xxviptips.blogspot.com/")
# actual_vip_sauce = bs.BeautifulSoup(actual_vip_site.content, "html5lib")
table_data = []

# for table in history.select("table"):
for table in viptips.select("table"):
# for table in actual_vip_sauce.select("table"):
    rows = table.select("tr")
    league = unicodedata.normalize("NFKD", rows[0].get_text(strip=True))
    match, info1, info2 = [unicodedata.normalize("NFKD", td.get_text(strip=True)) for td in rows[1].select("td")]
    # for td in rows[1].select('td'):
    #     print(td.get_text(strip=True))
    rate_star = " ".join([":star:"] * len(rows[2].select("img")))
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

for match in table_data:
    for match_detail in match:
        if "\xa0" in match_detail:
            print(match_detail)
            match_detail = unicodedata.normalize('NFKD', match_detail)
            print(match_detail)
        # if unicodedata.is_normalized('NFD', match_detail):
        #     print(match_detail)
            # new_match_detail = unicodedata.normalize("\xa0", match_detail)
            # print(new_match_detail)
