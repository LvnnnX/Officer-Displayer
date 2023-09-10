from Unused.process import *

def start() -> None:
    pass   
    st.markdown(f'<h1 style="text-align:center"> Select Officer To Edit </h1>', unsafe_allow_html=True)
    data_pgw:pd.DataFrame = get_df_excel()
    selected = st.selectbox('', options=data_pgw['Nama'].sort_values(ascending=True), key='pgw-1', label_visibility='collapsed')
    
    with st.form(key='Menu-pgw', clear_on_submit=True):
        pass
        col1,col2 = st.columns(2, gap='medium')
        try:
            images = get_filename_for_show(selected)
            images = get_image(images)
        except ValueError as e:
            images:Image = get_image('template_photo.jpeg')
            pass
        col1.image(images, width=180)
        col2.text_input('NIP', key=f'nip-1', value=data_pgw[data_pgw['Nama'] == selected]['NIP'].values[0], disabled=True, label_visibility='visible')
        photo_input = col2.file_uploader('Change Photo', key=f'photo-1', type=['png', 'jpg', 'jpeg'])

        edit_submitbtn = st.form_submit_button(label='Edit')
        
    if edit_submitbtn:
        if photo_input != None:
            save_image(photo_input, selected)
        st.experimental_rerun()

