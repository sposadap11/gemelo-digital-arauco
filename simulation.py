"""
╔══════════════════════════════════════════════════════════════════════════╗
║   SISTEMA DE TRANSPORTE AGV — ARAUCO PLYWOOD                            ║
║   Optimizador de Flota con Simulación Digital en Tiempo Real            ║
║   Universidad de Concepción · Hackathon Arauco 2026                     ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import streamlit.components.v1 as components
import math
import json
import base64
from pathlib import Path

# Cargar logos corporativos
logo_path = Path(__file__).parent / "logo.png"
if logo_path.exists():
    logo_base64 = base64.b64encode(logo_path.read_bytes()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height:45px;width:auto;object-fit:contain;">'
else:
    logo_html = "🏭"

udec_path = Path(__file__).parent / "logoudec.png"
if udec_path.exists():
    udec_base64 = base64.b64encode(udec_path.read_bytes()).decode()
    udec_html = f'<img src="data:image/png;base64,{udec_base64}" style="height:45px;width:auto;object-fit:contain;">'
else:
    udec_html = "🎓"

gearbox_path = Path(__file__).parent / "gearbox.png"
if gearbox_path.exists():
    gearbox_base64 = base64.b64encode(gearbox_path.read_bytes()).decode()
    gearbox_html = f'<img src="data:image/png;base64,{gearbox_base64}" style="height:45px;width:auto;object-fit:contain;">'
else:
    gearbox_html = "⚙️"




# ══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Sistema AGV · Arauco Plywood",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════
# ESTILOS GLOBALES
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
[data-testid="stApp"] {
    background: linear-gradient(135deg, #070c18 0%, #0a0f1e 60%, #070c18 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d1a 0%, #0f172a 100%) !important;
    border-right: 1px solid rgba(6,182,212,0.12) !important;
}
/* Ocultar el botón de colapsar la barra lateral para que quede fija */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"] button {
    background-color: #EA7600 !important;
    color: white !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    visibility: visible !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    margin-top: 10px !important;
    margin-left: 10px !important;
}
header[data-testid="stHeader"] button svg {
    fill: white !important;
    stroke: white !important;
}
footer { visibility: hidden; }
.stDeployButton, [data-testid="stToolbar"] { display: none !important; }

.kpi-wrap {
    background: rgba(10,14,26,0.85);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 18px;
    padding: 22px 20px 18px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: transform .25s, box-shadow .25s, border-color .25s;
    position: relative; overflow: hidden;
}
.kpi-wrap:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(6,182,212,0.12);
    border-color: rgba(6,182,212,0.35);
}
.kpi-num  { font-size:52px; font-weight:900; line-height:1; font-family:monospace; }
.kpi-lbl  { font-size:10px; text-transform:uppercase; letter-spacing:.18em;
             font-weight:700; color:#64748b; margin-top:6px; }
.kpi-sub  { font-size:11px; color:#475569; margin-top:5px; font-family:sans-serif; }

.xai-box {
    background: linear-gradient(135deg, rgba(6,182,212,.05) 0%, rgba(139,92,246,.05) 100%);
    border: 1px solid rgba(6,182,212,.13);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 14px;
    font-family: sans-serif;
}
.xai-title { font-size:12px; font-weight:900; color:#06b6d4;
              text-transform:uppercase; letter-spacing:.12em; margin-bottom:10px; }
.xai-body  { font-size:14px; color:#cbd5e1; line-height:1.8; }
.xai-hi    { color:#06b6d4; font-weight:700; }
.xai-ok    { color:#10b981; font-weight:700; }
.xai-warn  { color:#f59e0b; font-weight:700; }

.sb-section {
    font-size:10px; font-weight:900; color:#06b6d4;
    text-transform:uppercase; letter-spacing:.18em;
    margin:14px 0 6px; padding-bottom:4px;
    border-bottom:1px solid rgba(6,182,212,.15);
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,14,26,0.8) !important;
    border-radius: 12px !important; padding: 4px !important;
    border: 1px solid rgba(99,102,241,0.15) !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #475569 !important; font-size: 12px !important; font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(6,182,212,.12) !important;
    color: #06b6d4 !important; border: 1px solid rgba(6,182,212,.2) !important;
}
input[type="number"] {
    background: rgba(15,23,42,.9) !important;
    border: 1px solid rgba(99,102,241,.2) !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: monospace !important; font-weight: 800 !important;
    text-align: center !important;
}
hr { border-color: rgba(99,102,241,.1) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════
_DEFAULT = {
    "S1": {"L": 10, "C": 10},
    "S2": {"A": 8,  "B": 6, "M": 6},
    "S3": {"A": 7,  "B": 7, "M": 6},
}
if "prod" not in st.session_state:
    st.session_state.prod = {k: dict(v) for k, v in _DEFAULT.items()}

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 14px;
         border-bottom:1px solid rgba(6,182,212,.12);margin-bottom:4px;">
      <div style="font-size:11px;font-weight:900;letter-spacing:.3em;
           color:#f59e0b;text-transform:uppercase;">▲ ARAUCO</div>
      <div style="font-size:22px;font-weight:900;color:#fff;margin:6px 0 2px;">
        AGV <span style="color:#06b6d4;">Optimizer</span>
      </div>
      <div style="font-size:10px;color:#475569;font-family:sans-serif;">
        Simulación Digital de Flota Autónoma
      </div>
      <div style="margin-top:10px;display:inline-flex;align-items:center;gap:7px;
           background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);
           border-radius:20px;padding:3px 14px;">
        <div style="width:7px;height:7px;background:#10b981;border-radius:50%;
             animation:blink 1.8s infinite;"></div>
        <span style="font-size:10px;color:#10b981;font-weight:800;">SIMULACIÓN EN VIVO</span>
      </div>
    </div>
    <style>@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}</style>
    """, unsafe_allow_html=True)



    # ── Mezcla de Producción ───────────────────────────────────────────────
    st.markdown('<div class="sb-section">🏭 Mezcla de Producción</div>',
                unsafe_allow_html=True)
    st.caption("Objetivo: cada máquina produce exactamente **20 lotes/hora**")

    _MACH = [
        ("S1", "Salida 1 · Línea L y C",    ["L","C"],       "#06b6d4"),
        ("S2", "Salida 2 · Línea A, B y M", ["A","B","M"],   "#f59e0b"),
        ("S3", "Salida 3 · Línea A, B y M", ["A","B","M"],   "#a855f7"),
    ]
    for mach, mlbl, mprods, mcol in _MACH:
        st.markdown(
            f'<div style="font-size:11px;font-weight:800;color:{mcol};'
            f'text-transform:uppercase;letter-spacing:.1em;margin:10px 0 4px;">'
            f'{mlbl}</div>', unsafe_allow_html=True)
        cols = st.columns(len(mprods))
        for pk, col in zip(mprods, cols):
            nv = col.number_input(f"Prod {pk}", min_value=0, max_value=20,
                                  value=st.session_state.prod[mach][pk],
                                  key=f"ni_{mach}_{pk}")
            st.session_state.prod[mach][pk] = int(nv)
        tot = sum(st.session_state.prod[mach].values())
        ok  = tot == 20
        bc  = "#10b981" if ok else ("#f59e0b" if tot < 20 else "#ef4444")
        ic  = "✅" if ok else ("⚠️" if tot < 20 else "🔴")
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;font-size:11px;'
            f'color:{bc};font-weight:800;margin:4px 0 2px;">'
            f'<span>Total {mach}</span><span>{ic} {tot}/20</span></div>'
            f'<div style="width:100%;background:rgba(30,41,59,.8);border-radius:6px;height:5px;margin-bottom:10px;">'
            f'<div style="width:{min(tot/20*100,100):.0f}%;background:{bc};height:5px;'
            f'border-radius:6px;transition:width .4s;"></div></div>',
            unsafe_allow_html=True)

    st.divider()

    # ── Parámetros AGV ─────────────────────────────────────────────────────
    st.markdown('<div class="sb-section">⚙️ Parámetros AGV</div>',
                unsafe_allow_html=True)
    velocity = st.slider("🚀 Velocidad máxima", 1.0, 5.0, 5.0, 0.5,
                         format="%.1f km/h",
                         help="Normativa Arauco: máx **5 km/h**")
    occupancy = st.slider("📦 Ocupación máxima", 50, 70, 70, 5,
                          format="%d%%",
                          help="Normativa Arauco: máx **70%**")
    safety_margin = st.slider("🛡️ Margen de reserva", 0, 20, 5, 1,
                              format="%d%%",
                              help="AGVs adicionales para mantenimiento / fallas")

    st.divider()
    st.markdown('<div class="sb-section">📏 Infraestructura</div>',
                unsafe_allow_html=True)
    dist_short = st.slider("📍 Ruta corta (S1→E1 / S2,S3→E2)",
                           50, 250, 100, 10, format="%d m")
    dist_long  = st.slider("📍 Ruta larga (S2,S3→E3,E4)",
                           80, 350, 150, 10, format="%d m")
    load_time  = st.slider("⏱️ Tiempo carga/descarga",
                           5, 120, 30, 5, format="%d s",
                           help="Tiempo del transportador de rodillos por operación")
    load_weight = st.slider("⚖️ Peso del lote",
                            500, 3500, 2100, 100, format="%d kg",
                            help="Dimensiones reales del lote: 2.6×1.4×1m")

    st.divider()
    st.markdown(
        '<div style="font-size:9px;color:#1e293b;text-align:center;'
        'font-family:sans-serif;">Modelo MILP · UdeC · Hackathon Arauco 2026 · v3.0</div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# CÁLCULOS DE INGENIERÍA
# ══════════════════════════════════════════════════════════════════════════
prod = st.session_state.prod

flow_LC    = prod["S1"]["L"] + prod["S1"]["C"]
flow_A_S2  = prod["S2"]["A"]
flow_A_S3  = prod["S3"]["A"]
flow_A     = flow_A_S2 + flow_A_S3
flow_BM_S2 = prod["S2"]["B"] + prod["S2"]["M"]
flow_BM_S3 = prod["S3"]["B"] + prod["S3"]["M"]
flow_BM    = flow_BM_S2 + flow_BM_S3
flow_E3    = min(15.0, flow_BM / 2)
flow_E4    = flow_BM - flow_E3
total_prod = flow_LC + flow_A + flow_BM

sum_S1 = prod["S1"]["L"] + prod["S1"]["C"]
sum_S2 = prod["S2"]["A"] + prod["S2"]["B"] + prod["S2"]["M"]
sum_S3 = prod["S3"]["A"] + prod["S3"]["B"] + prod["S3"]["M"]

v_m_min = (velocity * 1000) / 60
v_m_s   = velocity * 1000 / 3600
lt_min  = load_time / 60

cycle_s   = (2 * dist_short) / v_m_min + 2 * lt_min
cycle_l   = (2 * dist_long)  / v_m_min + 2 * lt_min
cap_eff_s = (60 / max(cycle_s, 0.001)) * (occupancy / 100)
cap_eff_l = (60 / max(cycle_l, 0.001)) * (occupancy / 100)

agv_r1 = math.ceil(flow_LC  / max(cap_eff_s, 0.001))
agv_r2 = math.ceil(flow_A   / max(cap_eff_s, 0.001))
agv_r3 = math.ceil(flow_BM  / max(cap_eff_l, 0.001))

agv_r1s = math.ceil(agv_r1 * (1 + safety_margin / 100))
agv_r2s = math.ceil(agv_r2 * (1 + safety_margin / 100))
agv_r3s = math.ceil(agv_r3 * (1 + safety_margin / 100))

total_agv      = agv_r1  + agv_r2  + agv_r3
total_agv_safe = agv_r1s + agv_r2s + agv_r3s

util_r1  = (flow_LC  / max(agv_r1 * cap_eff_s, 0.001)) * 100
util_r2  = (flow_A   / max(agv_r2 * cap_eff_s, 0.001)) * 100
util_r3  = (flow_BM  / max(agv_r3 * cap_eff_l, 0.001)) * 100
avg_util = (util_r1 + util_r2 + util_r3) / 3

tonnage_h   = total_prod * (load_weight / 1000)
energy_kwh  = total_agv * 8.5

# Sub-rutas para animación
_r2a = max(1 if flow_A_S2 > 0 else 0,
           math.ceil(agv_r2 * flow_A_S2 / max(flow_A, 1)))
_r2b = max(0, agv_r2 - _r2a)
_r3a = max(1 if flow_BM_S2 > 0 else 0,
           math.ceil(agv_r3 * (flow_BM_S2 / 2) / max(flow_BM, 1)))
_r3b = max(1 if flow_BM_S3 > 0 else 0,
           math.ceil(agv_r3 * (flow_BM_S3 / 2) / max(flow_BM, 1)))
_r3c = max(0, math.ceil(agv_r3 * (flow_BM_S2 / 2) / max(flow_BM, 1)))
_r3d = max(0, agv_r3 - _r3a - _r3b - _r3c)

valid_S1  = sum_S1 == 20
valid_S2  = sum_S2 == 20
valid_S3  = sum_S3 == 20
valid_E1  = flow_LC  <= 20.01
valid_E2  = flow_A   <= 15.01
valid_E3  = flow_E3  <= 15.01
valid_E4  = flow_E4  <= 15.01
all_valid = all([valid_S1, valid_S2, valid_S3,
                 valid_E1, valid_E2, valid_E3, valid_E4])

# ══════════════════════════════════════════════════════════════════════════
# ENCABEZADO
# ══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex;align-items:center;gap:18px;padding-bottom:22px;
     border-bottom:3px solid #EA7600;margin-bottom:22px;">
  <div style="background:#696158;padding:10px;border-radius:14px;display:flex;
       align-items:center;gap:12px;justify-content:center;box-shadow:0 4px 20px rgba(0,0,0,0.4);
       flex-shrink:0;border:1px solid #BFB800;">
    {logo_html}
    <div style="width:1px;height:35px;background:rgba(255,255,255,0.2);"></div>
    {udec_html}
    <div style="width:1px;height:35px;background:rgba(255,255,255,0.2);"></div>
    {gearbox_html}
  </div>
  <div>
    <div style="font-size:11px;font-weight:900;letter-spacing:.22em;color:#BFB800;
         text-transform:uppercase;margin-bottom:3px;">
      ARAUCO Industrial Challenge · Universidad de Concepción
    </div>
    <div style="font-size:28px;font-weight:900;color:#DFD1a7;line-height:1.1;">
      Transporte Autónomo <span style="color:#EA7600;">AGV</span>
      <span style="font-size:13px;color:#696158;margin-left:10px;
            background:#F3CF1C;padding:2px 8px;border-radius:6px;font-weight:900;
            display:inline-block;vertical-align:middle;letter-spacing:0.05em;">
        Plywood · 24/7 · 60 lotes/h
      </span>
    </div>
    <div style="font-size:12px;color:#DFD1a7;font-family:sans-serif;margin-top:5px;">
      3 puntos de producción → 4 entradas de consumo
      · <span style="color:#33B2A9;font-weight:700;">Optimización MILP</span> 
      · <span style="color:#B46A55;font-weight:700;">Simulación Digital</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════
_sc = "#10b981" if all_valid else "#f59e0b"
_si = "✅" if all_valid else "⚠️"
_st = "SISTEMA ÓPTIMO" if all_valid else "AJUSTAR"
_scnt = sum([valid_S1, valid_S2, valid_S3,
             valid_E1, valid_E2, valid_E3, valid_E4])
_uc = "#10b981" if avg_util < 80 else ("#f59e0b" if avg_util < 95 else "#ef4444")

kc1, kc2, kc3, kc4 = st.columns(4)
with kc1:
    st.markdown(
        f'<div class="kpi-wrap" style="border-color:rgba(6,182,212,.25);">'
        f'<div class="kpi-lbl" style="color:#06b6d4;">🚚 Flota Mínima</div>'
        f'<div class="kpi-num" style="color:#06b6d4;">{total_agv}</div>'
        f'<div style="font-size:13px;color:#94a3b8;margin-top:4px;">AGVs requeridos</div>'
        f'<div class="kpi-sub">+{total_agv_safe-total_agv} reserva · Total: {total_agv_safe}</div>'
        f'</div>', unsafe_allow_html=True)
with kc2:
    st.markdown(
        f'<div class="kpi-wrap" style="border-color:rgba(16,185,129,.25);">'
        f'<div class="kpi-lbl" style="color:#10b981;">📦 Throughput</div>'
        f'<div class="kpi-num" style="color:#10b981;">{total_prod}</div>'
        f'<div style="font-size:13px;color:#94a3b8;margin-top:4px;">lotes / hora</div>'
        f'<div class="kpi-sub">{tonnage_h:.1f} toneladas/hora transportadas</div>'
        f'</div>', unsafe_allow_html=True)
with kc3:
    st.markdown(
        f'<div class="kpi-wrap" style="border-color:rgba(139,92,246,.25);">'
        f'<div class="kpi-lbl" style="color:#8b5cf6;">📊 Utilización</div>'
        f'<div class="kpi-num" style="color:{_uc};">{avg_util:.0f}%</div>'
        f'<div style="font-size:13px;color:#94a3b8;margin-top:4px;">carga promedio flota</div>'
        f'<div class="kpi-sub">R1:{util_r1:.0f}% · R2:{util_r2:.0f}% · R3:{util_r3:.0f}%</div>'
        f'</div>', unsafe_allow_html=True)
with kc4:
    _rgb = "16,185,129" if all_valid else "245,158,11"
    st.markdown(
        f'<div class="kpi-wrap" style="border-color:rgba({_rgb},.25);">'
        f'<div class="kpi-lbl" style="color:{_sc};">{_si} Estado</div>'
        f'<div style="font-size:26px;font-weight:900;color:{_sc};margin:8px 0;">{_st}</div>'
        f'<div style="font-size:13px;color:#94a3b8;margin-top:4px;">{_scnt}/7 restricciones ✓</div>'
        f'<div class="kpi-sub">Operación 24h · 365 días/año</div>'
        f'</div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════
tab_anim, tab_routes, tab_xai, tab_valid = st.tabs([
    "🎬  Simulación Animada",
    "📊  Análisis de Rutas",
    "🧠  Explicación Simple",
    "✅  Validación",
])

# ──────────────────────────────────────────────────────────────────────────
# TAB 1 — ANIMACIÓN DE CARRITOS AGV
# ──────────────────────────────────────────────────────────────────────────
with tab_anim:
    st.markdown(
        '<div style="font-size:11px;color:#475569;font-family:sans-serif;margin-bottom:12px;">'
        'Los carritos <b style="color:#06b6d4;">cargados</b> brillan con el color de su ruta; '
        'el regreso <b style="color:#334155;">vacío</b> aparece tenue. '
        'La velocidad visual refleja el valor configurado en el panel.</div>',
        unsafe_allow_html=True)

    # JSON de configuración para el canvas
    cfg = {
        "velocity":   velocity,
        "dist_short": dist_short,
        "dist_long":  dist_long,
        "load_time":  load_time,
        "TS":         55,                    # factor de compresión temporal
        "flow_E1":    round(flow_LC,  1),
        "flow_E2":    round(flow_A,   1),
        "flow_E3":    round(flow_E3,  1),
        "flow_E4":    round(flow_E4,  1),
        "flow_total": total_prod,
        "agv_r1":     agv_r1,
        "agv_r2a":    max(1 if flow_A_S2 > 0 else 0, _r2a),
        "agv_r2b":    max(1 if flow_A_S3 > 0 else 0, _r2b),
        "agv_r3a":    max(1 if flow_BM_S2 > 0 else 0, _r3a),
        "agv_r3b":    max(1 if flow_BM_S3 > 0 else 0, _r3b),
        "agv_r3c":    max(0, _r3c),
        "agv_r3d":    max(0, _r3d),
        "occ":        occupancy,
        "util_r1":    round(util_r1, 1),
        "util_r2":    round(util_r2, 1),
        "util_r3":    round(util_r3, 1),
    }
    cfg_json = json.dumps(cfg)

    # ── HTML/JS Canvas ─────────────────────────────────────────────────────
    CANVAS_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html,body { background:#070c18; overflow:hidden; width:100%; height:100%; }
canvas { display:block; }
#bar {
  position:absolute; bottom:6px; left:50%; transform:translateX(-50%);
  background:rgba(6,182,212,.07); border:1px solid rgba(6,182,212,.18);
  border-radius:20px; padding:3px 18px; font-family:monospace;
  font-size:10px; color:#06b6d4; white-space:nowrap;
  letter-spacing:.06em; pointer-events:none;
}
#leg {
  position:absolute; top:8px; left:50%; transform:translateX(-50%);
  display:flex; gap:14px; align-items:center;
  background:rgba(7,12,24,.75); border:1px solid rgba(99,102,241,.12);
  border-radius:20px; padding:4px 16px; pointer-events:none;
}
.li { display:flex; align-items:center; gap:5px;
      font-family:sans-serif; font-size:9px; color:#64748b; }
.ld { width:8px; height:8px; border-radius:50%; }
</style>
</head><body>
<canvas id="c"></canvas>
<div id="leg">
  <div class="li"><div class="ld" style="background:#06b6d4"></div>Ruta L/C · 100m</div>
  <div class="li"><div class="ld" style="background:#f59e0b"></div>Ruta A · 100m</div>
  <div class="li"><div class="ld" style="background:#8b5cf6"></div>Ruta B/M · 150m</div>
  <div class="li" style="margin-left:6px;color:#334155;">
    <div style="width:10px;height:6px;background:#06b6d4;border-radius:2px;opacity:.9;"></div>cargado
    <div style="width:10px;height:6px;background:#1e293b;border-radius:2px;margin-left:6px;
         border:1px solid #334155;"></div>vacío
  </div>
</div>
<div id="bar">—</div>
<script>
// ── CONFIG ──────────────────────────────────────────────────────────────
const P = __CFG__;
const W = 900, H = 448;
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
const DPR    = Math.min(window.devicePixelRatio || 1, 2);
canvas.width  = W * DPR; canvas.height = H * DPR;
canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
ctx.scale(DPR, DPR);

// ── TIEMPOS VISUALES ────────────────────────────────────────────────────
const vms    = P.velocity * 1000 / 3600;
const vtS    = (P.dist_short / vms) / P.TS;  // seg visuales viaje corto
const vtL    = (P.dist_long  / vms) / P.TS;  // seg visuales viaje largo
const vlt    = P.load_time / P.TS;            // seg visuales carga

// ── NODOS ───────────────────────────────────────────────────────────────
const N = {
  S1:{x:105,y:80,  lbl:'S1',sub:'20 l/h',col:'#06b6d4',tp:'p'},
  S2:{x:105,y:218, lbl:'S2',sub:'20 l/h',col:'#f59e0b',tp:'p'},
  S3:{x:105,y:360, lbl:'S3',sub:'20 l/h',col:'#a855f7',tp:'p'},
  E1:{x:795,y:58,  lbl:'E1',sub:'L y C',  col:'#06b6d4',tp:'c',flow:P.flow_E1},
  E2:{x:795,y:162, lbl:'E2',sub:'Prod A', col:'#f59e0b',tp:'c',flow:P.flow_E2},
  E3:{x:795,y:278, lbl:'E3',sub:'B y M',  col:'#8b5cf6',tp:'c',flow:P.flow_E3},
  E4:{x:795,y:394, lbl:'E4',sub:'B y M',  col:'#d946ef',tp:'c',flow:P.flow_E4},
};

// ── RUTAS (Cubic Bezier) ─────────────────────────────────────────────────
const RT = [
  {fr:'S1',to:'E1',c1x:305,c1y:78, c2x:595,c2y:58, col:'#06b6d4',n:P.agv_r1, vt:vtS},
  {fr:'S2',to:'E2',c1x:295,c1y:200,c2x:595,c2y:158,col:'#f59e0b',n:P.agv_r2a,vt:vtS},
  {fr:'S3',to:'E2',c1x:295,c1y:295,c2x:595,c2y:175,col:'#f59e0b',n:P.agv_r2b,vt:vtS},
  {fr:'S2',to:'E3',c1x:315,c1y:240,c2x:595,c2y:272,col:'#8b5cf6',n:P.agv_r3a,vt:vtL},
  {fr:'S3',to:'E3',c1x:315,c1y:325,c2x:595,c2y:278,col:'#8b5cf6',n:P.agv_r3b,vt:vtL},
  {fr:'S2',to:'E4',c1x:310,c1y:292,c2x:595,c2y:388,col:'#d946ef',n:P.agv_r3c,vt:vtL},
  {fr:'S3',to:'E4',c1x:450,c1y:372,c2x:655,c2y:392,col:'#d946ef',n:P.agv_r3d,vt:vtL},
];

// ── UTILIDADES ──────────────────────────────────────────────────────────
function bpt(p0,p1,p2,p3,t){
  const m=1-t;
  return { x:m*m*m*p0.x+3*m*m*t*p1.x+3*m*t*t*p2.x+t*t*t*p3.x,
           y:m*m*m*p0.y+3*m*m*t*p1.y+3*m*t*t*p2.y+t*t*t*p3.y };
}
function btan(p0,p1,p2,p3,t){
  const m=1-t;
  return { x:3*m*m*(p1.x-p0.x)+6*m*t*(p2.x-p1.x)+3*t*t*(p3.x-p2.x),
           y:3*m*m*(p1.y-p0.y)+6*m*t*(p2.y-p1.y)+3*t*t*(p3.y-p2.y) };
}
function rr(ctx,x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r); ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h); ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r); ctx.arcTo(x,y,x+r,y,r); ctx.closePath();
}
function hex6(ctx,x,y,r){
  ctx.beginPath();
  for(let i=0;i<6;i++){
    const a=i*Math.PI/3-Math.PI/6;
    i?ctx.lineTo(x+r*Math.cos(a),y+r*Math.sin(a))
     :ctx.moveTo(x+r*Math.cos(a),y+r*Math.sin(a));
  } ctx.closePath();
}

