#Remove number
import re
def remove_number():
    input_str = "Box A contains 3 red and 5 white balls, while Box B contains 4 red and 2 blue balls."
    result = re.sub(r'\d+', '', input_str)
    print(result)


import string
def remove_punctuation():
    text = "Hey, did you know that the summer break is coming? Amazing right !! It's only 5 more days !!"
    translator = str.maketrans('', '', string.punctuation)
    print(text.translate(translator))

def remove_whitespace():
    text = "   we don't need   the given questions"
    print(  " ".join(text.split()))

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# remove stopwords function
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return filtered_text

import nltk
nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
stemmer = PorterStemmer()

# stem words in the list of tokenised words
def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
lemmatizer = WordNetLemmatizer()
# lemmatize string
def lemmatize_word(text):
    word_tokens = word_tokenize(text)
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens]
    return lemmas

if __name__ == '__main__':
    remove_number()
    remove_punctuation()
    remove_whitespace()

    example_text = "This is a sample sentence and we are going to remove the stopwords from this."
    print(remove_stopwords(example_text))

    text = 'data science uses scientific methods algorithms and many types of processes'
    print(stem_words(text))


    text = 'data science uses scientific methods algorithms and many types of processes'
    print(lemmatize_word(text))
