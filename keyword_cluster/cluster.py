import os
import string
import time
from collections import Counter

import streamlit as st
import chardet
import pandas as pd
import plotly.express as px
import plotly.io as pio
from polyfuzz import PolyFuzz
from polyfuzz.models import SentenceEmbeddings
from sentence_transformers import SentenceTransformer

# Check if the system is Windows
IS_WINDOWS = os.name == 'nt'

if IS_WINDOWS:
    import win32com.client as win32
    win32c = win32.constants

COMMON_COLUMN_NAMES = [
    "Keyword", "Keywords", "keyword", "keywords",
    "Search Terms", "Search terms", "Search term", "Search Term"
]

def create_unigram(cluster: str, stem: bool):
    """Create unigram from the cluster and return the most common word."""
    words = cluster.split()
    word_counts = Counter(words)

    # Filter out number-only words
    word_counts = Counter({word: count for word, count in word_counts.items() if not word.isdigit()})

    if word_counts:
        # If there are any words left after filtering, return the most common one
        most_common_word = word_counts.most_common(1)[0][0]
    else:
        # If all words were number-only and thus filtered out, return 'no_keyword'
        most_common_word = 'no_keyword'

    return stem_and_remove_punctuation(most_common_word, stem)

def stem_and_remove_punctuation(text: str, stem: bool):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Stem the text if the stem flag is True
    if stem:
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text

def get_model(model_name: str):
    """Create and return a SentenceTransformer model based on the given model name."""
    model = SentenceTransformer(model_name)
    return model

def load_file(file_path: str):
    """Load a CSV file and return a DataFrame."""
    result = chardet.detect(open(file_path, 'rb').read())
    encoding_value = result["encoding"]
    white_space = False if encoding_value != "UTF-16" else True

    df = pd.read_csv(
        file_path,
        encoding=encoding_value,
        delim_whitespace=white_space,
        on_bad_lines='skip',
    )
    return df

def main():
    st.title("Keyword Clustering Streamlit App")

    chart_type = st.selectbox("Select chart type", ["sunburst", "treemap"])
    column_name = st.text_input("Column name in your CSV to be processed")
    device = st.selectbox("Select device", ["cpu", "cuda"])
    excel_pivot = st.checkbox("Save the output as an Excel pivot table")
    file_path = st.file_uploader("Upload your CSV file", type=["csv"])
    min_similarity = st.slider("Minimum similarity for clustering", 0.0, 1.0, 0.8, 0.01)
    model_name = st.text_input("Name of the SentenceTransformer model to use", "all-MiniLM-L6-v2")
    output_path = st.text_input("Path where the output CSV will be saved", "")
    remove_dupes = st.checkbox("Remove duplicates from the dataset", True)
    stem = st.checkbox("Enable stemming on the 'hub' column", False)
    volume = st.text_input("Name of the column containing numerical values", "")

    if st.button("Cluster Keywords"):
        # Clear the screen
        st.empty()

        # Print welcome message
        st.header("Keyword Clustering Result")

        # ... (same as before, process the data and display the result)
        # Example: st.dataframe(df)

        # Print the generated chart
        st.header("Generated Chart")
        # Example: st.plotly_chart(fig)

if __name__ == "__main__":
    main()