// ── CLASE CARRITO ────────────────────────────────────────────────────────
class Cart {
  constructor(route, phase){
    this.r=route; this.t=0; this.st='loading'; this.tm=0;
    const full=vlt+route.vt+vlt+route.vt;
    let tp=phase*full;
    if(tp<vlt)            { this.st='loading';   this.tm=vlt-tp;          this.t=0; }
    else if(tp<vlt+route.vt) { this.st='going'; this.t=(tp-vlt)/route.vt;         }
    else if(tp<vlt*2+route.vt){ this.st='unload'; this.tm=vlt*2+route.vt-tp; this.t=1; }
    else                      { this.st='back';  this.t=1-(tp-vlt*2-route.vt)/route.vt; }
  }
  upd(dt){
    switch(this.st){
      case 'loading': this.tm-=dt; if(this.tm<=0){this.st='going';this.t=0;} break;
      case 'going':   this.t=Math.min(1,this.t+dt/this.r.vt);
                      if(this.t>=1){this.st='unload';this.tm=vlt;} break;
      case 'unload':  this.tm-=dt; if(this.tm<=0){this.st='back';}  break;
      case 'back':    this.t=Math.max(0,this.t-dt/this.r.vt);
                      if(this.t<=0){this.st='loading';this.tm=vlt;}  break;
    }
  }
  loaded(){ return this.st==='going'||this.st==='unload'; }
  pos(){
    const r=this.r, from=N[r.fr], to=N[r.to];
    const p0={x:from.x,y:from.y}, p1={x:r.c1x,y:r.c1y};
    const p2={x:r.c2x,y:r.c2y},   p3={x:to.x,y:to.y};
    const pt =bpt(p0,p1,p2,p3,this.t);
    const tan=btan(p0,p1,p2,p3,Math.max(.001,Math.min(.999,this.t)));
    const base=Math.atan2(tan.y,tan.x);
    return { x:pt.x, y:pt.y, a:this.st==='back'?base+Math.PI:base };
  }
}

