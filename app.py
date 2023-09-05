from flask import Flask, render_template
import pandas as pd
from pathlib import Path
import datetime as dt

app = Flask(__name__)

@app.route('/')
def indexku():
    test_dict = {
        {
            'nama': 'Budi',
            'kaba'
        }
    }
    return render_template('index.html', ofc_on_duty = test_dict)

if __name__ == '__main__':
    PATH = Path(__file__).parent
    df = pd.read_excel(PATH / 'list-pegawai.xlsx')
    global nama, nip
    nama = df['Nama'].tolist()
    nip = df['NIP'].tolist()
    now = dt.datetime.now()
    if now > dt.timedelta(hours=18):
        nama = nama[0:8]
        nip = nip[0:8]
    data = dict(zip(nama, nip))
    app.run(debug=True)