import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def remove_stopword(text,namefile):
    
    text_tokens = text.split()
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    #print(tokens_without_sw)

    #riporto il testo normale senza stop word
    filtered_sentence = (" ").join(tokens_without_sw)
    #print(filtered_sentence)
    file = open(namefile,"w")
    file.write(filtered_sentence)
    print("file: "+namefile+" creato")
    file.close()
    return filtered_sentence
    