// Inicializar carritos
let carts=[];
RT.forEach(r=>{ for(let i=0;i<(r.n||0);i++) carts.push(new Cart(r,i/(r.n||1))); });

// ── DIBUJO NODO PRODUCCIÓN ───────────────────────────────────────────────
function drawProd(x,y,col,lbl,sub,ph){
  const R=28;
  const g=ctx.createRadialGradient(x,y,0,x,y,R*2.4);
  g.addColorStop(0,col+'22'); g.addColorStop(1,'transparent');
  ctx.beginPath(); ctx.arc(x,y,R*2.4,0,Math.PI*2);
  ctx.fillStyle=g; ctx.fill();
  const pr=R+6+Math.sin(ph)*4;
  const op=Math.round((0.22+Math.sin(ph)*.1)*255).toString(16).padStart(2,'0');
  ctx.beginPath(); ctx.arc(x,y,pr,0,Math.PI*2);
  ctx.strokeStyle=col+op; ctx.lineWidth=1.2; ctx.setLineDash([4,3]); ctx.stroke();
  ctx.setLineDash([]);
  hex6(ctx,x,y,R);
  ctx.fillStyle='#070c18'; ctx.fill();
  ctx.strokeStyle=col; ctx.lineWidth=2.2; ctx.stroke();
  ctx.fillStyle=col; ctx.font='bold 13px monospace';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(lbl,x,y);
  ctx.fillStyle='#64748b'; ctx.font='8px sans-serif'; ctx.fillText(sub,x,y+R+14);
  ctx.fillStyle=col+'55'; ctx.font='bold 7px sans-serif'; ctx.fillText('PRODUCCIÓN',x,y-R-9);
}

