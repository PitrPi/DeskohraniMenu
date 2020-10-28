import re
from typing import Union, Optional

import requests
import pandas
from xml.etree import ElementTree

ELEMENTS = ["yearpublished",
            "minplayers",
            "maxplayers",
            "playingtime",
            "age",
            "name",
            "description",
            "image",
            "thumbnail",
            "boardgamecategory"]


def load_df(path_to_df: str) -> pandas.DataFrame:
    df = pandas.read_csv(path_to_df, encoding="utf-8", sep=";")
    return df


def load_games_id_bgg(games: pandas.DataFrame, out_path: Optional[str]) -> pandas.DataFrame:
    if "bgg_id" not in games.columns:
        games["bgg_id"] = None
    games["bgg_id"] = [request_id_bgg(nm) if bgg_id is None else bgg_id for nm, bgg_id in games.loc[:, ["name", "bgg_id"]].values]
    if out_path:
        games.to_csv(out_path, index=False, encoding="utf-8", sep=";")
    return games


def get_bgg_info(games: pandas.DataFrame) -> pandas.DataFrame:
    resp = requests.get("https://www.boardgamegeek.com/xmlapi/boardgame/{}".format(
        ",".join(map(str, filter(None, games.bgg_id)))))
    resp_text = resp.content.decode("utf-8")
    # resp_text = re.sub("\\\\[nt]", "", resp_text)
    resp_parsed = ElementTree.fromstring(resp_text)
    resp_dict = {}
    for child in resp_parsed:
        resp_dict[child.get('objectid')] = {}
        for element in ELEMENTS:
            resp_dict[child.get('objectid')][element] = ""
            for val in child.findall(element):
                resp_dict[child.get('objectid')][element] += val.text+", "
            resp_dict[child.get('objectid')][element] = resp_dict[child.get('objectid')][element][:-2]
    final_df = pandas.DataFrame.from_dict(resp_dict, orient="index")
    final_df["bgg_id"] = final_df.index
    final_df.bgg_id = final_df.bgg_id.astype(int)
    return final_df


def request_id_bgg(nm: str) -> Optional[int]:
    resp = requests.get("https://www.boardgamegeek.com/xmlapi/search?search={}&exact=1".format(nm))
    string_xml = str(resp.content)
    bgg_id = re.findall('(?<=objectid=")\d*(?=")', string_xml)
    if id:
        return bgg_id[0]
    else:
        return None


def write_final_df(games_df: pandas.DataFrame, out_path:str) -> None:
    games_df.to_csv(out_path, index=False, encoding="utf-8", sep=";")


def step():
    data_path = "table.csv"
    out_path = "games_full_info.csv"
    games_df = load_df(data_path)
    games_df = load_games_id_bgg(games_df, out_path=data_path)
    games_bgg_info = get_bgg_info(games_df)
    final_df = pandas.merge(games_df, games_bgg_info, on="bgg_id", how="left")
    write_final_df(final_df, out_path)


if __name__ == '__main__':
    data_path = "table.csv"
    out_path = "games_full_info.csv"
    games_df = load_df(data_path)
    games_df = load_games_id_bgg(games_df, out_path=data_path)
    games_bgg_info = get_bgg_info(games_df)
    final_df = pandas.merge(games_df, games_bgg_info, on="bgg_id", how="left")
    write_final_df(final_df, out_path)
