import pickle
import bs4 as bs
from markdownify import markdownify as md

v_file = open('data/pickled_data/pickled_viptips.xyz', 'rb')
v_pickled = pickle.load(v_file)

viptips = bs.BeautifulSoup(v_pickled.content, "html5lib")

for table in viptips.select("table"):
    rows = table.select("tr")
    league = rows[0].get_text(strip=True)
    match, info1, info2 = [td.get_text(strip=True) for td in rows[1].select("td")]
    rate_star = " ".join([":star:"] * len(rows[2].select("img")))
    final_score_title, final_score = [
        "no results yet" if td.get_text(strip=True) == "" else td.get_text(strip=True) for td in rows[3].select('td')
    ]

    print(f"{league}, {match}, {info1}, {info2}, {rate_star}, {final_score_title} -- {final_score}")


all_tbls = viptips.find_all('table')

url_2_hit = "https://i.imgur.com/ffIvqVj.png"

new_p_tag = viptips.new_tag('p')
new_p_tag.string = ":star:"

other_imgs = []

with open('data/html_data/viptips.html', 'w') as html_writer:
    html_writer.write(str(v_pickled.content))


for table in all_tbls:
    for tr in table.find_all('tr'):
        for td in table.find_all('td'):
            for star_images in td.find_all('img'):
                if star_images['src'] == url_2_hit:
                    print(star_images)
                    p_tag = viptips.new_tag('p')
                    p_tag.string = ":star:"
                    # td.star_images.replace_with(p_tag)
                    td.replace_with(p_tag)
                    # td.clear(i)
                    modified_bs = bs.BeautifulSoup(p_tag, "html5lib").i
                    star_images.replace_with(modified_bs)
                    print(star_images)
                    some_p_tag = str(td).replace
                    some_p_tag.string = ":star:"
                    img.replace_with(some_p_tag)
                else:
                    # todo: replace country img with name here or something similar
                    other_imgs.append(star_images)

"""
some_table = 'sometable'
with open('data/some_table', 'r') as table_reader:
    some_table = table_reader.read()
print(str(some_table))

md_table = md(some_table)
print(md_table)
for table in all_tbls:
    if table is not None:
        print(table)
        something = md(table)
        print(something)

tbl_1 = all_tbls.pop()
print(tbl_1)
something = md(tbl_1)
print(something)

some_other_thing = md(v_pickled.content)
print(some_other_thing)
with open('data/some_markdown_file.md', 'w') as write_md:
    write_md.write(str(some_other_thing))
    # for table in all_tbls:
    #     md_file = md(table)
    #     write_md.write(str(md_file))

imgs = viptips.find_all('img')
len(imgs)
for img in imgs:
    if img['src'] == url_2_hit:
        parent = img.find_parent()
        print(parent)
        parent = img.replace_with(new_p_tag)
        print(parent)
        # replacement = img.find_parent().replace(new_p_tag)
        # img.replace_with(replacement)
        # img.find_parent().replace_with(new_p_tag)
        # img.find_parent().replace_with(new_p_tag)
for tbl in all_tbls:
    imgs = tbl.find_all('img')
    print(len(imgs))
    # if tbl.find_parent('table') is not None:
    #     print("works till now")
    # else:
    #     print("doesn't work")
# for tbl in all_tbls:
#     for tbody in tbl:
#         for tr in tbody:
#             # type(tr)
#             if type(tr) is str:
#                 # print(tr)
#                 # tr.decompose()
#                 pass
#             else:
#                 for td in tr:
#                     if type(td) is str:
#                         pass
#                     else:
#                         # print(td)
#                         if td.has_attr('img'):
#                             print("yes it does")
 """
