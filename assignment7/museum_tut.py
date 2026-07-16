# %% --- Import Libraries ---
from bs4 import BeautifulSoup

# %% --- code ---
# Collect first page of artists’ list
# page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')

pages = []

for i in range(1, 5):
    url = (
        "https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ"
        + str(i)
        + ".htm"
    )
    pages.append(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, "html.parser")

# Remove bottom links
last_links = soup.find(class_="AlphaNav")
last_links.decompose()

# Pull all text from the BodyText div
artist_name_list = soup.find(class_="BodyText")

# Pull text from all instances of <a> tag within BodyText div
artist_name_list_items = artist_name_list.find_all("a")

# Create for loop to print out all artists' names
for artist_name in artist_name_list_items:
    names = artist_name.contents[0]
    links = "https://web.archive.org" + artist_name.get("href")
    print(names)
    print(links)

# %%
