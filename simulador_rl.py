import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, LeaveOneOut

# ── CONFIGURACIÓ ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Milanta · Simulador de Pressupost",
    page_icon="🌿",
    layout="centered"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #F7F4EF;
        color: #3A3228;
    }
    .main { background-color: #F7F4EF; }
    
    /* Capçalera */
    .header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
        border-bottom: 1.5px solid #D6CFC4;
        margin-bottom: 2rem;
    }
    .header h1 {
        font-size: 1.6rem;
        font-weight: 600;
        color: #2D5A1B;
        letter-spacing: -0.3px;
        margin-bottom: 0.3rem;
    }
    .header p {
        font-size: 0.9rem;
        color: #7A7268;
        font-weight: 300;
        margin: 0;
    }

    /* Títols de secció */
    .sec-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #7A7268;
        margin-bottom: 0.8rem;
        margin-top: 1.8rem;
    }

    /* Inputs */
    .stSelectbox label, .stNumberInput label {
        font-size: 0.85rem !important;
        color: #5A5248 !important;
        font-weight: 400 !important;
    }
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6CFC4 !important;
        border-radius: 8px !important;
        color: #3A3228 !important;
        font-size: 0.9rem !important;
    }
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: #4A7C2F !important;
        box-shadow: 0 0 0 2px rgba(74,124,47,0.15) !important;
    }

    /* Botó */
    .stButton > button {
        width: 100%;
        background-color: #2D5A1B !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.2px;
        margin-top: 1.5rem;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #4A7C2F !important;
    }

    /* Resultats */
    .result-box {
        background-color: #FFFFFF;
        border: 1px solid #D6CFC4;
        border-radius: 14px;
        padding: 1.8rem 1.5rem;
        margin-top: 1.8rem;
    }
    .result-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #7A7268;
        margin-bottom: 0.3rem;
    }
    .result-value {
        font-size: 1.9rem;
        font-weight: 600;
        color: #2D5A1B;
        line-height: 1.1;
    }
    .result-sub {
        font-size: 0.8rem;
        color: #7A7268;
        margin-top: 0.2rem;
    }
    .result-mid {
        background-color: #F0F5EC;
        border: 1.5px solid #C5D9B8;
        border-radius: 14px;
        padding: 1.8rem 1.5rem;
        margin-top: 1.8rem;
        text-align: center;
    }
    .result-mid .result-value {
        font-size: 2.4rem;
    }

    /* Detall */
    .detail-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.875rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #EDE8E1;
        color: #5A5248;
    }
    .detail-row:last-child { border-bottom: none; }

    /* Divisor */
    hr { border-color: #D6CFC4 !important; }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: #ADA89F;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #D6CFC4;
    }

    /* Amagant elements streamlit */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── CAPÇALERA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>🌿 Simulador de Pressupost Orientatiu</h1>
    <p>Renaturalització de patis escolars · milanta.net</p>
