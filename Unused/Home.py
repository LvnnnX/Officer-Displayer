from Unused.library import *
import Home.ofd as ofd
import Home.ofsettings as settings

if __name__ == '__main__':
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=[
                'Officer On Duty',
                'Officer Settings'
            ],
            icons=[
                'file-person',
                'person-fill-gear'
            ],
            menu_icon='cast',
            default_index=0,
            orientation='vertical',
        )

if selected == 'Officer On Duty':
    ofd.start()
else:
    settings.start()