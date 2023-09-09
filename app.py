from flask import Flask, render_template
import pandas as pd
from pathlib import Path
import datetime as dt
from PIL import Image
import base64

app = Flask(__name__)

def get_images(name: str) -> Image.Image:
    img = Image.open(PATH / 'assets' / name)
    pass

@app.route('/', methods=['GET', 'POST'])
def indexku():
    num_images = 2
    table = [
        {
            'nama': 'Budi',
            'nip': '21085249',
        }
    ]
    return render_template('index.html', table=table, num_images=num_images)

if __name__ == '__main__':
    PATH = Path(__file__).parent
    # if now > dt.timedelta(hours=18):
    #     nama = nama[0:8]
    #     nip = nip[0:8]
    app.run(debug=True)