</div>
""", unsafe_allow_html=True)

# ── MODEL ─────────────────────────────────────────────────────────────────────
@st.cache_data
def carregar_model():
    df = pd.read_excel("DADES GENERALS.xlsx")
    df.columns = df.columns.str.strip()

    label_mappings = {
        'complexitat':    {'baixa': 0, 'mitja': 1, 'alta': 2},
        'accessibilitat': {'bona': 0, 'limitada': 1, 'molt limitada': 2},
        'repicat':        {'no': 0, 'parcial': 1, 'total': 2},
        'maquina':        {'no': 0, 'si': 1},
    }
    for col, mapping in label_mappings.items():
        df[col + '_enc'] = df[col].map(mapping)

    tipologia_dummies = pd.get_dummies(df['tipologia'], prefix='tip')
    df = pd.concat([df, tipologia_dummies], axis=1)

    features = ['m²', 'complexitat_enc', 'accessibilitat_enc',
    'tip_combinat', 'tip_espai trobada', 'tip_moviment', 'tip_sorral']

    X = df[features]
    y = df['preu/m²']

    model = LinearRegression()
    model.fit(X, y)

    loo = LeaveOneOut()
    mae = -cross_val_score(model, X, y, cv=loo,
                           scoring='neg_mean_absolute_error').mean()

    return model, features, mae

model, features, mae = carregar_model()

# ── FORMULARI ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">Dades del projecte</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    m2           = st.number_input("Superfície (m²)", min_value=10, max_value=2000, value=150, step=10)
    complexitat  = st.selectbox("Complexitat", ["baixa", "mitja", "alta"])
    accessibilitat = st.selectbox("Accessibilitat", ["bona", "limitada", "molt limitada"])
with col2:
    tipologia    = st.selectbox("Tipologia", ["combinat", "espai trobada", "moviment", "sorral"])
    maquina      = st.selectbox("Màquina necessària", ["no", "si"])
    repicat      = st.selectbox("Repicat", ["no", "parcial", "total"])

calcular = st.button("Calcular pressupost orientatiu")

# ── CÀLCUL ────────────────────────────────────────────────────────────────────
if calcular:
    comp_enc = {'baixa': 0, 'mitja': 1, 'alta': 2}[complexitat]
    acc_enc  = {'bona': 0, 'limitada': 1, 'molt limitada': 2}[accessibilitat]
    maq_enc  = {'no': 0, 'si': 1}[maquina]
    rep_enc  = {'no': 0, 'parcial': 1, 'total': 2}[repicat]

    tip_combinat      = 1 if tipologia == 'combinat' else 0
    tip_espai_trobada = 1 if tipologia == 'espai trobada' else 0
    tip_moviment      = 1 if tipologia == 'moviment' else 0
    tip_sorral        = 1 if tipologia == 'sorral' else 0

    X_nou = pd.DataFrame([[m2, comp_enc, acc_enc,
                        tip_combinat, tip_espai_trobada,
                        tip_moviment, tip_sorral]],
                      columns=features)

    preu_m2 = model.predict(X_nou)[0]

    # Costos addicionals
    if maquina == 'si':
        cost_maquina = 1000 if m2 < 50 else 1600 if m2 <= 100 else 2200
    else:
        cost_maquina = 0

    area_repicat = m2 * 0.40 if repicat == 'parcial' else m2 if repicat == 'total' else 0
    cost_repicat = round((area_repicat * 0.30 * 1.4 / 0.75) * 55) if area_repicat > 0 else 0

    cost_base  = round(preu_m2 * m2)
    total      = cost_base + cost_maquina + cost_repicat
    total_baix = round((preu_m2 - mae) * m2) + cost_maquina + cost_repicat
    total_alt  = round((preu_m2 + mae) * m2) + cost_maquina + cost_repicat

    # ── RESULTATS ────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title" style="margin-top:2rem">Pressupost orientatiu</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])

    with c1:
        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Estimació baixa</div>
            <div class="result-value">{total_baix:,.0f} €</div>
            <div class="result-sub">{(total_baix/m2):.0f} €/m²</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="result-mid">
            <div class="result-label">Estimació mitjana</div>
            <div class="result-value">{total:,.0f} €</div>
            <div class="result-sub">{preu_m2:.0f} €/m² · {m2} m²</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Estimació alta</div>
            <div class="result-value">{total_alt:,.0f} €</div>
            <div class="result-sub">{(total_alt/m2):.0f} €/m²</div>
        </div>""", unsafe_allow_html=True)

    # Detall
    st.markdown('<div class="sec-title" style="margin-top:2rem">Detall del càlcul</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-box">
        <div class="detail-row"><span>Cost base d'obra</span><span>{cost_base:,.0f} €</span></div>
        <div class="detail-row"><span>Cost màquina</span><span>{cost_maquina:,.0f} €</span></div>
        <div class="detail-row"><span>Cost repicat i retirada</span><span>{cost_repicat:,.0f} €</span></div>
        <div class="detail-row" style="font-weight:500;color:#2D5A1B">
            <span>Total estimació mitjana</span><span>{total:,.0f} €</span>
        </div>
        <div class="detail-row" style="border-bottom:none;font-size:0.8rem;color:#ADA89F">
            <span>Marge del model (±MAE)</span><span>±{mae:.0f} €/m²</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Pressupost orientatiu basat en projectes reals · 
    Com més projectes s'introdueixin a la base de dades, més fiable serà l'estimació
</div>
""", unsafe_allow_html=True)