from Unused.process import *

def start() -> None:    
    st.markdown(f"<h1 style='text-align:center'> Officer On Duty </h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Current Officer On Duty</p>", unsafe_allow_html=True)
    
    data: pd.DataFrame = get_df_excel()
    st.dataframe(get_current_shift(data), width=Mm(1))
    
    edit_menu: str = st.radio('Edit Menu', options=['Add', 'Delete'])
    
    if(edit_menu == 'Add'):
        # many:int = st.number_input('How many officers do you want to add?', min_value=1, max_value=10, value=1)
        _namapgw:str = st.selectbox('Nama Pegawai', options=data['Nama'].sort_values(ascending=True), key=f'pgw-1')
        with st.form(key='Add-Officer', clear_on_submit=True):
            # for x in range(many):
            col1,col2 = st.columns(2, gap='medium')
            # images = get_image('template_photo.jpeg')
            try:
                # st.write(_namapgw)
                images = get_filename_for_show(_namapgw)
                images = get_image(images)
                # st.write(_namapgw)
                pass
            except ValueError as e:
                images:Image = get_image('template_photo.jpeg')
                # st.write(e)
                pass
            col1.image(images, width=180)
            col2.text_input('NIP', key=f'nip-1', value=data[data['Nama'] == _namapgw]['NIP'].values[0], disabled=True, label_visibility='visible')
            # photo_input = col2.file_uploader('Change Photo', key=f'photo-1', type=['png', 'jpg', 'jpeg'])
            
            add_submitbtn = st.form_submit_button(label='Add')
        
        if add_submitbtn:
            # if photo_input != None:
            #     save_image(photo_input, _namapgw)
            data = data.iloc[-1]
            st.experimental_rerun()
                
    elif edit_menu == 'Delete':
        _namapgw:str = st.selectbox('Nama Pegawai', options=data['Nama'].sort_values(ascending=True), key=f'pgw-1')
        with st.form(key='Delete-Officer', clear_on_submit=True):
            # for x in range(many):
            col1,col2 = st.columns(2, gap='medium')
            # images = get_image('template_photo.jpeg')
            try:
                # st.write(_namapgw)
                images = get_filename_for_show(_namapgw)
                images = get_image(images)
                # st.write(_namapgw)
                pass
            except ValueError as e:
                images:Image = get_image('template_photo.jpeg')
                # st.write(e)
                pass
            col1.image(images, width=180)
            col2.text_input('NIP', key=f'nip-1', value=data[data['Nama'] == _namapgw]['NIP'].values[0], disabled=True, label_visibility='visible')
            # photo_input = col2.file_uploader('Change Photo', key=f'photo-1', type=['png', 'jpg', 'jpeg'])
            
            add_submitbtn = st.form_submit_button(label='Delete')
        
        if add_submitbtn:
            # if photo_input != None:
            #     save_image(photo_input, _namapgw)
            st.experimental_rerun()
    
    with st.form(key='Edit-Officer'):
        pass
    
