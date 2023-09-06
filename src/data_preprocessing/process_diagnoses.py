import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


# Define a function to clean the text
def clean_text(text):
    # Convert text to lower case
    text = text.lower()

    # Remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', text)

    # # Remove stop words
    # text = text.split()
    # text = [word for word in text if not word in set(stopwords.words('english'))]
    # text = ' '.join(text)

    return text


def get_categories():
    """A dictionary that maps each diagnosis category to a tuple containing the lower and upper bounds of its range"""

    icd_categories = {
        'Infectious And Parasitic Diseases': ('001', '139'),
        'Neoplasms': ('140', '239'),
        'Endocrine Nutritional And Metabolic Diseases And Immunity Disorders': ('240', '279'),
        'Diseases Of The Blood And Blood-Forming Organs': ('280', '289'),
        'Mental Disorders': ('290', '319'),
        'Diseases Of The Nervous System And Sense Organs': ('320', '389'),
        'Diseases Of The Circulatory System': ('390', '459'),
        'Diseases Of The Respiratory System': ('460', '519'),
        'Diseases Of The Digestive System': ('520', '579'),
        'Diseases Of The Genitourinary System': ('580', '629'),
        'Complications Of Pregnancy Childbirth And The Puerperium': ('630', '679'),
        'Diseases Of The Skin And Subcutaneous Tissue': ('680', '709'),
        'Diseases Of The Musculoskeletal System And Connective Tissue': ('710', '739'),
        'Congenital Anomalies': ('740', '759'),
        'Certain Conditions Originating In The Perinatal Period': ('760', '779'),
        'Symptoms Signs And Ill-Defined Conditions': ('780', '799'),
        'Injury And Poisoning': ('800', '999'),
        'Supplementary Classification Of Factors Influencing Health Status And Contact With Health Services': ('V01', 'V91'),
        'Supplementary Classification Of External Causes Of Injury And Poisoning': ('E000', 'E999')
    }

    return icd_categories


def group_diagnoses(code):
    if pd.isnull(code):
        return 'Missing'
    code = code[:4] if code[0] == 'E' else code[:3]

    categories_dict = get_categories()
    for category, (lower, upper) in categories_dict.items():
        if lower <= code <= upper:
            return category

    return 'Other'


def tfidf_diagnoses(df, column='short_title'):
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the 'short_title' column
    tfidf_matrix = vectorizer.fit_transform(df[column])

    # The result is a sparse matrix where each row corresponds to a document (a row in your data_preprocessing)
    # and each column corresponds to a word. The value in each cell is the TF-IDF score of that
    # word in that document.
    return tfidf_matrix
