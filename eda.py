from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition.pca import PCA
from sklearn.model_selection import train_test_split
from util import data_path
import pandas as pd


df = pd.read_pickle(data_path / "1_koinworks_cleaned.pkl")
df = df[["id", "date", "username", "cleaned", "tweet", "name"]]
df["date"] = pd.to_datetime(df["date"])
print(f"before drop duplicate: {len(df)}")
df = df.drop_duplicates(subset=["cleaned"])
print(f"after drop duplicate: {len(df)}")
df.dropna(inplace=True)

# TFIDF embeddings
vectorizer = TfidfVectorizer()
pca = PCA(n_components=2, svd_solver="full")
X = vectorizer.fit_transform(df.cleaned.values)
X_pca = pca.fit_transform(X.toarray())
df["pca"] = [a for a in X_pca]
df["tfidf"] = X
df.to_pickle(data_path / "2_koinworks_fix.pkl")
tweets = df.cleaned.values
x, y = train_test_split(tweets)
y_test, y_val = train_test_split(y)
with open(data_path / "flair_format/train/train.txt", "w") as f:
    for t in tweets:
        f.writelines(f"{t}\n")
with open(data_path / "flair_format/test.txt", "w") as f:
    for t in y_test:
        f.writelines(f"{t}\n")
with open(data_path / "flair_format/valid.txt", "w") as f:
    for t in y_val:
        f.writelines(f"{t}\n")
