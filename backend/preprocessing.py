import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

## Download required nltk data(run once)
nltk.download("stopwords")
nltk.download("wordnet")

stopwords = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text: str) -> str:
    
    """Cleans raw resume text by removing unwanted characters,
    stopwords, and applying lemmatization.
    """
    #Lowercase
    text = text.lower()
    
    #Remove special characters, digits, punctation
    text = re.sub(r"[^a-zA-Z\s]","",text)
    
    #Tokenize (split words)
    tokens = text.split()
    
    #Remove stopwords + lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords]
    
    #join back to single string
    return " ".join(tokens)