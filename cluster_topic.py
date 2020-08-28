try:
    import os
    import ktrain
except Exception as e:
    print(e)
    pass
import numpy as np
from collections import Counter
from pprint import pprint
from util import data_path
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

"""
clustering topics
"""
# TODO: bikin top k words per cluster method
# TODO: pemilih


def get_k_word(tweets: list):
    words = [b for a in tweets for b in a.split()]
    return [a[0] for a in Counter(words).most_common(10)]


def check_column(column_name, df):
    return column_name in df.columns


def kmeans_(df):
    if not check_column("pca", df):
        raise ValueError("column pca not found in df")
    X = np.array([a for a in df.pca.values])
    range_n_cluster = [x for x in range(4, 20, 2)]
    clusters = [KMeans(n_clusters=n) for n in range_n_cluster]
    labels = [cluster.fit_predict(X) for cluster in clusters]
    scores = [silhouette_score(X, label) for label in labels]
    best_by_index = np.argmax(scores)
    print(
        f"highest silhouette score is {scores[best_by_index]}\n \
            with n_cluster: {range_n_cluster[best_by_index]} "
    )
    df["kmeans"] = labels[best_by_index]
    return df


def dbscan_(df):
    if not check_column("pca", df):
        raise ValueError("column pca not found in df")
    X = np.array([a for a in df.pca.values])
    db = DBSCAN(eps=0.003, min_samples=3)  # 3-> 2 * n - 1
    db.fit(X)
    labels = db.labels_
    df["dbscan"] = labels
    return df


def lda_method(df):
    """ CANNOT RETRIEVE THE TOPIC ID"""
    tweets = df.cleaned.values
    tm = ktrain.text.get_topic_model(tweets, n_topics=None, n_features=10000)
    tm.print_topics(show_counts=True)
    # precompute doc matrix (isinya probability ditribution)
    tm.build(tweets, threshold=0)  # 0 karena ada range_id yang harus persistent
    tweet_docs = tm.get_docs()
    assert len(tweets) == len(tweet_docs)
    topic_selection = input("select your input here (1 2 3 ...)\n>")
    topic_selection = topic_selection.split()
    docs = tm.get_docs(topic_ids=topic_selection, rank=True)
    df["range_id"] = [x for x in range(len(df))]
    keluhan_df = pd.DataFrame(docs, columns=["text", "range_id", "score", "topic_id"])
    keluhan_df = keluhan_df[["text", "range_id", "topic_id"]]
    df = df.merge(keluhan_df, on="range_id")
    df = df[["id", "date", "username", "cleaned", "range_id", "topic_d"]]
    df.to_csv("./data/5_keluhan_lda.csv", index=False)


if __name__ == "__main__":
    df = pd.read_pickle(data_path / "2_koinworks_fix.pkl")
    tes = df.pipe(kmeans_).pipe(dbscan_)
    tes.to_pickle(data_path / "4_hasil_cluster.pkl")
#     dbscan_method(df)
# keluhan_flair()
