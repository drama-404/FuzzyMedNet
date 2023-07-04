import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


# Define a function to clean the text
def clean_text(text):
    # Convert text to lower case
    text = text.lower()

    # Remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Remove stop words
    text = text.split()
    text = [word for word in text if not word in set(stopwords.words('english'))]
    text = ' '.join(text)

    return text


def tfidf_diagnoses(df, column='short_title'):
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the 'short_title' column
    tfidf_matrix = vectorizer.fit_transform(df[column])

    # The result is a sparse matrix where each row corresponds to a document (a row in your data)
    # and each column corresponds to a word. The value in each cell is the TF-IDF score of that
    # word in that document.
    return tfidf_matrix
