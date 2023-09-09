from flask import Flask, render_template, url_for
import pandas as pd
from pathlib import Path
import datetime as dt
from PIL import Image
import base64
from glob import glob
import app
from livereload import Server

app: Flask = Flask(__name__)

def get_df_excel(df_name:str | None = 'list-pegawai - Copy') -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(PATH / f'{df_name}.xlsx', index_col=0)
    return df

def get_current_shift(df:pd.DataFrame) -> list[dict]:
    #get current shift data
    now: str = dt.datetime.now().strftime('%H:%M:%S')
    hours_now: str = now.split(':')[0]
    # df = df[df['Shift'] >= int(hours_now)]
    return_df: list[dict] = []
    for i in range(6):
        return_df.append(df.iloc[i].to_dict())
    return return_df

def check_valid_photos(df:list[dict]) -> list[dict]:
    for x,data in enumerate(df):
        try:
            valid = glob(PATH / 'static' / 'images' / f'{data["Nama File"]}.*')
            df[x]['Nama File'] = valid[0]
        except:
            df[x]['Nama File'] = 'template_photo.jpeg' 
    return df

def get_profile_pics(df:list[dict]) -> list:
    for x,data in enumerate(df):
        data = url_for('static', filename='images/' + 'template_photo.jpeg')
        df[x]['Profpics'] = data
    return df


@app.route('/', methods=['GET', 'POST'])
def indexku():
    # table = [
    #     {
    #         'nama': 'Budi',
    #         'nip': '21085249',
    #     }
    # ]
    df: pd.DataFrame = get_df_excel()
    table: pd.DataFrame = get_current_shift(df)
    table = check_valid_photos(table)
    table = get_profile_pics(table)
    return render_template('index.html', table=table)

if __name__ == '__main__':
    PATH = Path(__file__).parent
    # if now > dt.timedelta(hours=18):
    #     nama = nama[0:8]
    #     nip = nip[0:8]
    server = Server(app.wsgi_app)
    app.run(debug=True)
    server.serve()