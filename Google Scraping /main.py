import scraping
import pandas as pd
from weasyprint import HTML
import sys
import datetime

#controllo la validità della data
def date_check(start,end):
    try:
        datetime.datetime.strptime(start_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")
    try:
        datetime.datetime.strptime(end_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")
    if start < end:
        return True
    else:
        return False

#divido le parole chiave
def keywords(keyword):
    text = keyword.split('-')
    word =''
    for t in text:
        word += t +" "
    return word

#creo il file xlsx
def store_xlsx(page,id_master):
    title = []
    link = []
    description = []
    text = []
    ID_master = []
    data = []
    for i in page:
        title.append(i.title)
        link.append(i.link)
        data_descr = i.description.split('—')
        data.append(data_descr[0])
        description.append(data_descr[1])

        #controllo se il campo text è vuoto e lo riempio con la descrizione
        if (i.text==" " or not i.text):
            i.text = data_descr[1]

        text.append(i.text)
        ID_master.append(id_master)

    df = pd.DataFrame()
    df["ID MASTER"] = ID_master
    df["Title"] = title
    df["Link"] = link
    df["Data"] = data
    df["Description"] = description
    df["Text"] =  text

    #df.to_csv('output.csv')
    df.to_excel('output.xlsx')

#creo il file pdf dal html
def from_html_to_pdf(page):
    for i in page:
        url = i.link.split('https://')
        name =url[1].split('.')
        HTML(i.link).write_pdf('pdf/'+name[1] +'.pdf')


if __name__ == "__main__":

    num_page = 999

    #numero di parametri
    if (len(sys.argv))!=5:
        print(
              "start date :"+ "%d/%m/%Y"+"\n" +
              "end date : "+"%d/%m/%Y"+"\n" +
              "ID Master : " + "interger number"+"\n"+
              "KEY WORD : "+ "string"
                )
    else:
        name_script,start_date,end_date,id_master,word = sys.argv

        query = keywords(word)

        #se la data è corretta allora procedo
        if(date_check(start_date,end_date) == True):

            print("##### Inizio della Scraping per la keyword {query} #####")
            page = scraping.search(query,start_date,end_date,num_page)
            print("##### Finito dello Scraping per la keyword {query} #####\n")

            print("##### Creazione del del file Xlsx ######")
            store_xlsx(page,id_master)
            print("##### File Xlsx creato ######\n")

            print("##### Creazione dei PDF ######\n")
            from_html_to_pdf(page)
            print("##### FINE creazione dei PDF ######\n")
        else:
            print("Controlla le date!!!!")
