import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px # Biblioteca para gráficos modernos

# --- CONFIGURAÇÃO VISUAL ULTRA-FUTURISTA (OrthoKlin) ---
st.set_page_config(page_title="OrthoKlin Pro - Gestão Futurista", layout="wide", initial_sidebar_state="expanded")

# CSS Avançado: Glassmorphism e Cores da Logo
st.markdown("""
    <style>
    /* Fundo Principal e Fontes */
    .main { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); font-family: 'Segoe UI', sans-serif; }
    
    /* Sidebar com Efeito Vidro (Glassmorphism) */
    .css-1d391kg { 
        background-color: rgba(255, 255, 255, 0.4) !important; 
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Botões Futuristas com degradê da logo */
    .stButton>button { 
        width: 100%; 
        border-radius: 50px; 
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%); 
        color: white; 
        font-weight: 600;
        text-transform: uppercase;
        border: none;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { box-shadow: 0 6px 20px rgba(233, 30,
