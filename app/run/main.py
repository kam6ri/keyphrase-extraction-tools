from abc import ABC, abstractmethod

import nltk
import pandas as pd
import pke
import spacy
import streamlit as st

METHODS = ["PKE"]
POS = ["NOUN", "PROPN", "ADJ", "NUM"]


class Container(ABC):
    def __init__(self, container):
        self.container = container
        with self.container:
            self.set_elements()

    @abstractmethod
    def set_elements(self):
        raise NotImplementedError()


class Controller(Container):
    def set_elements(self):
        st.session_state["method"] = st.selectbox("method", METHODS)

        if st.button("RUN"):
            st.session_state["run"] = True


st.title("Keyphrase Extract App")
c1, c2 = st.columns([1, 1])
controller = Controller(c1)
st.session_state["text"] = c2.text_area("text", height=400)

if st.session_state.get("run"):
    st.title("result")

    c3, c4 = st.columns([1, 1])

    if st.session_state["method"] == "PKE":
        # Setting for pke to use japanese
        pke.lang.stopwords["ja_ginza"] = "ja"
        stopwords = list(spacy.lang.ja.STOP_WORDS)
        try:
            nltk.corpus.stopwords.words_org = nltk.corpus.stopwords.words
        except:
            nltk.download("stopwords")
            nltk.corpus.stopwords.words_org = nltk.corpus.stopwords.words
        nltk.corpus.stopwords.words = (
            lambda lang: stopwords
            if lang == "ja"
            else nltk.corpus.stopwords.words_org(lang)
        )

        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(
            input=st.session_state["text"],
            language="ja_ginza",
            spacy_model=spacy.load("ja_ginza"),
        )
        extractor.candidate_selection(pos=POS)
        extractor.candidate_weighting(threshold=0.74, method="average", alpha=1.0)
        keyphrases = extractor.get_n_best(n=10)
    else:
        raise NotImplementedError()

    df = (
        pd.DataFrame(keyphrases, columns=["keyphrase", "score"])
        .sort_values(by="score", ascending=False)
        .reset_index(drop=True)
    )
    df.index += 1

    c3.table(df)
