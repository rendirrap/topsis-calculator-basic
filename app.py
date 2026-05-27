import streamlit as st

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Online Calculator Replica",
    page_icon="🧮",
    layout="centered" # Menggunakan centered agar bentuk kalkulator tetap proporsional seperti aslinya
)

# 2. CUSTOM CSS - TAMPILAN RESPONSIF UNTUK HP, TABLET, DAN WEB
st.markdown("""
    <style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background-color: #F3F4F6;
    }
    
    /* Wadah Utama Kalkulator (Card) */
    .calc-container {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Layar Display Kalkulator */
    .calc-display {
        background-color: #050505;
        color: #00FF66;
        font-family: 'Courier New', Courier, monospace;
        text-align: right;
        padding: 15px;
        font-size: 32px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
        min-height: 70px;
        word-wrap: break-word;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
    }
    
    /* Modifikasi tombol default Streamlit agar menyerupai tombol fisik */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        margin: 5px 0px !important;
        transition: all 0.2s ease;
    }
    
    /* Warna khusus tombol Operator (Kuning/Oranye) */
    div.stButton > button[key^="btn_op_"], div.stButton > button[key="btn_sama_dengan"] {
        background-color: #D97706 !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button[key^="btn_op_"]:hover, div.stButton > button[key="btn_sama_dengan"]:hover {
        background-color: #F59E0B !important;
    }
    
    /* Warna khusus tombol Clear / Reset (Merah) */
    div.stButton > button[key="btn_clear"] {
        background-color: #DC2626 !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button[key="btn_clear"]:hover {
        background-color: #EF4444 !important;
    }

    /* 📱 MEDIA QUERIES UNTUK HP (Layar di bawah 640px) */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        div.stButton > button {
            height: 55px !important;
            font-size: 18px !important;
        }
        .calc-display {
            font-size: 26px;
            padding: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. MANAJEMEN STATE MEMORI KALKULATOR
if 'display_val' not in st.session_state:
    st.session_state.display_val = "0"
if 'reset_on_next_click' not in st.session_state:
    st.session_state.reset_on_next_click = False

# Fungsi Aksi ketika tombol ditekan
def press_key(key):
    if st.session_state.reset_on_next_click and key in ["0","1","2","3","4","5","6","7","8","9","."]:
        st.session_state.display_val = ""
    st.session_state.reset_on_next_click = False
    
    if st.session_state.display_val == "0" and key != ".":
        st.session_state.display_val = str(key)
    else:
        st.session_state.display_val += str(key)

def clear_display():
    st.session_state.display_val = "0"
    st.session_state.reset_on_next_click = False

def calculate_result():
    try:
        # Mengubah simbol visual perkalian dan pembagian ke operator Python asli
        expression = st.session_state.display_val.replace('×', '*').replace('÷', '/')
        # Evaluasi string matematika dengan aman
        result = eval(expression)
        
        # Format hasil agar tidak terlalu panjang jika berupa desimal pecahan
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 6)
            
        st.session_state.display_val = str(result)
    except ZeroDivisionError:
        st.session_state.display_val = "Error: Div by 0"
    except Exception:
        st.session_state.display_val = "Error"
    
    st.session_state.reset_on_next_click = True

# --- STRUKTUR WIDGET KALKULATOR ---
st.title("🧮 The Online Calculator")
st.write("Aplikasi kalkulator responsif yang menyesuaikan ukuran di HP, Tablet, dan Web PC.")

# Mulai pembungkus container kalkulator
st.markdown('<div class="calc-container">', unsafe_allow_html=True)

# Tampilan Layar Utama
st.markdown(f'<div class="calc-display">{st.session_state.display_val}</div>', unsafe_allow_html=True)

# Susunan Grid Tombol Kalkulator (4 Kolom)
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([1, 1, 1, 1])
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns([1, 1, 1, 1])
row3_col1, row3_col2, row3_col3, row3_col4 = st.columns([1, 1, 1, 1])
row4_col1, row4_col2, row4_col3, row4_col4 = st.columns([1, 1, 1, 1])
row5_col1, row5_col2, row5_col3, row5_col4 = st.columns([1, 1, 1, 1])

# --- BARIS 1 ---
with row1_col1:
    st.button("C", key="btn_clear", on_click=clear_display)
with row1_col2:
    if st.button("(", key="btn_kurung_buka"): press_key("(")
with row1_col3:
    if st.button(")", key="btn_kurung_tutup"): press_key(")")
with row1_col4:
    if st.button("÷", key="btn_op_bagi"): press_key("÷")

# --- BARIS 2 ---
with row2_col1:
    if st.button("7", key="btn_7"): press_key("7")
with row2_col2:
    if st.button("8", key="btn_8"): press_key("8")
with row2_col3:
    if st.button("9", key="btn_9"): press_key("9")
with row2_col4:
    if st.button("×", key="btn_op_kali"): press_key("×")

# --- BARIS 3 ---
with row3_col1:
    if st.button("4", key="btn_4"): press_key("4")
with row3_col2:
    if st.button("5", key="btn_5"): press_key("5")
with row3_col3:
    if st.button("6", key="btn_6"): press_key("6")
with row3_col4:
    if st.button("-", key="btn_op_kurang"): press_key("-")

# --- BARIS 4 ---
with row4_col1:
    if st.button("1", key="btn_1"): press_key("1")
with row4_col2:
    if st.button("2", key="btn_2"): press_key("2")
with row4_col3:
    if st.button("3", key="btn_3"): press_key("3")
with row4_col4:
    if st.button("+", key="btn_op_tambah"): press_key("+")

# --- BARIS 5 ---
with row5_col1:
    if st.button("0", key="btn_0"): press_key("0")
with row5_col2:
    if st.button(".", key="btn_titik"): press_key(".")
with row5_col3:
    if st.button("%", key="btn_persen"): press_key("/100")
with row5_col4:
    st.button("=", key="btn_sama_dengan", on_click=calculate_result)

# Penutup pembungkus container kalkulator
st.markdown('</div>', unsafe_allow_html=True)
