import scraping
import pandas as pd
def store_csv(page):
    title = []
    link = []
    description = []
    text = []
    for i in page:
        title.append(i.title)
        link.append(i.link)
        description.append(i.description)
        text.append(i.text)

    df = pd.DataFrame()

    df["Title"] = title
    df["Link"] = link
    df["Description"] = description
    df["Text"] =  text

    df.to_csv('output.csv')

if __name__ == "__main__":
    num_page = 3

    page = scraping.search("assiteca",num_page)

    #print(page[2].text)
    str = page[2].text.lower()
    print(str.count("assiteca"))

    store_csv(page)
