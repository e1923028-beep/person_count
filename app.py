import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. ページ設定と自動更新（YOLOの送信間隔に合わせて5秒更新）
# ==========================================
st.set_page_config(page_title="人数カウントダッシュボード", layout="centered")

# 5000ミリ秒（5秒）ごとにページを自動リロードする
st_autorefresh(interval=5000, key="data_refresh")

# ==========================================
# 2. スプレッドシートの認証設定
# ==========================================
# 取得したJSONキーのパスを指定してください
# ==========================================
# 2. スプレッドシートの認証設定（Secretsから読み込む版）
# ==========================================
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
# ==========================================
# 3. 画面の構築とデータ取得
# ==========================================
st.title("リアルタイム人数カウント")

try:
    gc = init_gspread()
    sh = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = sh.worksheet(WORKSHEET_NAME)

    # Makeが更新しているセルを指定して値を取得（例としてA2セルを指定）
    # ※ Make側でどのセルに追記/更新しているかに合わせて変更してください
    cell_value = worksheet.acell('B2').value
    
    # 指標を大きく表示
    st.metric(label="現在の検出人数", value=f"{cell_value} 人")
    
    st.success("")

except Exception as e:
    st.error(f"データ取得エラー: {e}")