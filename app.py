import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Set page configuration
st.set_page_config(
    page_title="NSM FRP Shear Resistance",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look (Light Mode) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@300;400;600;700&display=swap');

    /* Variables */
    :root {
        --primary: #0066CC; /* Deep Blue */
        --secondary: #00E5FF; /* Cyan */
        --accent: #FF1744; /* Red */
        --bg-light: #F8F9FA; /* Light Gray/White */
        --card-bg: rgba(255, 255, 255, 0.8);
        --text-main: #1A202C; /* Dark Gray/Black */
        --text-muted: #64748B; /* Slate Gray */
        --glass-border: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* Global Reset & Typography */
    .stApp {
        background-color: var(--bg-light);
        background-image: radial-gradient(circle at 50% 0%, rgba(0, 102, 204, 0.05) 0%, transparent 50%);
        color: var(--text-main);
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #0F172A;
    }
    
    p, label, .stMarkdown {
        font-family: 'Outfit', sans-serif;
        color: var(--text-main);
    }

    /* Custom Header */
    .main-header {
        padding: 2rem 0;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: var(--glass-border);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #0066CC 0%, #2979FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        color: var(--text-muted);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: var(--glass-border);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--primary);
    }

    /* Cards / Containers */
    .css-1r6slb0, .stVerticalBlock {
        gap: 1.5rem;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', monospace;
        font-size: 2.5rem !important;
        color: var(--primary) !important;
        text-shadow: none;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(0,0,0,0.03);
        border-radius: 8px;
        color: var(--text-muted);
        border: none;
        padding: 0 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 102, 204, 0.1) !important;
        color: var(--primary) !important;
        border: 1px solid rgba(0, 102, 204, 0.2) !important;
    }

    /* Latex */
    .katex {
        font-size: 1.1em;
        color: #334155;
    }
    
    /* Plotly/Charts background */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>NSM FRP Shear Resistance</h1>
    <p>Reliability-Based Design Model for RC Beams • Bars & Laminates</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Inputs ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Group 1: System
    with st.expander("Strengthening System", expanded=True):
        reinforcement_type = st.radio("Type", ["Bars", "Laminates"], index=1, label_visibility="collapsed") # Default to Laminates
        
    # Group 2: Geometry
    with st.expander("Geometry", expanded=True):
        cross_section_type = st.radio("Cross Section", ["Rectangular", "T-Beam"], index=1, horizontal=True)
        
        col_g1, col_g2 = st.columns(2)
        b_w = col_g1.number_input("$b_w$ [mm]", value=180, step=10)
        d_s = col_g2.number_input("$d_s$ [mm]", value=360, step=10)
        
        if cross_section_type == "T-Beam":
            b_fl = col_g1.number_input("$b_{fl}$ [mm]", value=450, step=10)
            h_fl = col_g2.number_input("$h_{fl}$ [mm]", value=100, step=10)
        else:
            b_fl = b_w
            h_fl = 0.0
        
    # Group 3: Materials
    with st.expander("Materials", expanded=False):
        f_cm = st.slider("$f_{cm}$ [MPa]", 20.0, 100.0, 59.4, 0.1)
        f_swy = st.slider("$f_{swy}$ [MPa]", 200, 800, 551)
        E_f = st.slider("$E_f$ [MPa]", 100000, 300000, 174300, 100)
        
    # Group 4: Reinforcement
    with st.expander("Reinforcement Ratios", expanded=False):
        rho_sw = st.slider("$\\rho_{sw}$", 0.0, 0.01, 0.001, 0.0001, format="%.4f") # 0.1%
        rho_slT = st.slider("$\\rho_{slT}$", 0.001, 0.04, 0.031, 0.001, format="%.3f") # 3.1%
        rho_f = st.slider("$\\rho_f$", 0.0001, 0.01, 0.0008, 0.0001, format="%.4f") # 0.082% approx 0.0008
        
    # Group 5: NSM Config
    with st.expander("NSM Details", expanded=False):
        alpha_f_deg = st.slider("$\\alpha_f$ [deg]", 45, 90, 90, 5)
        h_f = st.slider("$h_f$ [mm]", 100, 1000, 300, 10)
        d_g = st.slider("Groove Depth ($d_g$) [mm]", 5, 40, 14, 1) # d_b = 14

# --- Calculations (Logic remains same) ---
alpha_f = math.radians(alpha_f_deg)
L_Rf = h_f / (4 * math.sin(alpha_f))

# 1. Concrete
n_c = min((b_fl - b_w) / h_fl, 3) if h_fl > 0 else 0
k_f = min(1 + (n_c * h_fl**2) / (b_w * d_s), 1.5)

if reinforcement_type == "Laminates":
    theta_deg = 0.61 * (40.5 * rho_slT**(-0.05) + 1.35 * (f_swy * rho_sw)**2.8) * \
                (1 + 0.001 * f_cm) * (1 + 0.00043 * L_Rf) * (1 + 0.00005 * rho_f * E_f)
else:
    theta_deg = 3.85 * (5.8 * rho_slT**(-0.08) + 0.32 * (f_swy * rho_sw)**1.7) * \
                (1 + 0.00024 * f_cm) * (1 + 0.00067 * L_Rf) * (1 + 0.000012 * rho_f * E_f)
theta = math.radians(theta_deg)

if reinforcement_type == "Laminates":
    k_v = 0.69 * 10**5 * theta_deg**(-3.6)
else:
    k_v = 1.1 * 10**5 * theta_deg**(-3.8)

f_ck = f_cm - 8
nu_ck = k_f * k_v * math.sqrt(f_ck)

# 2. Steel
f_swyk = f_swy * 0.88
nu_sk = rho_sw * f_swyk * (1 / math.tan(theta))

# 3. FRP
if reinforcement_type == "Laminates":
    eps_fe_basis = 0.103 * (rho_f * E_f)**(-0.665)
else:
    eps_fe_basis = 0.027 * (rho_f * E_f)**(-0.52)

if reinforcement_type == "Laminates":
    k_m = (0.063 * f_cm + 0.59) * \
          (0.0044 * L_Rf + 1.98) * \
          (-0.0053 * alpha_f_deg + 1.52) * \
          (0.0036 * d_g + 0.27) * \
          (-3.1 * rho_slT + 0.44) * \
          (0.00031 * rho_f * E_f + 0.921)
else:
    k_m = (0 * f_cm + 1) * \
          (0.00028 * L_Rf + 0.41) * \
          (-0.0071 * alpha_f_deg + 1.73) * \
          (0.15 * d_g + 0.22) * \
          (7.4 * rho_slT + 1.38) * \
          (-0.00012 * rho_f * E_f + 0.52)

eps_fe_mean = k_m * eps_fe_basis

if reinforcement_type == "Laminates":
    eps_fek = 0.676 * eps_fe_mean
else:
    eps_fek = 0.592 * eps_fe_mean

nu_fk = (rho_f * E_f * h_f * eps_fek / d_s) * (1/math.tan(theta) + 1/math.tan(alpha_f)) * math.sin(alpha_f)

# 4. Factors
s_val = f_swy * rho_sw
if reinforcement_type == "Laminates":
    gamma_R_Lind = -0.6 / (1.7 + s_val) + 1.6
    gamma_R_WLSF = -0.8 / (2.1 + s_val) + 1.5
    gamma_R_Const_Lind = 1.41
    gamma_R_Const_WLSF = 1.25
else:
    gamma_R_Lind = -2.6 / (3.8 + s_val) + 1.8
    gamma_R_WLSF = -2.5 / (4.0 + s_val) + 1.7
    gamma_R_Const_Lind = 1.30
    gamma_R_Const_WLSF = 1.16

gamma_c = 1.5
gamma_s = 1.15
gamma_fb = 1.25

def calculate_V_Rd(gamma_R, nu_ck, nu_sk, nu_fk, b_w, d_s):
    term = (nu_ck / gamma_c) + (nu_sk / gamma_s) + (nu_fk / gamma_fb)
    return (1 / gamma_R) * term * b_w * d_s / 1000

V_Rd_Lind_Var = calculate_V_Rd(gamma_R_Lind, nu_ck, nu_sk, nu_fk, b_w, d_s)
V_Rd_WLSF_Var = calculate_V_Rd(gamma_R_WLSF, nu_ck, nu_sk, nu_fk, b_w, d_s)
V_Rd_Lind_Const = calculate_V_Rd(gamma_R_Const_Lind, nu_ck, nu_sk, nu_fk, b_w, d_s)
V_Rd_WLSF_Const = calculate_V_Rd(gamma_R_Const_WLSF, nu_ck, nu_sk, nu_fk, b_w, d_s)

# --- Main Dashboard ---

# Top KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Design Resistance (Lind)", f"{V_Rd_Lind_Var:.1f} kN", delta="Variable γR")
with kpi2:
    st.metric("Design Resistance (WLSF)", f"{V_Rd_WLSF_Var:.1f} kN", delta="Variable γR")
with kpi3:
    st.metric("Reliability Factor (Lind)", f"{gamma_R_Lind:.2f}", delta_color="off")
with kpi4:
    st.metric("Reliability Factor (WLSF)", f"{gamma_R_WLSF:.2f}", delta_color="off")

st.markdown("---")

# Tabs for detailed view
tab1, tab2, tab3 = st.tabs(["📊 Analysis & Charts", "🧮 Detailed Calculations", "📝 Formulas"])

with tab1:
    col_charts_1, col_charts_2 = st.columns([1.5, 1])
    
    with col_charts_1:
        st.markdown("### 📈 Resistance Comparison")
        # Bar Chart
        plt.style.use('default') # Reset to default (light)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')
        ax.set_facecolor('none')
        
        methods = ["Lind (Var)", "WLSF (Var)", "Lind (Const)", "WLSF (Const)"]
        values = [V_Rd_Lind_Var, V_Rd_WLSF_Var, V_Rd_Lind_Const, V_Rd_WLSF_Const]
        colors_bar = ['#0066CC', '#2979FF', '#475569', '#64748B'] # Blue shades and Grays
        
        bars = ax.bar(methods, values, color=colors_bar, width=0.6, zorder=3)
        
        # Grid and Spines
        ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0, color='#CBD5E1')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#64748B')
        
        ax.tick_params(axis='x', colors='#475569', labelsize=10)
        ax.tick_params(axis='y', colors='#475569', labelsize=10)
        
        # Labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f} kN',
                    ha='center', va='bottom', color='#1E293B', fontsize=11, fontweight='bold')
            
        st.pyplot(fig, use_container_width=True)

    with col_charts_2:
        st.markdown("### 🥧 Resistance Share")
        # Pie Chart
        v_c_d = (nu_ck / gamma_c) * b_w * d_s / 1000
        v_s_d = (nu_sk / gamma_s) * b_w * d_s / 1000
        v_f_d = (nu_fk / gamma_fb) * b_w * d_s / 1000
        
        labels = ['Concrete', 'Steel', 'FRP']
        sizes = [v_c_d, v_s_d, v_f_d]
        colors_pie = ['#26C6DA', '#FFA726', '#EF5350'] # Teal, Orange, Red
        
        fig2, ax2 = plt.subplots(figsize=(5, 5), facecolor='none')
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                          autopct='%1.1f%%', startangle=140, 
                                          pctdistance=0.85, explode=(0.05, 0.05, 0.05),
                                          textprops={'color':"#334155", 'fontsize': 10})
        
        # Donut hole
        centre_circle = plt.Circle((0,0),0.70,fc='white') # White center for light theme
        fig2.gca().add_artist(centre_circle)
        
        # Center text
        total_v = sum(sizes)
        ax2.text(0, 0, f"Total\n{total_v:.0f} kN", ha='center', va='center', color='#1E293B', fontsize=12, fontweight='bold')
        
        st.pyplot(fig2, use_container_width=True)

