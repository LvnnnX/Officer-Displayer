from Unused.library import *
IMGDIR = PATH / 'static' / 'images'
def get_df_excel(df_name:str | None = 'list-pegawai - Copy') -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(PATH / f'{df_name}.xlsx', index_col=0)
    df['NIP'] = df['NIP'].apply(lambda x: x[1:])
    df.drop(columns=['Shift'], inplace=True)
    return df

def get_current_shift(df:pd.DataFrame) -> pd.DataFrame:
    #get current shift data
    now: str = datetime.now().strftime('%H:%M:%S')
    hours_now: str = now.split(':')[0]
    # df = df[df['Shift'] >= int(hours_now)]
    return_df: list[dict] = []
    for i in range(6):
        return_df.append(df.iloc[-i].to_dict())
    new_df: pd.DataFrame = pd.DataFrame(return_df)
    return new_df

def get_filename_for_show(name):
    try:
        # st.write(get_path)
        name:list = str(next(IMGDIR.glob(f'{name}.*')))
        # st.write(name)
        return name.split('\\')[-1]
    except:
        raise ValueError

def get_image(location: str) -> Image:
    # st.write(location)
    image = Image.open(os.path.join(IMGDIR, location))
    return image

def save_image(file_uploaded, name):
    if file_uploaded != '':
        file_uploaded.name = name + '.' + file_uploaded.name.split('.')[-1]
        with open(os.path.join(IMGDIR,file_uploaded.name),"wb") as f:
            f.write(file_uploaded.getbuffer())