import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="TOPSIS Calculator - Responsive Multi-Device",
    page_icon="📊",
    layout="wide"  # Menggunakan mode wide agar fleksibel dari PC sampai HP
)

# 2. ADVANCED CSS - RESPONSIVE LAYOUT FOR WEB, TABLET, & MOBILE
st.markdown("""
    <style>
    /* --- GLOBAL STYLES --- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* --- NAVIGATION BAR (NAVY) --- */
    .navbar-navy {
        background-color: #1A237E;
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* --- MATERIAL DESIGN CARD ELEVATION --- */
    .material-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 25px;
    }
    
    /* --- SECTION TITLE --- */
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1A237E;
        margin-bottom: 18px;
        border-bottom: 2px solid #E8EAF6;
        padding-bottom: 8px;
    }
    
    /* --- WINNER BOX GRADIENT --- */
    .winner-box {
        background: linear-gradient(135deg, #1A237E 0%, #311B92 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(26, 35, 126, 0.15);
        text-align: center;
        margin-bottom: 30px;
    }
    .winner-title {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        opacity: 0.85;
        margin-bottom: 8px;
    }
    .winner-name {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 12px;
        line-height: 1.2;
    }
    .winner-score {
        font-size: 15px;
        opacity: 0.95;
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 30px;
        display: inline-block;
    }

    /* ================================================================= */
    /* 📱 RESPONSIVE MEDIA QUERIES (HP, TABLET, WEB)                   */
    /* ================================================================= */
    
    /* 1. LAYAR SMARTPHONE / HP (Maksimal 640px) */
    @media (max-width: 640px) {
        /* Memaksimalkan area baca di HP dengan mengecilkan padding utama Streamlit */
        .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
            padding-top: 1rem !important;
        }
        .material-card {
            padding: 16px;
            margin-bottom: 15px;
        }
        .winner-name {
            font-size: 24px;
        }
        /* Membuat input form di HP memiliki jarak ketuk (touch target) yang lega */
        div[data-testid="stDataFrame"] {
            width: 100% !important;
        }
    }
    
    /* 2. LAYAR TABLET (641px sampai 1024px) */
    @media (min-width: 641px) and (max-width: 1024px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .winner-name {
            font-size: 28px;
        }
    }
    
    /* 3. LAYAR WEB / DESKTOP PC (Minimal 1025px) */
    @media (min-width: 1025px) {
        .block-container {
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR HEADER ---
st.markdown("""
<div class="navbar-navy">
    <h3 style='margin:0; font-weight:600; color:white; font-size:22px;'>📊 TOPSIS Multi-Criteria Calculator</h3>
    <p style='margin:6px 0 0 0; opacity:0.8; font-size:13px;'>Auto-responsive layout optimized for Mobile, Tablet, and Desktop Web.</p>
</div>
""", unsafe_allow_html=True)


# 3. DATA STATE MANAGEMENT
if 'c_list' not in st.session_state:
    st.session_state.c_list = [
        {"name": "Harga (C1)", "weight": 0.40, "type": "Cost"},
        {"name": "Kualitas (C2)", "weight": 0.40, "type": "Benefit"},
        {"name": "Pelayanan (C3)", "weight": 0.20, "type": "Benefit"}
    ]
if 'a_list' not in st.session_state:
    st.session_state.a_list = ["Alternatif A", "Alternatif B", "Alternatif C"]

if 'matrix_cells' not in st.session_state:
    st.session_state.matrix_cells = {
        ("Alternatif A", "Harga (C1)"): 80.0, ("Alternatif A", "Kualitas (C2)"): 90.0, ("Alternatif A", "Pelayanan (C3)"): 70.0,
        ("Alternatif B", "Harga (C1)"): 70.0, ("Alternatif B", "Kualitas (C2)"): 85.0, ("Alternatif B", "Pelayanan (C3)"): 80.0,
        ("Alternatif C", "Harga (C1)"): 90.0, ("Alternatif C", "Kualitas (C2)"): 75.0, ("Alternatif C", "Pelayanan (C3)"): 85.0,
    }


# ==========================================
# PANEL DATA ENTRY (RESPONSIF: 2 KOLOM DI WEB, 1 KOLOM DI HP)
# ==========================================
# Di HP, objek st.columns([1, 1]) otomatis ditumpuk vertikal jika ruang tidak cukup
col_panel_left, col_panel_right = st.columns([1, 1])

# --- PANEL KRITERIA ---
with col_panel_left:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Setup Kriteria</div>', unsafe_allow_html=True)
    
    updated_c_list = []
    for idx, crit in enumerate(st.session_state.c_list):
        # Membagi kolom input internal kriteria agar proporsional di layar manapun
        c_cols = st.columns([4, 3, 3, 1])
        
        c_name = c_cols[0].text_input("Nama Kriteria", value=crit["name"], label_visibility="collapsed", key=f"crit_name_{idx}")
        c_weight = c_cols[1].number_input("Bobot", value=float(crit["weight"]), step=0.05, format="%.2f", label_visibility="collapsed", key=f"crit_weight_{idx}")
        t_idx = 0 if crit["type"] == "Benefit" else 1
        c_type = c_cols[2].selectbox("Jenis", ["Benefit", "Cost"], index=t_idx, label_visibility="collapsed", key=f"crit_type_{idx}")
        
        if c_cols[3].button("❌", key=f"del_c_{idx}"):
            if len(st.session_state.c_list) > 1:
                st.session_state.c_list.pop(idx)
                st.rerun()
                
        updated_c_list.append({"name": c_name, "weight": c_weight, "type": c_type})
    
    st.session_state.c_list = updated_c_list
    
    if st.button("➕ Tambah Kriteria", type="secondary", use_container_width="always"):
        new_id = len(st.session_state.c_list) + 1
        st.session_state.c_list.append({"name": f"Kriteria C{new_id}", "weight": 0.0, "type": "Benefit"})
        st.rerun()
        
    total_w = sum([c["weight"] for c in st.session_state.c_list])
    if not np.isclose(total_w, 1.0):
        st.warning(f"⚠️ Total Bobot: {total_w:.2f} (Wajib berjumlah 1.00)")
    else:
        st.success("✅ Akumulasi bobot tepat 1.00")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL ALTERNATIF ---
with col_panel_right:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏢 Setup Alternatif</div>', unsafe_allow_html=True)
    
    updated_a_list = []
    for idx, alt in enumerate(st.session_state.a_list):
        a_cols = st.columns([8, 2])
        a_name = a_cols[0].text_input("Nama Alternatif", value=alt, label_visibility="collapsed", key=f"alt_name_{idx}")
        
        if a_cols[1].button("❌", key=f"del_a_{idx}"):
            if len(st.session_state.a_list) > 1:
                st.session_state.a_list.pop(idx)
                st.rerun()
                
        updated_a_list.append(a_name)
        
    st.session_state.a_list = updated_a_list
    
    if st.button("➕ Tambah Alternatif", type="secondary", use_container_width="always"):
        new_char = chr(65 + len(st.session_state.a_list)) if len(st.session_state.a_list) < 26 else str(len(st.session_state.a_list)+1)
        st.session_state.a_list.append(f"Alternatif {new_char}")
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# MATRIKS KEPUTUSAN DINAMIS (BERADAPTASI OTOMATIS)
# ==========================================
st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Isi Nilai Matriks Keputusan (X)</div>', unsafe_allow_html=True)

for a_idx, alt in enumerate(st.session_state.a_list):
    st.markdown(f"🔹 **{alt}**")
    
    # Grid dinamis mengikuti jumlah kriteria yang aktif
    m_cols = st.columns(len(st.session_state.c_list))
    for c_idx, crit in enumerate(st.session_state.c_list):
        cell_key = (alt, crit["name"])
        val_default = st.session_state.matrix_cells.get(cell_key, 0.0)
        
        with m_cols[c_idx]:
            new_val = st.number_input(
                f"{crit['name']} ({crit['type'][:3]})", 
                value=float(val_default), 
                min_value=0.0, 
                step=1.0, 
                key=f"cell_{alt}_{crit['name']}"
            )
            st.session_state.matrix_cells[cell_key] = new_val
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# ENGINE MATEMATIKA TOPSIS Core
# ==========================================
def run_topsis_calculation(X, W, types):
    divider = np.sqrt(np.sum(X**2, axis=0))
    divider[divider == 0] = 1.0
    R = X / divider
    Y = R * W
    
    A_pos = np.zeros(X.shape[1])
    A_neg = np.zeros(X.shape[1])
    for j in range(X.shape[1]):
        if types[j].lower() == 'benefit':
            A_pos[j] = np.max(Y[:, j])
            A_neg[j] = np.min(Y[:, j])
        else:
            A_pos[j] = np.min(Y[:, j])
            A_neg[j] = np.max(Y[:, j])
            
    D_pos = np.sqrt(np.sum((Y - A_pos)**2, axis=1))
    D_neg = np.sqrt(np.sum((Y - A_neg)**2, axis=1))
    
    total_d = D_neg + D_pos
    total_d[total_d == 0] = 1.0
    V = D_neg / total_d
    
    return R, Y, A_pos, A_neg, D_pos, D_neg, V


# ==========================================
# EKSEKUSI DAN OUTPUT RESPONSIF (WEB, TABLET, HP)
# ==========================================
btn_compute = st.button("🚀 HITUNG SEKARANG", use_container_width="always", type="primary")

if btn_compute:
    X_rows = []
    for alt in st.session_state.a_list:
        row_vals = []
        for crit in st.session_state.c_list:
            row_vals.append(st.session_state.matrix_cells.get((alt, crit["name"]), 0.0))
        X_rows.append(row_vals)
        
    X_matrix = np.array(X_rows, dtype=float)
    W_vector = np.array([c["weight"] for c in st.session_state.c_list], dtype=float)
    t_vector = [c["type"] for c in st.session_state.c_list]
    c_names_list = [c["name"] for c in st.session_state.c_list]
    
    st.write("---")
    
    with st.status("Menghitung Algoritma TOPSIS...", expanded=False) as status:
        time.sleep(0.2)
        status.update(label="Kalkulasi Selesai!", state="complete")
        
    # Ambil hasil kalkulasi
    R_mat, Y_mat, A_p, A_n, D_p, D_n, V_score = run_topsis_calculation(X_matrix, W_vector, t_vector)
    
    df_ranking = pd.DataFrame({
        'Alternative': st.session_state.a_list,
        'D+ (Ideal Positif)': D_p,
        'D- (Ideal Negatif)': D_n,
        'Closeness Coefficient (V)': V_score
    }).sort_values(by='Closeness Coefficient (V)', ascending=False).reset_index(drop=True)
    
    df_ranking.index = df_ranking.index + 1
    df_ranking.index.name = 'Peringkat'
    
    best_alt = df_ranking.iloc[0]['Alternative']
    best_score = df_ranking.iloc[0]['Closeness Coefficient (V)']
    
    # 🏆 Banner Rekomendasi Utama (Responsif via CSS)
    st.markdown(f"""
    <div class="winner-box">
        <div class="winner-title">🏆 Solusi Alternatif Terbaik</div>
        <div class="winner-name">{best_alt}</div>
        <div class="winner-score">Nilai Kedekatan Relatif (V) = {best_score:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 📈 Chart Plotly Responsif Lintas Layar
    st.markdown("📈 **Grafik Nilai Kedekatan Kedekatan (V Score):**")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ranking['Alternative'],
        y=df_ranking['Closeness Coefficient (V)'],
        mode='lines+markers',
        line=dict(color='#1A237E', width=3),
        marker=dict(size=10, color='#1A237E'),
        name='Nilai V'
    ))
    
    fig.update_layout(
        yaxis=dict(range=[0, 1.05], dtick=0.2, gridcolor='#EAEAEA'),
        xaxis=dict(gridcolor='#F5F5F5'),
        plot_bgcolor='white',
        margin=dict(l=25, r=25, t=15, b=15),
        height=280,  # Tinggi ideal agar pas di layar HP tanpa scroll terlalu jauh
        hovermode="x unified"
    )
    # use_container_width="always" mengamankan grafik agar melebar proporsional mengikuti lebar kontainer alat
    st.plotly_chart(fig, use_container_width="always", config={'displayModeBar': False})
    
    # 📊 Tabel Hasil Akhir dengan Fitur Penanda Warna Baris Teratas
    st.markdown("📊 **Tabel Hasil Pemeringkatan Resmi:**")
    
    def highlight_best(row):
        if row['Alternative'] == best_alt:
            return ['background-color: #E8F5E9; font-weight: bold; color: #2E7D32'] * len(row)
        return [''] * len(row)
        
    st.dataframe(
        df_ranking.style.apply(highlight_best, axis=1)
        .format({'D+ (Ideal Positif)': '{:.4f}', 'D- (Ideal Negatif)': '{:.4f}', 'Closeness Coefficient (V)': '{:.4f}'}),
        use_container_width="always"
    )
    
    # 📥 Fitur Ekspor Data CSV (Lebar Penuh di HP)
    df_export = df_ranking.copy()
    csv_report = df_export.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Download Laporan Hasil (CSV)",
        data=csv_report,
        file_name='Laporan_TOPSIS_Responsive.csv',
        mime='text/csv',
        use_container_width="always"
    )
    
    # 🔍 Tab Log Matematika Audit Transparan
    st.write("")
    with st.expander("🔍 Log Langkah Perhitungan Matematis (Audit Data)"):
        t_b1, t_b2, t_b3 = st.tabs(["Matriks R (Normalisasi)", "Matriks Y (Terbobot)", "Nilai Solusi Ideal"])
        with t_b1:
            st.dataframe(pd.DataFrame(R_mat, columns=c_names_list, index=st.session_state.a_list).style.format("{:.4f}"), use_container_width="always")
        with t_b2:
            st.dataframe(pd.DataFrame(Y_mat, columns=c_names_list, index=st.session_state.a_list).style.format("{:.4f}"), use_container_width="always")
        with t_b3:
            st.dataframe(pd.DataFrame([A_p, A_n], columns=c_names_list, index=['A+ (Ideal Positif)', 'A- (Ideal Negatif)']).style.format("{:.4f}"), use_container_width="always")