with tab2:
    st.markdown("### 🔢 Intermediate Parameters")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"**Theta ($\\theta$)**\n\n {theta_deg:.2f}°")
    c2.info(f"**Crack Factor ($k_v$)**\n\n {k_v:.3f}")
    c3.info(f"**Mod. Factor ($\\kappa_m$)**\n\n {k_m:.3f}")
    c4.info(f"**Eff. Strain ($\\varepsilon_{{fek}}$)**\n\n {eps_fek:.5f}")
    
    st.markdown("### 🧱 Strength Components (Characteristic)")
    c_a, c_b, c_c = st.columns(3)
    c_a.success(f"**Concrete ($\\nu_{{ck}}$)**\n\n {nu_ck:.2f} MPa")
    c_b.warning(f"**Steel ($\\nu_{{sk}}$)**\n\n {nu_sk:.2f} MPa")
    c_c.error(f"**FRP ($\\nu_{{fk}}$)**\n\n {nu_fk:.2f} MPa")

with tab3:
    st.markdown("### 📐 Governing Equations")
    st.latex(r"V_{Rd} = \frac{1}{\gamma_R} \left( \frac{\nu_{ck}}{\gamma_c} + \frac{\nu_{sk}}{\gamma_s} + \frac{\nu_{fk}}{\gamma_{fb}} \right) b_w d_s")
    st.markdown("---")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Concrete Contribution**")
        st.latex(r"\nu_c = k_f k_v \sqrt{f_{cm}}")
        st.markdown("**Steel Contribution**")
        st.latex(r"\nu_s = \rho_{sw} f_{swy} \cot \theta")
    with col_f2:
        st.markdown("**FRP Contribution**")
        st.latex(r"\nu_f = \frac{\rho_f E_f h_f \varepsilon_{fe}}{d_s} (\cot \theta + \cot \alpha_f) \sin \alpha_f")
        st.markdown("**Effective Strain**")
        st.latex(r"\varepsilon_{fe} = \kappa_m \cdot p' (\rho_f E_f)^q")
