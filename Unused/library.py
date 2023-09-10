from datetime import datetime, timedelta
from docx.shared import Mm
from PIL import Image
import os
import pandas as pd
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

PATH = Path(__file__).parent