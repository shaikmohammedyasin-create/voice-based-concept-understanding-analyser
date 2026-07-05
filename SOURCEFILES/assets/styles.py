import streamlit as st

def apply_styles():
    st.markdown("""
<style>
/* Import Google Font Outfit */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Global app layout */
.stApp {
    background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #030712 100%);
    color: #e2e8f0;
    font-family: 'Outfit', sans-serif;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #090d16 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Custom layout card component */
.custom-card {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.custom-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 12px 32px -8px rgba(99, 102, 241, 0.15);
}

/* Accent Badge styles */
.accent-badge {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%);
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 9999px;
    display: inline-block;
    border: 1px solid rgba(99, 102, 241, 0.25);
    margin: 4px;
    letter-spacing: 0.02em;
}

/* Keyword result styles */
.keyword-covered {
    background: rgba(16, 185, 129, 0.1) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
}

.keyword-missed {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
}

/* Main title header */
.main-title {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2px;
    letter-spacing: -0.02em;
}

.main-subtitle {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 24px;
    font-weight: 300;
    letter-spacing: 0.01em;
}

/* Primary button styling */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 500;
}

/* Responsive: mobile portrait (320-480px) */
@media (max-width: 480px) {
    .main-title { font-size: 22px; }
    .main-subtitle { font-size: 12px; }
    .custom-card { padding: 16px; border-radius: 14px; }
    .accent-badge { font-size: 10px; padding: 4px 8px; }
}

/* Responsive: mobile landscape and small tablets (481-768px) */
@media (min-width: 481px) and (max-width: 768px) {
    .main-title { font-size: 26px; }
    .custom-card { padding: 20px; }
}

/* Responsive: large desktops (1600px+) */
@media (min-width: 1600px) {
    .main-title { font-size: 38px; }
    .main-subtitle { font-size: 16px; }
}
</style>
""", unsafe_allow_html=True)
