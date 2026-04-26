import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh
import base64, pathlib
import streamlit.components.v1 as components

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
     # ファイルからではなく、st.secrets から直接情報を読み込む
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes
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
    st.title("プーさんのホームランダービー⚾")
    
    # さっきGitHub Pagesで作ったURL + exportフォルダ + index.html
    # URLの末尾に「?count=人数」をつけてデータを渡す
    base_url = "https://e1923028-beep.github.io/person_count/game/index.html"
    game_url = f"{base_url}?count={cell_value}"
    
    # URLを指定してiframeで埋め込む
    components.iframe(game_url, width=800, height=600)
# with col2:
#     st.subheader("🎮 人数シューティングゲーム")
#     # GodotをHTML5でエクスポートしたファイルのパスを指定
#     game_path = pathlib.Path("./game/index.html")
#     if game_path.exists():
#         st.components.v1.html(
#             game_path.read_text(encoding="utf-8"),
#             height=600,
#             scrolling=False
#         )
#     else:
#         st.warning("ゲームファイルが見つかりません。`./export/index.html` にGodotのHTML5エクスポートを配置してください。")