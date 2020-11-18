import scraping


if __name__ == "__main__":
    num_page = 1

    page = scraping.search("assiteca",num_page)

    for i in page:
        print(i)
