from fastapi import FastAPI
import pandas as pd

app = FastAPI()
FILE_PATH = 'data/games_full_info.csv'


@app.get("/")
async def root():
    return {"message: Hello World"}


@app.get("/games")
def get_games(minplayers: int = None,
              maxplayers: int = None,
              minduration: int = None,
              maxduration: int = None,
              minage: int = None,
              name: str = None,
              minyearpublished: int = None,
              maxyearpublished: int = None,
              ):
    DATA = pd.read_csv(FILE_PATH, sep=';')
    if minplayers:
        DATA = DATA.loc[DATA.minplayers >= minplayers]
    if maxplayers:
        DATA = DATA.loc[DATA.mpxlayers <= maxplayers]
    if minduration:
        DATA = DATA.loc[DATA.duration >= minduration]
    if maxduration:
        DATA = DATA.loc[DATA.duration <= maxduration]
    if minage:
        DATA = DATA.loc[DATA.age <= minage]
    if minyearpublished:
        DATA = DATA.loc[DATA.yearpublished >= minyearpublished]
    if maxyearpublished:
        DATA = DATA.loc[DATA.yearpublished <= maxyearpublished]
    if name:
        DATA = DATA.loc[DATA.name.str.match(f'.*{name}.*')]
    return {"games_data": DATA.to_json(orient='records')}
