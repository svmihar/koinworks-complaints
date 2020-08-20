import texthero.preprocessing as h
from util import data_path
import pandas as pd
import os
import uuid

stopwords = {a.replace("\n", "") for a in (open("stopwords.txt").readlines())}
custom_pipeline = (
    h.lowercase,
    h.remove_digits,
    h.remove_punctuation,
    h.remove_diacritics,
    lambda x: h.remove_stopwords(x, stopwords=stopwords),
    h.remove_whitespace,
)


def custom_pipe(tweets):
    return


def is_referral(tweet):
    p = False
    t = tweet.split()
    keywords = ["referral", "kode", "referal", "code", "click to watch"]
    for word in keywords:
        if word in t:
            p = True
        return p


df = pd.read_csv(data_path / "koinworks_raw.csv")
data_folder = os.listdir()

if '0_koinworks_raw_id.csv' not in data_folder:
    df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df.to_csv(data_path / "koinworks_raw.csv")
del data_folder

df["cleaned"] = h.clean(df["tweet"], pipeline=custom_pipeline)
df["flair_dataset"] = h.clean(df["tweet"], pipeline=custom_pipeline[:4])
df["flair_dataset"] = h.remove_whitespace(df["flair_dataset"])
df["is_ref"] = df["cleaned"].apply(is_referral)
df = df[df["is_ref"] == False]
df = df[df["username"] != "danielchayau"]  # spam / bot account
df = df[df["username"] != "koinworks"]  # own koinworks
df = df.dropna()
df = df.reset_index(drop=True)

print("now saving the flair format dataset")

df.to_pickle(data_path / "1_koinworks_cleaned.pkl")


# testing kalo stopwords nya udah di remove
for tweet in df["cleaned"].values:
    if "kalian" in tweet:
        print("belum ke remove")
        break
