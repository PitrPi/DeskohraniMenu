import os
import re

import requests
import pandas as pd
import shutil
from data_loader import write_final_df

PATH = 'games_full_info.csv'
OVERWRITE = False


def open_data_file(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8")
    return df


def download_images(games: pd.DataFrame) -> None:
    for name, url, url_full in zip(games["name_x"], games["thumbnail"], games["image"]):
        name = re.sub(" ", "_", name)
        if not os.path.isfile("assets/"+name+'.png') or OVERWRITE:
            response = requests.get(url, stream=True)
            with open('assets/'+name+'.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        if not os.path.isfile("assets/"+name+'_full.png') or OVERWRITE:
            response = requests.get(url_full, stream=True)
            with open('assets/'+name+'_full.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)


def add_internal_link(df: pd.DataFrame) -> pd.DataFrame:
    df["local_thumb"] = ["![{nm}](assets/{nm}.png)".format(nm=re.sub(" ", "_", x)) for x in df["name_x"]]
    df["local_full"] = ["![{nm}](assets/{nm}_full.png)".format(nm=re.sub(" ", "_", x)) for x in df["name_x"]]
    df.drop(["thumbnail", "image"], axis=1, inplace=True)
    return df


def step():
    data = open_data_file(PATH)
    download_images(data)
    data = add_internal_link(data)
    out_path = "games_full_info.csv"
    write_final_df(data, out_path)



if __name__ == '__main__':
    data = open_data_file(PATH)
    download_images(data)
    data = add_internal_link(data)
    out_path = "games_full_info.csv"
    write_final_df(data, out_path)
