from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField
from livereload import Server
import pandas as pd
import re
import json
from pathlib import Path
import datetime as dt
from PIL import Image
import app
import time

PATH = Path(__file__).parent
IMAGEDIR = PATH / 'static' / 'images'

with open(PATH / 'list-shift.txt', 'r') as f:
    shift = f.read()
all_shift:dict = json.loads(shift)
    
app: Flask = Flask(__name__)


def get_df_excel(df_name:str = 'list-pegawai-sekarang',cleannip:bool=True) -> pd.DataFrame:
    """Get excel for all user"""
    df: pd.DataFrame = pd.read_excel(PATH / f'{df_name}.xlsx', index_col=0)
    if cleannip:
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

def get_current_shift(df:pd.DataFrame, todict:bool=True):
    """get current shift data"""
    get_current_time = dt.datetime.now() 
    get_current_time = get_current_time.strftime('%d %H:%M')
    current_day = get_current_time.split()[0]
    # df = df.loc[:,int(current_day)]
    # print(get_current_time)
    current_hour = get_current_time.split()[1]
    for shift, hour in all_shift.items():
        # print(shift,hour)
        minhour = int(hour.split('-')[0].split('.')[0]) * 60 + int(hour.split('-')[0].split('.')[1]) 
        maxhour = int(hour.split('-')[1].split('.')[0]) * 60 + int(hour.split('-')[1].split('.')[1])
        if(maxhour < minhour):
            maxhour += 24 * 60
            if(int(current_hour.split(':')[0]) < 2):
                current_hour = str(int(current_hour.split(':')[0])+24) + ':' + current_hour.split(':')[1] 
        
        now_hour = int(current_hour.split(':')[0]) * 60 + int(current_hour.split(':')[1])
        if(now_hour > minhour and now_hour < maxhour):
            df = df[df[int(current_day)] == shift]
            # print('shiftnow is ', shift)
            break
    return_df: list[dict] = []
    if todict:
        for i in range(len(df)):
            return_df.append(df.iloc[i].to_dict())
        
        return return_df
    else:
        return df

def get_current_shit_to_excel() -> None:
    df:pd.DataFrame = get_df_excel('list-pegawai', cleannip=False)
    df:pd.DataFrame = get_current_shift(df, todict=False)
    df.reset_index(drop=True,inplace=True)
    df.to_excel('list-pegawai-sekarang.xlsx')
    return None

def save_current_edit(edit:dict) -> None:
    df:pd.DataFrame = get_df_excel(cleannip=False)
    df.loc[len(df)] = edit
    df.to_excel('list-pegawai-sekarang.xlsx')
    return None

def delete_current_edit(edit_nip:str) -> None:
    df:pd.DataFrame = get_df_excel(cleannip=False)
    try:
        get_index = df.index[df['NIP']==edit_nip].tolist()[0]
        df.drop(get_index, inplace=True)
        df.to_excel('list-pegawai-sekarang.xlsx')
        print('success', get_index)
    except:
        print('Not Found!')
    return None
    
    

def check_valid_photos(df:list[dict]) -> list[dict]:
    """Validating the photos, if not exist, change to default photo"""
    # print(df)
    for x,data in enumerate(df):
        # print(data)
        try:
            valid = str(next(IMAGEDIR.glob(f'{data["NIP"]}.*')))
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


def remove_photos(location: str) -> None:
    """Remove the photos"""
    try:
        Path(location).unlink()
    except:
        pass
    return None

def clear_shift(all_shift:dict) -> dict:
    """Clear shift with Nothing in value (Cuti and Dinas Luar)"""
    newdict :dict = {}
    for k,v in all_shift.items():
        if v != '':
            newdict[k] = v
    return newdict

@app.route('/', methods=['GET', 'POST'])
def indexku():
    """Homepage"""
    time = dt.datetime.now().strftime('%H:%M:%S')
    df: pd.DataFrame = get_df_excel()
    table: pd.DataFrame = get_all_df(df)
    return render_template('index.html', table=table, time = time)

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    """Custom Page, for adding the Pegawai"""
    df: pd.DataFrame = get_df_excel('list-pegawai', cleannip=True)
    table = get_all_df(df, with_shift=True)
    
    if request.method == 'POST':
        nama_new = request.form.get('nama')
        nip_new = '\'' + request.form.get('nip')
        # foto_new = request.form.get('fotoPegawai')  
        namafile = re.sub(r'[\(\),.! ]', '', nama_new)
    
        edit = [nama_new, namafile, nip_new] + ['-' for i in range(30)]
        save_current_edit(edit)
    return render_template('custom.html', table=table)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    """Custom Page, but for removing the Pegawai"""
    df: pd.DataFrame = get_df_excel()
    table:list[dict] = check_valid_photos(get_current_shift(df))
    
    if request.method == 'POST':
        nama_new = request.form.get('nama')
        nip_new = '\'' + request.form.get('nip')
        foto_new = request.form.get('fotoPegawai')  

        delete_current_edit(nip_new)
    return render_template('remove.html', table=table)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """Custom Page, but for editing the Pegawai"""
    df: pd.DataFrame = get_df_excel('list-pegawai', cleannip=True)
    table = get_all_df(df)
    
    if request.method == 'POST':
        nama_new = request.form.get('nama')
        nip_new = request.form.get('nip')
        try:
            if('fotoUploadPegawai' not in request.files):
                print('No file part')
            if remove_location := str(next(IMAGEDIR.glob(f'{nip_new}.*'))):
                remove_photos(remove_location)
            foto_new = request.files['fotoUploadPegawai']
            extension = foto_new.filename.split('.')[-1]
            # filename = re.sub(r'[\(\),.! ]', '', nama_new)
            # print(request.files['fotoUploadPegawai'])
            foto_new.save(f"{IMAGEDIR}/{nip_new}.{extension}")
        except:
            foto_new = request.form.get('fotoPegawai')
        # print(nama_new, nip_new, foto_new)
    return render_template('edit.html', table=table)


if __name__ == '__main__':
    all_shift = clear_shift(all_shift)
    
    
    while(True):
        get_current_shit_to_excel()    
        # reset_current_shift()
        app.run(debug=True)
        server = Server(app.wsgi_app)
        server.serve()
        time.sleep(30)