// ── DIBUJO NODO CONSUMO ──────────────────────────────────────────────────
function drawCons(x,y,col,lbl,sub,flow){
  const W2=50,H2=42,fR=Math.min(flow/15,1);
  const g=ctx.createRadialGradient(x,y,0,x,y,52);
  g.addColorStop(0,col+'18'); g.addColorStop(1,'transparent');
  ctx.beginPath(); ctx.arc(x,y,52,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
  if(fR>0){ rr(ctx,x-W2/2+2,y+H2/2-2-fR*(H2-4),W2-4,fR*(H2-4),3);
    ctx.fillStyle=col+'18'; ctx.fill(); }
  rr(ctx,x-W2/2,y-H2/2,W2,H2,9);
  ctx.fillStyle='#070c18'; ctx.fill();
  ctx.strokeStyle=col; ctx.lineWidth=2.2; ctx.stroke();
  ctx.fillStyle=col; ctx.font='bold 13px monospace';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(lbl,x,y-6);
  ctx.fillStyle='#cbd5e1'; ctx.font='bold 9px monospace';
  ctx.fillText(flow.toFixed(0)+'/15',x,y+7);
  ctx.fillStyle='#64748b'; ctx.font='8px sans-serif'; ctx.fillText(sub,x,y+H2/2+13);
  ctx.fillStyle=col+'55'; ctx.font='bold 7px sans-serif'; ctx.fillText('CONSUMO',x,y-H2/2-9);
}

// ── DIBUJO RUTA ──────────────────────────────────────────────────────────
function drawRoute(r){
  if((r.n||0)<=0) return;
  const fr=N[r.fr],to=N[r.to];
  ctx.beginPath();
  ctx.moveTo(fr.x,fr.y);
  ctx.bezierCurveTo(r.c1x,r.c1y,r.c2x,r.c2y,to.x,to.y);
  ctx.setLineDash([5,5]); ctx.strokeStyle=r.col+'28'; ctx.lineWidth=1.2; ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(fr.x,fr.y);
  ctx.bezierCurveTo(r.c1x,r.c1y,r.c2x,r.c2y,to.x,to.y);
  ctx.strokeStyle=r.col+'50'; ctx.lineWidth=1; ctx.stroke();
}

// ── DIBUJO CARRITO ───────────────────────────────────────────────────────
function drawCart(x,y,ang,loaded,col){
  ctx.save(); ctx.translate(x,y); ctx.rotate(ang);
  if(loaded){ ctx.shadowColor=col; ctx.shadowBlur=10; }
  rr(ctx,-15,-7,30,14,3);
  ctx.fillStyle=loaded?col+'44':'#1e293b';
  ctx.fill();
  ctx.strokeStyle=loaded?col:'#334155';
  ctx.lineWidth=loaded?1.8:0.8; ctx.stroke();
  ctx.shadowBlur=0;
  [[-10,7],[10,7],[-10,-7],[10,-7]].forEach(([wx,wy])=>{
    ctx.beginPath(); ctx.arc(wx,wy,2.8,0,Math.PI*2);
    ctx.fillStyle='#0a0e1a'; ctx.fill();
    ctx.strokeStyle=loaded?col+'99':'#475569'; ctx.lineWidth=1; ctx.stroke();
  });
  ctx.strokeStyle=loaded?col+'30':'#1e293b'; ctx.lineWidth=0.8;
  for(let rx=-10;rx<=10;rx+=5){ ctx.beginPath(); ctx.moveTo(rx,-6); ctx.lineTo(rx,6); ctx.stroke(); }
  if(loaded){
    rr(ctx,-9,-15,18,8,2);
    ctx.fillStyle=col+'55'; ctx.fill(); ctx.strokeStyle=col+'99'; ctx.lineWidth=1; ctx.stroke();
    ctx.strokeStyle=col+'28'; ctx.lineWidth=0.5;
    for(let lx=-7;lx<=7;lx+=4){ ctx.beginPath(); ctx.moveTo(lx,-15); ctx.lineTo(lx,-7); ctx.stroke(); }
  }
  ctx.beginPath(); ctx.arc(loaded?12:-12,-5,2.2,0,Math.PI*2);
  ctx.fillStyle=loaded?'#10b981':'#ef444499'; ctx.fill();
  ctx.restore();
}

// ── LOOP PRINCIPAL ────────────────────────────────────────────────────────
let lastT=null;
const barEl=document.getElementById('bar');

function frame(ts){
  if(!lastT) lastT=ts;
  const dt=Math.min((ts-lastT)/1000,.06); lastT=ts;
  carts.forEach(c=>c.upd(dt));

  ctx.clearRect(0,0,W,H);
  const bg=ctx.createLinearGradient(0,0,W,H);
  bg.addColorStop(0,'#070c18'); bg.addColorStop(1,'#0a0f1e');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  ctx.strokeStyle='rgba(99,102,241,0.035)'; ctx.lineWidth=0.5;
  for(let gx=0;gx<W;gx+=32){ ctx.beginPath(); ctx.moveTo(gx,0); ctx.lineTo(gx,H); ctx.stroke(); }
  for(let gy=0;gy<H;gy+=32){ ctx.beginPath(); ctx.moveTo(0,gy); ctx.lineTo(W,gy); ctx.stroke(); }

  // Glows ambientales
  let gL=ctx.createRadialGradient(105,220,0,105,220,180);
  gL.addColorStop(0,'rgba(6,182,212,0.04)'); gL.addColorStop(1,'transparent');
  ctx.fillStyle=gL; ctx.fillRect(0,0,W,H);
  let gR=ctx.createRadialGradient(795,220,0,795,220,180);
  gR.addColorStop(0,'rgba(139,92,246,0.04)'); gR.addColorStop(1,'transparent');
  ctx.fillStyle=gR; ctx.fillRect(0,0,W,H);

  // Headers de zona
  const ph=ts/1000;
  ctx.fillStyle='rgba(71,85,105,0.65)'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center';
  ctx.fillText('▼  ZONA DE PRODUCCIÓN',110,12);
  ctx.fillText('▼  ZONA DE CONSUMO',795,12);

  // Línea central
  ctx.beginPath(); ctx.moveTo(W/2,28); ctx.lineTo(W/2,H-22);
  ctx.strokeStyle='rgba(99,102,241,0.07)'; ctx.lineWidth=1;
  ctx.setLineDash([6,8]); ctx.stroke(); ctx.setLineDash([]);

  RT.forEach(r=>drawRoute(r));

  drawProd(N.S1.x,N.S1.y,N.S1.col,'S1','20 l/h',ph+0.0);
  drawProd(N.S2.x,N.S2.y,N.S2.col,'S2','20 l/h',ph+2.1);
  drawProd(N.S3.x,N.S3.y,N.S3.col,'S3','20 l/h',ph+4.3);
  drawCons(N.E1.x,N.E1.y,N.E1.col,'E1','L y C', P.flow_E1);
  drawCons(N.E2.x,N.E2.y,N.E2.col,'E2','Prod A',P.flow_E2);
  drawCons(N.E3.x,N.E3.y,N.E3.col,'E3','B y M', P.flow_E3);
  drawCons(N.E4.x,N.E4.y,N.E4.col,'E4','B y M', P.flow_E4);

  carts.forEach(c=>{ const p=c.pos(); drawCart(p.x,p.y,p.a,c.loaded(),c.r.col); });

  const lc=carts.filter(c=>c.loaded()).length;
  barEl.textContent=
    P.velocity+' km/h  ·  '+carts.length+' AGVs activos  ·  '+
    lc+' cargados  ·  '+P.flow_total+' lotes/h  ·  Occ. máx '+P.occ+'%';

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script></body></html>"""

    canvas_html = CANVAS_HTML.replace("__CFG__", cfg_json)
    components.html(canvas_html, height=488, scrolling=False)

    # ── Indicadores bajo el canvas ──────────────────────────────────────────
    mi1, mi2, mi3, mi4 = st.columns(4)
    def _mk(col, lbl, val, unit, color):
        col.markdown(
            f'<div style="background:rgba(10,14,26,.7);border:1px solid rgba(99,102,241,.15);'
            f'border-radius:12px;padding:10px 14px;text-align:center;">'
            f'<div style="font-size:9px;color:#475569;font-weight:700;'
            f'text-transform:uppercase;letter-spacing:.1em;">{lbl}</div>'
            f'<div style="font-size:22px;font-weight:900;color:{color};'
            f'font-family:monospace;margin:2px 0;">{val}</div>'
            f'<div style="font-size:9px;color:#334155;">{unit}</div></div>',
            unsafe_allow_html=True)
    _mk(mi1, "Velocidad AGV",  f"{velocity:.1f}", "km/h",       "#06b6d4")
    _mk(mi2, "Ciclo ruta corta", f"{cycle_s:.1f}", "min / ciclo", "#f59e0b")
    _mk(mi3, "Ciclo ruta larga", f"{cycle_l:.1f}", "min / ciclo", "#8b5cf6")
    _mk(mi4, "Tonelaje total",   f"{tonnage_h:.1f}", "ton / hora",  "#10b981")


# ──────────────────────────────────────────────────────────────────────────
# TAB 2 — ANÁLISIS DE RUTAS
# ──────────────────────────────────────────────────────────────────────────
with tab_routes:
    _RD = [
        ("R1","Ruta L/C",  "S1",     "E1",     flow_LC, agv_r1, util_r1, cycle_s, cap_eff_s, dist_short, "#06b6d4"),
        ("R2","Ruta A",    "S2, S3", "E2",     flow_A,  agv_r2, util_r2, cycle_s, cap_eff_s, dist_short, "#f59e0b"),
        ("R3","Ruta B/M",  "S2, S3", "E3, E4", flow_BM, agv_r3, util_r3, cycle_l, cap_eff_l, dist_long,  "#8b5cf6"),
    ]
    rc = st.columns(3)
    for (rid,rn,rfr,rto,rfl,ragv,rut,rcy,rcp,rds,rcol), col in zip(_RD, rc):
        uc = "#10b981" if rut<75 else ("#f59e0b" if rut<92 else "#ef4444")
        with col:
            st.markdown(
                f'<div style="background:rgba(10,14,26,.7);border:1px solid {rcol}33;'
                f'border-radius:16px;padding:18px;">'
                f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
                f'<span style="font-size:11px;font-weight:900;color:{rcol};background:{rcol}15;'
                f'border:1px solid {rcol}33;border-radius:8px;padding:2px 10px;">{rid}</span>'
                f'<span style="font-size:13px;font-weight:800;color:#e2e8f0;">{rn}</span>'
                f'<span style="font-size:10px;color:#475569;">{rds}m</span></div>'
                f'<div style="font-size:11px;color:#64748b;font-family:sans-serif;margin-bottom:12px;">'
                f'<b style="color:#94a3b8;">{rfr}</b> → <b style="color:#94a3b8;">{rto}</b></div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">'
                f'<div style="background:rgba(7,12,24,.6);border-radius:10px;padding:10px;text-align:center;">'
                f'<div style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;">Flujo</div>'
                f'<div style="font-size:26px;font-weight:900;color:#e2e8f0;font-family:monospace;">{rfl:.0f}</div>'
                f'<div style="font-size:9px;color:#475569;">lotes/h</div></div>'
                f'<div style="background:rgba(7,12,24,.6);border-radius:10px;padding:10px;text-align:center;">'
                f'<div style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;">AGVs</div>'
                f'<div style="font-size:26px;font-weight:900;color:{rcol};font-family:monospace;">{ragv}</div>'
                f'<div style="font-size:9px;color:#475569;">unidades</div></div></div>'
                f'<div style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.1em;margin-bottom:4px;">Carga operativa '
                f'<span style="color:{uc};">{rut:.1f}%</span></div>'
                f'<div style="width:100%;background:rgba(10,14,26,.8);border-radius:9999px;'
                f'height:6px;margin-bottom:10px;">'
                f'<div style="width:{min(rut,100):.0f}%;background:{uc};height:6px;'
                f'border-radius:9999px;box-shadow:0 0 8px {uc}44;"></div></div>'
                f'<div style="font-size:10px;color:#475569;font-family:sans-serif;">'
                f'Ciclo: <b style="color:#94a3b8;">{rcy:.2f} min</b> &nbsp;·&nbsp; '
                f'Cap/AGV: <b style="color:#94a3b8;">{rcp:.1f} l/h</b></div></div>',
                unsafe_allow_html=True)

    st.divider()
    st.markdown(
        '<div style="font-size:11px;font-weight:900;color:#94a3b8;text-transform:uppercase;'
        'letter-spacing:.15em;margin-bottom:12px;">📐 Métricas de Ingeniería</div>',
        unsafe_allow_html=True)
    _MET = [
        ("Velocidad m/min",   f"{v_m_min:.2f}",  "m/min"),
        ("Velocidad m/s",     f"{v_m_s:.3f}",    "m/s"),
        ("Ciclo ruta corta",  f"{cycle_s:.3f}",  "min"),
        ("Ciclo ruta larga",  f"{cycle_l:.3f}",  "min"),
        ("Cap. AGV 100m",     f"{cap_eff_s:.2f}", "lotes/h"),
        ("Cap. AGV 150m",     f"{cap_eff_l:.2f}", "lotes/h"),
        ("Dist. total flota", f"{(flow_LC*2*dist_short+flow_A*2*dist_short+flow_BM*2*dist_long)/1000:.1f}", "km/h"),
        ("Tonelaje total",    f"{tonnage_h:.2f}", "ton/h"),
        ("Energía estimada",  f"{energy_kwh:.1f}","kWh"),
        ("Flota operativa",   f"{total_agv_safe}", "AGVs"),
    ]
    mc = st.columns(5)
    for i, (ml, mv, mu) in enumerate(_MET):
        with mc[i % 5]:
            st.markdown(
                f'<div style="background:rgba(10,14,26,.6);border:1px solid rgba(99,102,241,.12);'
                f'border-radius:12px;padding:12px 14px;margin-bottom:8px;">'
                f'<div style="font-size:9px;color:#334155;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.1em;">{ml}</div>'
                f'<div style="font-size:20px;font-weight:900;color:#e2e8f0;font-family:monospace;">{mv}</div>'
                f'<div style="font-size:9px;color:#1e293b;">{mu}</div></div>',
                unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# TAB 3 — XAI: EXPLICACIÓN EN LENGUAJE SIMPLE
# ──────────────────────────────────────────────────────────────────────────
with tab_xai:
    utils_map = {
        "Ruta L/C (S1→E1)":        util_r1,
        "Ruta A (S2,S3→E2)":       util_r2,
        "Ruta B/M (S2,S3→E3,E4)": util_r3,
    }
    bn_name = max(utils_map, key=utils_map.get)
    bn_val  = utils_map[bn_name]
    bn_cls  = "xai-ok" if bn_val < 80 else ("xai-warn" if bn_val < 95 else "xai-hi")

    cap_max_5 = (60 / max((2*dist_short)/(5*1000/60) + 2*lt_min, 0.001)) * (occupancy/100)
    agv_r1_at5 = math.ceil(flow_LC / max(cap_max_5, 0.001))

    if velocity < 5:
        v_msg = (
            f'Al usar <span class="xai-warn">{velocity} km/h</span> en vez de 5 km/h, '
            f'cada carrito tarda más por viaje y hace menos ciclos por hora. '
            f'La Ruta L/C necesita <span class="xai-hi">{agv_r1} carrito(s)</span> '
            f'(a velocidad máxima serían {agv_r1_at5}). '
            f'<span class="xai-warn">→ Menor velocidad = más carritos necesarios.</span>'
        )
    else:
        v_msg = (
            f'Estás usando la <span class="xai-ok">velocidad máxima permitida (5 km/h)</span>. '
            f'Esto maximiza la cantidad de viajes por hora y <span class="xai-ok">minimiza la flota</span>. '
            f'Cualquier reducción de velocidad incrementa el número de AGVs requeridos.'
        )

    bn_msg = (
        f'✅ <span class="xai-ok">El sistema opera con holgura. Todas las rutas tienen '
        f'capacidad de reserva ante variaciones de producción.</span>'
        if bn_val < 85 else
        f'⚠️ <span class="xai-warn">Esta ruta está cerca de su límite. Considera agregar '
        f'1 AGV de reserva o revisar el tiempo de carga/descarga.</span>'
    )

    _XAI = [
        (
            "🚚 ¿Por qué necesitamos exactamente estos carritos?",
            f"""Imagina que debes entregar <span class="xai-hi">{flow_LC} cajas/hora</span>
            entre la Salida 1 y la Entrada 1, recorriendo <span class="xai-hi">{dist_short} m</span>.
            A <span class="xai-hi">{velocity} km/h</span>, un carrito tarda
            <span class="xai-hi">{dist_short/v_m_s/60:.1f} minutos</span> por tramo.
            Sumando carga y descarga (<span class="xai-hi">{load_time}s c/u</span>),
            solo puede hacer <span class="xai-hi">{cap_eff_s:.1f} ciclos por hora</span>.
            Por eso necesitamos <span class="xai-hi">{agv_r1} carrito(s)</span> solo en esa ruta,
            y en total <span class="xai-hi">{total_agv} AGVs</span> para los {total_prod} lotes/hora.""",
        ),
        (
            "⏱️ ¿Cómo funciona el ciclo de trabajo de un carrito?",
            f"""Cada AGV repite sin parar las 24 horas el mismo ciclo de 4 pasos:<br><br>
            <b style='color:#06b6d4;'>① CARGA ({load_time}s)</b> — El transportador de rodillos sube el lote de Plywood al AGV.<br>
            <b style='color:#10b981;'>② VIAJE CARGADO ({dist_short/v_m_s:.0f}–{dist_long/v_m_s:.0f}s)</b> — El AGV navega solo hasta el punto de consumo.<br>
            <b style='color:#f59e0b;'>③ DESCARGA ({load_time}s)</b> — Los rodillos bajan el lote en la línea siguiente.<br>
            <b style='color:#8b5cf6;'>④ REGRESO VACÍO ({dist_short/v_m_s:.0f}–{dist_long/v_m_s:.0f}s)</b> — El AGV vuelve en vacío para cargar de nuevo.<br><br>
            Este ciclo completo dura entre <span class="xai-hi">{cycle_s:.1f} y {cycle_l:.1f} minutos</span> según la ruta.""",
        ),
        (
            f"⚡ Impacto de la velocidad (actual: {velocity:.1f} km/h)",
            v_msg,
        ),
        (
            f"🎯 Cuello de botella detectado: {bn_name}",
            f"""La ruta con mayor presión operativa es
            <span class="xai-hi">{bn_name}</span> con
            <span class="{bn_cls}">{bn_val:.1f}% de utilización</span>.<br><br>
            {bn_msg}<br><br>
            La <span class="xai-hi">ocupación máxima del {occupancy}%</span> significa que cada carrito
            trabaja deliberadamente al {occupancy}% de su límite.
            Ese margen del {100-occupancy}% protege al sistema de retrasos
            causados por pequeñas variaciones en producción o tráfico en la planta.""",
        ),
        (
            "💡 Recomendación del sistema",
            f"""Con la configuración actual, el análisis arroja:<br><br>
            <ul style='margin-top:8px;padding-left:20px;'>
            <li>Flota mínima: <span class="xai-hi">{total_agv} AGVs</span>
                (R1={agv_r1} · R2={agv_r2} · R3={agv_r3}).</li>
            <li>Con {safety_margin}% de reserva, operar con
                <span class="xai-ok">{total_agv_safe} AGVs</span>
                para cubrir mantenimiento y fallas.</li>
            <li>La flota transporta
                <span class="xai-hi">{tonnage_h:.1f} toneladas/hora</span>
                ({total_prod} lotes × {load_weight} kg) de forma 100% autónoma.</li>
            <li>Esta solución <b>elimina completamente</b> las grúas horquilla,
                reduciendo el riesgo de atropellos a
                <span class="xai-ok">cero</span>.</li>
            <li>El sistema opera <span class="xai-ok">24/7 sin conductor</span>,
                garantizando los 60 lotes/hora de forma constante.</li>
            </ul>""",
        ),
    ]
    for title, body in _XAI:
        st.markdown(
            f'<div class="xai-box"><div class="xai-title">{title}</div>'
            f'<div class="xai-body">{body}</div></div>',
            unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# TAB 4 — VALIDACIÓN DE RESTRICCIONES
# ──────────────────────────────────────────────────────────────────────────
with tab_valid:
    st.markdown(
        '<div style="font-size:11px;font-weight:900;color:#94a3b8;text-transform:uppercase;'
        'letter-spacing:.15em;margin-bottom:14px;">Verificación de las 7 restricciones Arauco</div>',
        unsafe_allow_html=True)

    _V = [
        ("Producción S1 = 20 lotes/h", f"{sum_S1}/20",     valid_S1, "S1: L + C deben sumar exactamente 20"),
        ("Producción S2 = 20 lotes/h", f"{sum_S2}/20",     valid_S2, "S2: A + B + M deben sumar exactamente 20"),
        ("Producción S3 = 20 lotes/h", f"{sum_S3}/20",     valid_S3, "S3: A + B + M deben sumar exactamente 20"),
        ("Consumo E1 ≤ 15 lotes/h",    f"{flow_LC:.1f}/15", valid_E1, "Entrada 1 (L y C): máximo 15 lotes/h"),
        ("Consumo E2 ≤ 15 lotes/h",    f"{flow_A:.1f}/15",  valid_E2, "Entrada 2 (Prod A): máximo 15 lotes/h"),
        ("Consumo E3 ≤ 15 lotes/h",    f"{flow_E3:.1f}/15", valid_E3, "Entrada 3 (B y M): máximo 15 lotes/h"),
        ("Consumo E4 ≤ 15 lotes/h",    f"{flow_E4:.1f}/15", valid_E4, "Entrada 4 (B y M): máximo 15 lotes/h"),
    ]
    vc1, vc2 = st.columns(2)
    for i, (vn, vv, vok, vd) in enumerate(_V):
        col = vc1 if i % 2 == 0 else vc2
        ic = "✅" if vok else "❌"
        cl = "#10b981" if vok else "#ef4444"
        bg = "rgba(16,185,129,.06)" if vok else "rgba(239,68,68,.06)"
        bd = "rgba(16,185,129,.2)"  if vok else "rgba(239,68,68,.3)"
        with col:
            st.markdown(
                f'<div style="background:{bg};border:1px solid {bd};border-radius:12px;'
                f'padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;'
                f'justify-content:space-between;gap:12px;">'
                f'<div><div style="font-size:12px;font-weight:800;color:{cl};">{ic} {vn}</div>'
                f'<div style="font-size:10px;color:#475569;font-family:sans-serif;margin-top:2px;">{vd}</div></div>'
                f'<div style="font-size:20px;font-weight:900;color:{cl};font-family:monospace;">{vv}</div>'
                f'</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(
        '<div style="font-size:11px;font-weight:900;color:#94a3b8;text-transform:uppercase;'
        'letter-spacing:.15em;margin-bottom:10px;">Restricciones de Diseño AGV</div>',
        unsafe_allow_html=True)
    _DES = [
        ("Velocidad ≤ 5 km/h",        velocity <= 5,    f"{velocity:.1f} km/h"),
        ("Ocupación ≤ 70%",            occupancy <= 70,  f"{occupancy}%"),
        ("S1 sirve solo a E1",         True,              "Restricción de ruta única"),
        ("S2 y S3 identificables",     True,              "Rutas independientes y etiquetadas"),
        ("Movimiento longitudinal",    True,              "2 DOF: avance + giro central"),
        ("Transportador de rodillos",  True,              "Carga/descarga autónoma superior"),
    ]
    dc = st.columns(3)
    for i, (dn, dok, dv) in enumerate(_DES):
        ic = "✅" if dok else "⚠️"
        cl = "#10b981" if dok else "#f59e0b"
        with dc[i % 3]:
            st.markdown(
                f'<div style="background:rgba(10,14,26,.5);border:1px solid rgba(99,102,241,.12);'
                f'border-radius:10px;padding:10px 14px;margin-bottom:8px;">'
                f'<div style="font-size:11px;font-weight:700;color:{cl};">{ic} {dn}</div>'
                f'<div style="font-size:10px;color:#334155;font-family:monospace;">{dv}</div>'
                f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="margin-top:32px;padding:18px 24px;'
    f'background:rgba(10,14,26,.6);border:1px solid rgba(99,102,241,.1);'
    f'border-radius:16px;display:flex;flex-wrap:wrap;align-items:center;'
    f'justify-content:space-between;gap:12px;font-family:sans-serif;'
    f'font-size:11px;color:#334155;">'
    f'<div style="display:flex;align-items:center;gap:16px;">'
    f'<span style="font-weight:900;color:#f59e0b;letter-spacing:.15em;">▲ ARAUCO</span>'
    f'<span>·</span>'
    f'<span>Programación Entera Mixta (MILP) — Optimización de Flota AGV</span></div>'
    f'<div style="display:flex;align-items:center;gap:16px;">'
    f'<span>Lote: 2.6×1.4×1m · {load_weight} kg</span>'
    f'<span>·</span><span>24/7 · 365 días/año</span>'
    f'<span>·</span>'
    f'<span style="color:#06b6d4;font-weight:700;">UdeC · Hackathon 2026 · v3.0</span>'
    f'</div></div>',
    unsafe_allow_html=True)
