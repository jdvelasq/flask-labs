"""
Document viewer
===============================================================================


"""
import textwrap

import pandas as pd

from .utils import load_filtered_documents


def document_viewer(directory, column, text, case=False, flags=0, regex=True, top_n=10):

    documents = load_filtered_documents(directory)
    contains = documents[column].str.contains(text, case=case, flags=flags, regex=regex)
    contains = contains.dropna()
    contains = contains[contains]
    documents = documents.loc[contains.index, :]

    column_list = []

    reported_columns = [
        "document_title",
        "authors",
        "global_citations",
        "source_title",
        "pub_year",
        "abstract",
        "author_keywords",
        "index_keywords",
    ]

    for column in reported_columns:
        if column in documents.columns:
            column_list.append(column)

    documents = documents[column_list]
    if "global_citations" in documents.columns:
        documents = documents.sort_values(by="global_citations", ascending=False)

    documents = documents.head(top_n)

    for index, row in documents.iterrows():

        for column in reported_columns:

            if column not in row.index:
                continue

            if column == "document_title":
                print("           document_title :", end="")
                print(
                    textwrap.fill(
                        row[column],
                        width=120,
                        initial_indent=" " * 28,
                        subsequent_indent=" " * 28,
                        fix_sentence_endings=True,
                    )[27:]
                )
                continue

            if column == "abstract":
                print("                 abstract :", end="")
                print(
                    textwrap.fill(
                        row[column],
                        width=120,
                        initial_indent=" " * 28,
                        subsequent_indent=" " * 28,
                        fix_sentence_endings=True,
                    )[27:]
                )
                continue

            if column in [
                "author_keywords",
                "author_keywords_cleaned",
                "index_keywords",
                "index_keywords_cleaned",
            ]:
                keywords = row[column]
                if pd.isna(keywords):
                    continue
                keywords = keywords.split("; ")
                print(" {:>24} : {}".format(column, keywords[0]))
                for keyword in keywords[1:]:
                    print(" " * 28 + keyword)
                continue

            print(" {:>24} : {}".format(column, row[column]))

        if index != documents.index[-1]:
            print("-" * 125)
