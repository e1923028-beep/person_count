import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh
import base64, pathlib

st.set_page_config(page_title="人数カウント × ゲーム", layout="wide")
st_autorefresh(interval=5000, key="data_refresh")

SPREADSHEET_KEY = "12_rwsKyulxeDArXlz6lLPrdD8pMt8hS0isIMH8ahcJw"
WORKSHEET_NAME = "シート1"

@st.cache_resource
def init_gspread():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    # st.secrets ではなく、元の JSON ファイルを読み込む方式に戻す
    SERVICE_ACCOUNT_FILE = 'rosy-proposal-464707-i4-80dbecc88cca.json'
    
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes
    )
    return gspread.authorize(credentials)

# ---- レイアウト ----
col1, col2 = st.columns([1, 2])

with col1:
    st.title("リアルタイム人数カウント")
    try:
        gc = init_gspread()
        sh = gc.open_by_key(SPREADSHEET_KEY)
        worksheet = sh.worksheet(WORKSHEET_NAME)
        cell_value = worksheet.acell('B2').value
        st.metric(label="現在の検出人数", value=f"{cell_value} 人")
        st.info(f"この人数（{cell_value}球）でゲームが遊べます →")
    except Exception as e:
        st.error(f"データ取得エラー: {e}")

with col2:
    st.subheader("🎮 人数シューティングゲーム")
    # GodotをHTML5でエクスポートしたファイルのパスを指定
    game_path = pathlib.Path("./export/index.html")
    if game_path.exists():
        st.components.v1.html(
            game_path.read_text(encoding="utf-8"),
            height=600,
            scrolling=False
        )
    else:
        st.warning("ゲームファイルが見つかりません。`./export/index.html` にGodotのHTML5エクスポートを配置してください。")