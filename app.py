from flask import Flask, render_template, url_for, request, json
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField
from livereload import Server
import pandas as pd
from pathlib import Path
import datetime as dt
from PIL import Image
import app
import time

PATH = Path(__file__).parent
IMAGEDIR = PATH / 'static' / 'images'

app: Flask = Flask(__name__)

def get_df_excel(df_name:str | None = 'list-pegawai - Copy') -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(PATH / f'{df_name}.xlsx', index_col=0)
    return df.sort_values(ascending=True, by='Nama')

def get_all_df(df:pd.DataFrame, with_shift:bool=False) -> list[dict]:
    return_df: list[dict] = []
    df['NIP'] = df['NIP'].apply(lambda x: x[1:])
    for x in range(len(df)):
        return_df.append(df.iloc[x].to_dict())
    if with_shift:
        return_df = get_non_shift_df(return_df, get_current_shift(df))
    return check_valid_photos(return_df)

def get_non_shift_df(df:list[dict], data_shift:list[dict]) -> list[dict]:
    return_df:list[dict] = []
    for data in df:
        if data not in data_shift:
            return_df.append(data)
    return return_df

def get_current_shift(df:pd.DataFrame) -> list[dict]:
    #get current shift data
    now: str = dt.datetime.now().strftime('%H:%M:%S')
    hours_now: str = now.split(':')[0]
    # df = df[df['Shift'] >= int(hours_now)]
    return_df: list[dict] = []
    for i in range(6):
        return_df.append(df.iloc[-i].to_dict())
    return return_df

def check_valid_photos(df:list[dict]) -> list[dict]:
    for x,data in enumerate(df):
        try:
            valid = str(next(IMAGEDIR.glob(f'{data["Nama File"]}.*')))
            df[x]['Nama File'] = valid.split('\\')[-1]
        except:
            df[x]['Nama File'] = 'template_photo.jpeg' 
    return get_profile_pics(df)

def get_profile_pics(df:list[dict]) -> list:
    for x,data in enumerate(df):
        data: str = url_for('static', filename='images/' + data['Nama File'])
        df[x]['Profpics'] = data
    return df


@app.route('/', methods=['GET', 'POST'])
def indexku():
    time = dt.datetime.now().strftime('%H:%M:%S')
    df: pd.DataFrame = get_df_excel()
    table: pd.DataFrame = check_valid_photos(get_current_shift(df))
    return render_template('index.html', table=table, time = time)

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    df: pd.DataFrame = get_df_excel()
    table = get_all_df(df, with_shift=True)
    return render_template('custom.html', table=table)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    df: pd.DataFrame = get_df_excel()
    table:list[dict] = check_valid_photos(get_current_shift(df))
    return render_template('remove.html', table=table)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    df: pd.DataFrame = get_df_excel()
    table = get_all_df(df)
    return render_template('edit.html', table=table)


if __name__ == '__main__':
    while(True):
        app.run(debug=True)
        server = Server(app.wsgi_app)
        server.serve()
        time.sleep(30)