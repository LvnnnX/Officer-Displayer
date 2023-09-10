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
    """Get excel for all user"""
    df: pd.DataFrame = pd.read_excel(PATH / f'{df_name}.xlsx', index_col=0)
    df['NIP'] = df['NIP'].apply(lambda x: x[1:])
    return df.sort_values(ascending=True, by='Nama')

def get_all_df(df:pd.DataFrame, with_shift:bool=False) -> list[dict]:
    """Change dataframe to list of dict"""
    return_df: list[dict] = []
    for x in range(len(df)):
        return_df.append(df.iloc[x].to_dict())
    if with_shift:
        return_df = get_non_shift_df(return_df, get_current_shift(df))
    return check_valid_photos(return_df)

def get_non_shift_df(df:list[dict], data_shift:list[dict]) -> list[dict]:
    """Get non shift (Pegawai Tidak Sedang Shift) data"""
    return_df:list[dict] = []
    for data in df:
        if data not in data_shift:
            return_df.append(data)
    return return_df

def get_current_shift(df:pd.DataFrame) -> list[dict]:
    """get current shift data"""
    now: str = dt.datetime.now().strftime('%H:%M:%S')
    hours_now: str = now.split(':')[0]
    # df = df[df['Shift'] >= int(hours_now)]
    return_df: list[dict] = []
    
    for i in range(6):
        return_df.append(df.iloc[-i].to_dict())
    
    return return_df

def check_valid_photos(df:list[dict]) -> list[dict]:
    """Validating the photos, if not exist, change to default photo"""
    for x,data in enumerate(df):
        try:
            valid = str(next(IMAGEDIR.glob(f'{data["Nama File"]}.*')))
            df[x]['Nama File'] = valid.split('\\')[-1]
        except:
            df[x]['Nama File'] = 'template_photo.jpeg' 
    return get_profile_pics(df)

def get_profile_pics(df:list[dict]) -> list:
    """Get profile pics from static/images"""
    for x,data in enumerate(df):
        data: str = url_for('static', filename='images/' + data['Nama File'])
        df[x]['Profpics'] = data
    return df


@app.route('/', methods=['GET', 'POST'])
def indexku():
    """Homepage"""
    time = dt.datetime.now().strftime('%H:%M:%S')
    df: pd.DataFrame = get_df_excel()
    table: pd.DataFrame = check_valid_photos(get_current_shift(df))
    return render_template('index.html', table=table, time = time)

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    """Custom Page, for adding the Pegawai"""
    df: pd.DataFrame = get_df_excel()
    table = get_all_df(df, with_shift=True)
    return render_template('custom.html', table=table)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    """Custom Page, but for removing the Pegawai"""
    df: pd.DataFrame = get_df_excel()
    table:list[dict] = check_valid_photos(get_current_shift(df))
    return render_template('remove.html', table=table)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """Custom Page, but for editing the Pegawai"""
    df: pd.DataFrame = get_df_excel()
    table = get_all_df(df)
    
    if request.method == 'POST':
        nama_new = request.form.get('nama')
        nip_new = request.form.get('nip')
        try:
            if('fotoUploadPegawai' not in request.files):
                print('No file part')
            foto_new = request.files['fotoUploadPegawai']
            extension = foto_new.filename.split('.')[-1]
            foto_new.save(f'{IMAGEDIR}/{nama_new}.{extension}')
        except:
            foto_new = request.form.get('fotoPegawai')
        print(nama_new, nip_new, type(foto_new), foto_new)
    return render_template('edit.html', table=table)


def reset_current_shift() -> None:
    """Resetting the current shift, so the current shift will be empty"""
    template_docs:pd.DataFrame = get_df_excel()
    df:pd.DataFrame = pd.DataFrame(columns=template_docs.columns)
    df.to_excel(PATH / 'current-shift.xlsx', index=False)
    return None


if __name__ == '__main__':
    while(True):
        reset_current_shift()
        app.run(debug=True)
        server = Server(app.wsgi_app)
        server.serve()
        time.sleep(30)