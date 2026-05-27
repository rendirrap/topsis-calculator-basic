import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="TOPSIS Calculator - Decision Radar Replica",
    page_icon="📊",
    layout="wide"
)

# 2. CUSTOM CSS - REPLIKASI MATERIAL DESIGN LANGUAGE & ENTERPRISE LOOK
st.markdown("""
    <style>
    /* Global Styles (Roboto / Segoe UI Font) */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        background-color: #FAFAFA;
        color: #212121;
    }
    
    /* Navigation Bar Navy (#1A237E) */
    .navbar-navy {
        background-color: #1A237E;
        padding: 18px 25px;
        border-radius: 4px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Material Design Card Elevation */
    .material-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    /* Section Headings */
    .section-title {
        font-size: 18px;
        font-weight: 500;
        color: #1A237E;
        margin-bottom: 15px;
        border-bottom: 1px solid #E0E0E0;
        padding-bottom: 8px;
    }

    /* Kustomisasi tombol Streamlit agar presisi Flat/Rounded */
    div.stButton > button {
        border-radius: 4px !important;
        font-weight: 500 !important;
    }
    
    /* Custom Styling untuk Winner Card yang Keren (Bukan Balon) */
    .winner-box {
        background: linear-gradient(135deg, #1A237E 0%, #311B92 100%);
        color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(26, 35, 126, 0.2);
        text-align: center;
        margin-bottom: 25px;
    }
    .winner-title {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.8;
        margin-bottom: 5px;
    }
    .winner-name {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .winner-score {
        font-size: 16px;
        opacity: 0.9;
        background: rgba(255, 255, 255, 0.15);
        padding: 6px 15px;
        border-radius: 20px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR TOP HEADER ---
st.markdown("""
<div class="navbar-navy">
    <h3 style='margin:0; font-weight:500; color:white; font-size:22px;'>📊 TOPSIS Calculator</h3>
    <p style='margin:4px 0 0 0; opacity:0.7; font-size:13px;'>Calculate the ideal positive and negative solutions for multi-criteria decisions.</p>
</div>
""", unsafe_allow_html=True)


# 3. INITIALIZATION DATA STATE
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
# KOMPONEN 1: DATA ENTRY - CRITERIA & ALTERNATIVES
# ==========================================
col_panel_left, col_panel_right = st.columns(2)

# --- PANEL KIRI: LIST KRITERIA DINAMIS ---
with col_panel_left:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Criteria Setup</div>', unsafe_allow_html=True)
    
    lbl1, lbl2, lbl3, _ = st.columns([4, 3, 3, 1])
    lbl1.caption("Criteria Name")
    lbl2.caption("Weight")
    lbl3.caption("Type")
    
    updated_c_list = []
    for idx, crit in enumerate(st.session_state.c_list):
        c_cols = st.columns([4, 3, 3, 1])
        
        c_name = c_cols[0].text_input(f"c_n_{idx}", value=crit["name"], label_visibility="collapsed", key=f"crit_name_key_{idx}")
        c_weight = c_cols[1].number_input(f"c_w_{idx}", value=float(crit["weight"]), step=0.05, format="%.2f", label_visibility="collapsed", key=f"crit_weight_key_{idx}")
        t_idx = 0 if crit["type"] == "Benefit" else 1
        c_type = c_cols[2].selectbox(f"c_t_{idx}", ["Benefit", "Cost"], index=t_idx, label_visibility="collapsed", key=f"crit_type_key_{idx}")
        
        if c_cols[3].button("❌", key=f"del_c_{idx}"):
            if len(st.session_state.c_list) > 1:
                st.session_state.c_list.pop(idx)
                st.rerun()
                
        updated_c_list.append({"name": c_name, "weight": c_weight, "type": c_type})
    
    st.session_state.c_list = updated_c_list
    
    if st.button("➕ Add Criteria", type="secondary"):
        new_id = len(st.session_state.c_list) + 1
        st.session_state.c_list.append({"name": f"Kriteria C{new_id}", "weight": 0.0, "type": "Benefit"})
        st.rerun()
        
    total_w = sum([c["weight"] for c in st.session_state.c_list])
    if not np.isclose(total_w, 1.0):
        st.warning(f"⚠️ Total Weight: {total_w:.2f} (Must equal 1.00)")
    else:
        st.success("✅ Weights equal 1.00")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL KANAN: LIST ALTERNATIF DINAMIS ---
with col_panel_right:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏢 Alternatives Setup</div>', unsafe_allow_html=True)
    
    updated_a_list = []
    for idx, alt in enumerate(st.session_state.a_list):
        a_cols = st.columns([9, 1])
        
        a_name = a_cols[0].text_input(f"alt_{idx}", value=alt, label_visibility="collapsed", key=f"alt_name_key_{idx}")
        
        if a_cols[1].button("❌", key=f"del_a_{idx}"):
            if len(st.session_state.a_list) > 1:
                st.session_state.a_list.pop(idx)
                st.rerun()
                
        updated_a_list.append(a_name)
        
    st.session_state.a_list = updated_a_list
    
    if st.button("➕ Add Alternative", type="secondary"):
        new_char = chr(65 + len(st.session_state.a_list)) if len(st.session_state.a_list) < 26 else str(len(st.session_state.a_list)+1)
        st.session_state.a_list.append(f"Alternatif {new_char}")
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# KOMPONEN 2: MATRIKS KEPUTUSAN (X) DINAMIS
# ==========================================
st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Decision Matrix Table (X)</div>', unsafe_allow_html=True)

cols_layout = st.columns([2] + [1] * len(st.session_state.c_list))
cols_layout[0].markdown("**Alternative / Criteria**")

for c_idx, crit in enumerate(st.session_state.c_list):
    cols_layout[c_idx + 1].markdown(f"<p style='text-align:center; margin:0; font-weight:bold;'>{crit['name']}<br><span style='font-size:11px; font-weight:normal; opacity:0.6;'>({crit['type']})</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:12px 0; border-color:#E0E0E0;'>", unsafe_allow_html=True)

for a_idx, alt in enumerate(st.session_state.a_list):
    row_layout = st.columns([2] + [1] * len(st.session_state.c_list))
    row_layout[0].markdown(f"<p style='margin-top:8px; font-weight:500;'>{alt}</p>", unsafe_allow_html=True)
    
    for c_idx, crit in enumerate(st.session_state.c_list):
        cell_key = (alt, crit["name"])
        val_default = st.session_state.matrix_cells.get(cell_key, 0.0)
        
        with row_layout[c_idx + 1]:
            new_val = st.number_input(
                f"cell_{a_idx}_{c_idx}", 
                value=float(val_default), 
                min_value=0.0, 
                step=1.0, 
                label_visibility="collapsed", 
                key=f"input_matrix_cell_{alt}_{crit['name']}"
            )
            st.session_state.matrix_cells[cell_key] = new_val

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# KOMPONEN 3: CORE TOPSIS MATHEMATICS ENGINE
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
# KOMPONEN 4: TOMBOL EKSEKUSI & HASIL AKHIR
# ==========================================
_, center_btn_col, _ = st.columns([1, 1, 1])
with center_btn_col:
    btn_compute = st.button("🚀 COMPUTE", use_container_width=True, type="primary")

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
    
    with st.status("Menginisialisasi Algoritma Komputasi...", expanded=True) as status:
        st.write("🔄 Mentransformasi Matriks Keputusan...")
        time.sleep(0.2)
        st.write("📐 Menghitung Jarak Solusi Ideal Positif & Negatif...")
        time.sleep(0.2)
        status.update(label="Komputasi Selesai Sukses!", state="complete", expanded=False)
        
    st.toast('Kalkulasi Berhasil Diperbarui!', icon='✅')
    
    # Jalankan Engine Perhitungan
    R_mat, Y_mat, A_p, A_n, D_p, D_n, V_score = run_topsis_calculation(X_matrix, W_vector, t_vector)
    
    df_ranking = pd.DataFrame({
        'Alternative': st.session_state.a_list,
        'D+ (Ideal Positive)': D_p,
        'D- (Ideal Negative)': D_n,
        'Closeness Coefficient (V)': V_score
    }).sort_values(by='Closeness Coefficient (V)', ascending=False).reset_index(drop=True)
    
    df_ranking.index = df_ranking.index + 1
    df_ranking.index.name = 'Rank'
    
    best_alt = df_ranking.iloc[0]['Alternative']
    best_score = df_ranking.iloc[0]['Closeness Coefficient (V)']
    
    # Tampilan Banner Pemenang
    st.markdown(f"""
    <div class="winner-box">
        <div class="winner-title">🏆 Rekomendasi Solusi Optimal</div>
        <div class="winner-name">{best_alt}</div>
        <div class="winner-score">Nilai Kedekatan Relatif (V) = {best_score:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🌟 REPLIKASI CHART PLOTLY INDEPENDEN (Persis Gambar Pengguna)
    st.write("")
    st.markdown("**Visual Closeness Coefficient Ranking Chart:**")
    
    # Membuat plot garis interaktif menggunakan Plotly Graph Objects
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ranking['Alternative'],
        y=df_ranking['Closeness Coefficient (V)'],
        mode='lines+markers',
        line=dict(color='#1A237E', width=3),
        marker=dict(size=10, color='#1A237E'),
        name='Closeness Coefficient'
    ))
    
    fig.update_layout(
        xaxis_title="Alternative",
        yaxis_title="Closeness Coefficient (V)",
        yaxis=dict(range=[0, 1.05], dtick=0.1, gridcolor='#E0E0E0'),
        xaxis=dict(gridcolor='#F0F0F0'),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=40),
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 🌟 TABEL DENGAN HIGHLIGHT BARIS TERBAIK (Full Green Row Highlight)
    st.write("")
    st.markdown("**Official Multi-Criteria Ranking Table:**")
    
    def highlight_row(row):
        # Jika nilai baris alternatif sama dengan alternatif terbaik, beri warna background hijau sage
        if row['Alternative'] == best_alt:
            return ['background-color: #D1FAE5'] * len(row)
        return [''] * len(row)
        
    st.dataframe(
        df_ranking.style.apply(highlight_row, axis=1)
        .format({'D+ (Ideal Positive)': '{:.4f}', 'D- (Ideal Negative)': '{:.4f}', 'Closeness Coefficient (V)': '{:.4f}'}),
        use_container_width=True
    )
    
    # DOWNLOAD DATA REPORT
    csv_report = df_ranking.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Export Report to CSV",
        data=csv_report,
        file_name='topsis_decision_radar_report.csv',
        mime='text/csv'
    )
    
    # TRANSPARANSI PROSES MATEMATIKA (AUDIT LOG)
    st.write("")
    with st.expander("🔍 Step-by-Step Mathematical Computation Matrix Log"):
        tb1, tb2, tb3 = st.tabs(["1. Normalized Vector (R)", "2. Weighted Matrix (Y)", "3. Extreme Bounds (A+ / A-)"])
        with tb1:
            st.dataframe(pd.DataFrame(R_mat, columns=c_names_list, index=st.session_state.a_list).style.format("{:.4f}"), use_container_width=True)
        with tb2:
            st.dataframe(pd.DataFrame(Y_mat, columns=c_names_list, index=st.session_state.a_list).style.format("{:.4f}"), use_container_width=True)
        with tb3:
            st.dataframe(pd.DataFrame([A_p, A_n], columns=c_names_list, index=['A+ (Positive Vector)', 'A- (Negative Vector)']).style.format("{:.4f}"), use_container_width=True)