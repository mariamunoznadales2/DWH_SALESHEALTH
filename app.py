"""
Saleshealth Customer Intelligence — Dashboard Streamlit (single file, todo embebido).

Ejecutar:
    pip install streamlit
    streamlit run saleshealth_unico.py
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Saleshealth · Customer Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: #0b0f14 !important;
    }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    footer { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .main .block-container { padding: 0 !important; }
    iframe { border: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

DASHBOARD_HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<title>Saleshealth · Customer Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>
/* Saleshealth Customer Intelligence — dashboard prototype styles */
:root {
  --bg: #0b0f14;
  --panel: #11161d;
  --panel-2: #151c24;
  --border: #1f2630;
  --border-2: #2a323d;
  --text: #e6edf3;
  --muted: #8b96a5;
  --muted-2: #6b7785;
  --accent: #5ec2b6;
  --accent-soft: rgba(94, 194, 182, 0.12);
  --warn: #c9a66b;
  --danger: #d98a7a;
  --critical: #c46a6a;
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text); }
body {
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 14px;
  font-feature-settings: "ss01", "cv11";
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
.mono { font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; }

/* Layout */
.app {
  display: grid;
  grid-template-columns: 248px 1fr;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  background: var(--panel);
  border-right: 1px solid var(--border);
  padding: 20px 14px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.brand {
  display: flex; align-items: center; gap: 10px;
  padding: 4px 8px 14px;
}
.brand-mark {
  width: 30px; height: 30px;
  border: 1px solid var(--border-2);
  border-radius: 7px;
  display: grid; place-items: center;
  background: linear-gradient(180deg, #1a2230, #11161d);
  color: var(--accent);
  font-weight: 600;
}
.brand-name { font-weight: 600; letter-spacing: -0.01em; font-size: 15px; }
.brand-sub { color: var(--muted); font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; }

.nav-section {
  font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted-2); padding: 14px 10px 6px;
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 10px;
  border-radius: 7px;
  color: var(--muted);
  cursor: pointer;
  font-size: 13.5px;
  border: 1px solid transparent;
  user-select: none;
}
.nav-item:hover { color: var(--text); background: var(--panel-2); }
.nav-item.active {
  color: var(--text);
  background: var(--panel-2);
  border-color: var(--border);
}
.nav-item .nav-num {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 11px;
  color: var(--muted-2);
  width: 16px;
}
.nav-item.active .nav-num { color: var(--accent); }

.sidebar-footer {
  margin-top: auto;
  padding: 14px 10px 4px;
  border-top: 1px solid var(--border);
  margin-top: 18px;
}
.sf-row { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); padding: 4px 0; }
.sf-row .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 3px rgba(94,194,182,0.18); }
.sf-row b { color: var(--text); font-weight: 600; }

/* Main */
.main {
  padding: 26px 32px 24px;
  max-width: 1400px;
  width: 100%;
}
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.crumbs { font-size: 12px; color: var(--muted); letter-spacing: 0.04em; }
.crumbs b { color: var(--text); font-weight: 500; }
.topbar-actions { display: flex; gap: 8px; align-items: center; }
.chip {
  font-size: 11.5px; color: var(--muted); padding: 5px 10px;
  border: 1px solid var(--border); border-radius: 999px;
  display: inline-flex; align-items: center; gap: 6px;
}
.chip .chip-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }

.page-title {
  font-size: 24px; font-weight: 600; letter-spacing: -0.015em;
  margin: 0 0 4px;
}
.page-sub { color: var(--muted); font-size: 13px; margin-bottom: 22px; }

.section-title { font-size: 14px; font-weight: 600; letter-spacing: -0.005em; margin: 0 0 10px; }
.section-sub { color: var(--muted); font-size: 12px; margin-bottom: 12px; }

/* Grids */
.grid { display: grid; gap: 14px; }
.grid-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 10px; }
.grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-12 { grid-template-columns: 1.3fr 1fr; }

/* KPI card */
.kpi {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 14px;
  min-width: 0;
}
.kpi-label {
  color: var(--muted);
  font-size: 10.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.kpi-value {
  font-size: 21px; font-weight: 600;
  margin-top: 8px; letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kpi-value.sm { font-size: 19px; }
.kpi-delta { color: var(--accent); font-size: 11.5px; margin-top: 4px; }
.kpi-delta.warn { color: var(--warn); }
.kpi-delta.danger { color: var(--danger); }
.kpi-spark { margin-top: 8px; height: 28px; }

/* Panels */
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
}
.panel-tight { padding: 12px 14px; }
.panel-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}

/* Pills / badges */
.pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 2px 10px; border-radius: 999px;
  font-size: 11px; border: 1px solid var(--border); color: var(--muted);
  background: rgba(255,255,255,0.02);
}
.pill.churn-Bajo { color: var(--accent); border-color: rgba(94,194,182,0.4); background: rgba(94,194,182,0.08); }
.pill.churn-Medio { color: var(--warn); border-color: rgba(201,166,107,0.4); background: rgba(201,166,107,0.08); }
.pill.churn-Alto { color: var(--danger); border-color: rgba(217,138,122,0.4); background: rgba(217,138,122,0.08); }
.pill.churn-Critico { color: var(--critical); border-color: rgba(196,106,106,0.5); background: rgba(196,106,106,0.1); }

/* Tables */
table.tbl {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 12.5px;
  font-variant-numeric: tabular-nums;
}
table.tbl th {
  text-align: left;
  font-weight: 500;
  color: var(--muted);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  background: var(--panel);
  position: sticky; top: 0;
  white-space: nowrap;
}
table.tbl td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
table.tbl tr:hover td { background: var(--panel-2); }
table.tbl td.num, table.tbl th.num { text-align: right; }
table.tbl td.muted { color: var(--muted); }
table.tbl td.mono { font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 11.5px; }

/* Selects, inputs */
.input, .select {
  background: var(--panel-2);
  border: 1px solid var(--border-2);
  color: var(--text);
  border-radius: 7px;
  padding: 8px 12px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  width: 100%;
}
.input:focus, .select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(94,194,182,0.12);
}
.field-label {
  font-size: 11px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 6px;
}

/* Customer 360 hero */
.cust-hero {
  background: linear-gradient(180deg, #141b24 0%, var(--panel) 100%);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 22px 24px;
  margin-bottom: 16px;
}
.cust-hero-row { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.cust-name { font-size: 22px; font-weight: 600; letter-spacing: -0.015em; }
.cust-id { color: var(--muted); font-size: 12px; }
.cust-meta { color: var(--muted); font-size: 12.5px; margin-top: 6px; }
.cust-meta b { color: var(--text); font-weight: 500; }

/* Action card */
.action-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: 14px 16px;
  color: #cfd6df;
  font-size: 13.5px;
  line-height: 1.6;
}

/* Findings */
.findings { display: grid; gap: 1px; background: var(--border); border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
.finding-row {
  display: grid; grid-template-columns: 240px 1fr;
  background: var(--panel);
  padding: 14px 18px;
  align-items: start;
}
.finding-row:hover { background: var(--panel-2); }
.finding-title { font-weight: 500; font-size: 13.5px; }
.finding-text { color: var(--muted); font-size: 13px; line-height: 1.55; }

/* Validation grid */
.checks { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--border); border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
.check {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px;
  background: var(--panel);
  font-size: 12.5px;
}
.check .ok {
  color: var(--accent);
  font-size: 11px;
  border: 1px solid rgba(94,194,182,0.4);
  background: rgba(94,194,182,0.08);
  padding: 2px 8px;
  border-radius: 999px;
}

/* Streamlit-style radio (segmented) */
.seg {
  display: inline-flex;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  background: var(--panel-2);
}
.seg-item {
  padding: 7px 14px;
  font-size: 12.5px;
  color: var(--muted);
  cursor: pointer;
  border-right: 1px solid var(--border);
}
.seg-item:last-child { border-right: none; }
.seg-item.active { background: var(--panel); color: var(--text); }

/* Plotly container reset */
.chart { width: 100%; }

/* Misc */
.spacer-12 { height: 12px; }
.spacer-20 { height: 20px; }
.spacer-28 { height: 28px; }

.legend-explain {
  display: grid; gap: 10px; grid-template-columns: repeat(3, 1fr);
  margin-top: 14px;
}
.legend-explain .item {
  background: var(--panel-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 12.5px;
}
.legend-explain .item h4 { margin: 0 0 4px; font-size: 12px; color: var(--accent); font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
.legend-explain .item p { margin: 0; color: var(--muted); line-height: 1.55; }

/* Scroll table wrapper */
.table-wrap {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  max-height: 520px;
  overflow-y: auto;
}

/* Quality callout */
.callout {
  background: var(--panel);
  border: 1px solid var(--border);
  border-left: 3px solid var(--warn);
  border-radius: 8px;
  padding: 16px 18px;
  font-size: 13px;
  color: #cfd6df;
  line-height: 1.6;
}
.callout code, .callout .mono {
  background: rgba(255,255,255,0.04);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 12px;
}

/* Tweaks */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #1f2630; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #2a323d; }

/* Embed adjustments */
html, body { min-height: 100vh; }
.app { min-height: 100vh; }
</style>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" crossorigin="anonymous"></script>
</head>
<body>
<div id="root"></div>
<script>
window.__CUSTOMERS__ = [{"customer_id":781,"full_name":"Félix Pacheco Sampedro","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":26.67,"numero_compras":1,"recencia_dias":985,"frecuencia_mensual":0.0309,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.14295,"pca_2":0.446904,"lineas_coste_imputado":0},{"customer_id":1060,"full_name":"Belén Maldonado Yuste","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":18.37,"numero_compras":1,"recencia_dias":1430,"frecuencia_mensual":0.0213,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.226655,"pca_2":1.18284,"lineas_coste_imputado":0},{"customer_id":1189,"full_name":"Fabián Esteban Huertas","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":19.05,"numero_compras":1,"recencia_dias":1379,"frecuencia_mensual":0.0221,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.226286,"pca_2":1.108412,"lineas_coste_imputado":0},{"customer_id":2030,"full_name":"Camila Bonilla Collado","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":18.49,"numero_compras":1,"recencia_dias":1421,"frecuencia_mensual":0.0214,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.226605,"pca_2":1.169783,"lineas_coste_imputado":0},{"customer_id":2431,"full_name":"Joel Aizpurua Belinchón","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":49.66,"numero_compras":1,"recencia_dias":529,"frecuencia_mensual":0.0575,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.041834,"pca_2":-0.347406,"lineas_coste_imputado":0},{"customer_id":2705,"full_name":"Fabiola Caballero Arriaga","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":49.28,"numero_compras":1,"recencia_dias":533,"frecuencia_mensual":0.0571,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.042237,"pca_2":-0.340694,"lineas_coste_imputado":0},{"customer_id":3499,"full_name":"Eladio Galán Abarca","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":19.4,"numero_compras":1,"recencia_dias":1354,"frecuencia_mensual":0.0225,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.226089,"pca_2":1.071901,"lineas_coste_imputado":0},{"customer_id":3865,"full_name":"Ariadna Antúnez Cuadrado","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":62.54,"numero_compras":1,"recencia_dias":420,"frecuencia_mensual":0.0725,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.027402,"pca_2":-0.539858,"lineas_coste_imputado":0},{"customer_id":5381,"full_name":"Alejo Espinosa Gimeno","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":67.36,"numero_compras":1,"recencia_dias":390,"frecuencia_mensual":0.078,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.021949,"pca_2":-0.59634,"lineas_coste_imputado":0},{"customer_id":5713,"full_name":"Gumersindo Gimeno Cabezas","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":14.46,"numero_compras":1,"recencia_dias":1817,"frecuencia_mensual":0.0168,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.227923,"pca_2":1.743744,"lineas_coste_imputado":0},{"customer_id":767,"full_name":"Iago Tejada Guijarro","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":16.71,"numero_compras":1,"recencia_dias":1399,"frecuencia_mensual":0.0218,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.261005,"pca_2":1.138596,"lineas_coste_imputado":0},{"customer_id":771,"full_name":"Fabián Wenceslao Pacheco","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":16.17,"numero_compras":1,"recencia_dias":1446,"frecuencia_mensual":0.021,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.261303,"pca_2":1.207242,"lineas_coste_imputado":0},{"customer_id":791,"full_name":"Jon Luque Burgos","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":25.22,"numero_compras":1,"recencia_dias":927,"frecuencia_mensual":0.0328,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.176854,"pca_2":0.36152,"lineas_coste_imputado":0},{"customer_id":863,"full_name":"Lara Valverde Luque","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":16.57,"numero_compras":1,"recencia_dias":1411,"frecuencia_mensual":0.0216,"tasa_devolucion_importe":0,"churn_risk_score":68,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Clientes medios","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.261081,"pca_2":1.156116,"lineas_coste_imputado":0},{"customer_id":719,"full_name":"Ana Álvarez Pérez","ingresos_netos":16630.17,"margen_neto_estimado":6652.48,"cltv_historico_margen":6652.48,"cltv_estimado_12m_margen":1189.34,"numero_compras":24,"recencia_dias":383,"frecuencia_mensual":0.3576,"tasa_devolucion_importe":0.0177,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-8.690511,"pca_2":0.66103,"lineas_coste_imputado":0},{"customer_id":657,"full_name":"David Sánchez Sánchez","ingresos_netos":13839.48,"margen_neto_estimado":5536.08,"cltv_historico_margen":5536.08,"cltv_estimado_12m_margen":957.41,"numero_compras":22,"recencia_dias":460,"frecuencia_mensual":0.3171,"tasa_devolucion_importe":0.0043,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.236122,"pca_2":0.72126,"lineas_coste_imputado":0},{"customer_id":350,"full_name":"Alejandro Pérez Sánchez","ingresos_netos":13736.1,"margen_neto_estimado":5494.76,"cltv_historico_margen":5494.76,"cltv_estimado_12m_margen":919.36,"numero_compras":28,"recencia_dias":497,"frecuencia_mensual":0.3904,"tasa_devolucion_importe":0.0098,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-8.028943,"pca_2":1.128268,"lineas_coste_imputado":2},{"customer_id":388,"full_name":"Carlos García Álvarez","ingresos_netos":13452.5,"margen_neto_estimado":5381.36,"cltv_historico_margen":5381.36,"cltv_estimado_12m_margen":905.36,"numero_compras":18,"recencia_dias":434,"frecuencia_mensual":0.2524,"tasa_devolucion_importe":0.0268,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.888543,"pca_2":1.33119,"lineas_coste_imputado":2},{"customer_id":65,"full_name":"Carlos Fernández Álvarez","ingresos_netos":13187.64,"margen_neto_estimado":5275.36,"cltv_historico_margen":5275.36,"cltv_estimado_12m_margen":904.19,"numero_compras":19,"recencia_dias":480,"frecuencia_mensual":0.2714,"tasa_devolucion_importe":0.009,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-6.861082,"pca_2":0.77614,"lineas_coste_imputado":2},{"customer_id":210,"full_name":"David Díaz López","ingresos_netos":12941.03,"margen_neto_estimado":5176.68,"cltv_historico_margen":5176.68,"cltv_estimado_12m_margen":916.97,"numero_compras":18,"recencia_dias":625,"frecuencia_mensual":0.2657,"tasa_devolucion_importe":0.0307,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.303738,"pca_2":1.166802,"lineas_coste_imputado":1},{"customer_id":94,"full_name":"Javier Gómez Gómez","ingresos_netos":12760.51,"margen_neto_estimado":5104.48,"cltv_historico_margen":5104.48,"cltv_estimado_12m_margen":986.98,"numero_compras":22,"recencia_dias":491,"frecuencia_mensual":0.3545,"tasa_devolucion_importe":0.0329,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.702175,"pca_2":0.964969,"lineas_coste_imputado":2},{"customer_id":372,"full_name":"Laura Fernández Gómez","ingresos_netos":12049.74,"margen_neto_estimado":4820.2,"cltv_historico_margen":4820.2,"cltv_estimado_12m_margen":804.28,"numero_compras":22,"recencia_dias":514,"frecuencia_mensual":0.3059,"tasa_devolucion_importe":0.0448,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.329932,"pca_2":1.358928,"lineas_coste_imputado":1},{"customer_id":356,"full_name":"Javier Martínez López","ingresos_netos":11258.12,"margen_neto_estimado":4503.48,"cltv_historico_margen":4503.48,"cltv_estimado_12m_margen":762.94,"numero_compras":20,"recencia_dias":536,"frecuencia_mensual":0.2824,"tasa_devolucion_importe":0.0027,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-5.990623,"pca_2":0.782374,"lineas_coste_imputado":0},{"customer_id":115,"full_name":"María Álvarez Ruiz","ingresos_netos":10891.31,"margen_neto_estimado":4356.72,"cltv_historico_margen":4356.72,"cltv_estimado_12m_margen":729.95,"numero_compras":15,"recencia_dias":559,"frecuencia_mensual":0.2094,"tasa_devolucion_importe":0.1037,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-7.237694,"pca_2":1.808708,"lineas_coste_imputado":1},{"customer_id":552,"full_name":"Javier Sánchez Gómez","ingresos_netos":10322.95,"margen_neto_estimado":4129.4,"cltv_historico_margen":4129.4,"cltv_estimado_12m_margen":882.03,"numero_compras":20,"recencia_dias":403,"frecuencia_mensual":0.356,"tasa_devolucion_importe":0.0171,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-5.894758,"pca_2":0.266665,"lineas_coste_imputado":0},{"customer_id":348,"full_name":"Ana Pérez Pérez","ingresos_netos":10229.61,"margen_neto_estimado":4092.04,"cltv_historico_margen":4092.04,"cltv_estimado_12m_margen":686.23,"numero_compras":15,"recencia_dias":865,"frecuencia_mensual":0.2096,"tasa_devolucion_importe":0.0201,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-5.523627,"pca_2":1.242861,"lineas_coste_imputado":2},{"customer_id":626,"full_name":"Carlos Ruiz Fernández","ingresos_netos":10051.46,"margen_neto_estimado":4020.84,"cltv_historico_margen":4020.84,"cltv_estimado_12m_margen":700.34,"numero_compras":18,"recencia_dias":402,"frecuencia_mensual":0.2613,"tasa_devolucion_importe":0.0519,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-6.723882,"pca_2":1.352567,"lineas_coste_imputado":0},{"customer_id":286,"full_name":"Sergio Gómez López","ingresos_netos":10023.7,"margen_neto_estimado":4009.68,"cltv_historico_margen":4009.68,"cltv_estimado_12m_margen":746.83,"numero_compras":13,"recencia_dias":543,"frecuencia_mensual":0.2018,"tasa_devolucion_importe":0.0123,"churn_risk_score":58,"churn_risk_level":"Alto","recommended_action":"Campana de reactivacion personalizada","segmento_rfm":"Alto valor","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-5.448548,"pca_2":0.753291,"lineas_coste_imputado":0},{"customer_id":801,"full_name":"Gala Llorente Miralles","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.51,"numero_compras":1,"recencia_dias":1389,"frecuencia_mensual":0.0219,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.53142,"pca_2":1.284391,"lineas_coste_imputado":0},{"customer_id":865,"full_name":"Xavi Naranjo Barrios","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":14.73,"numero_compras":1,"recencia_dias":991,"frecuencia_mensual":0.0307,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.450703,"pca_2":0.619662,"lineas_coste_imputado":0},{"customer_id":868,"full_name":"Yolanda Escribano Esteban","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.43,"numero_compras":1,"recencia_dias":1399,"frecuencia_mensual":0.0218,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.53143,"pca_2":1.298838,"lineas_coste_imputado":0},{"customer_id":978,"full_name":"Nicolás Carretero Alcaraz","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":15.4,"numero_compras":1,"recencia_dias":948,"frecuencia_mensual":0.0321,"tasa_devolucion_importe":0.5,"churn_risk_score":80,"churn_risk_level":"Critico","recommended_action":"Revisar experiencia y causas de devolucion","segmento_rfm":"Clientes dormidos","cluster_id":3,"cluster_name":"Clientes con mas devoluciones","pca_1":1.177344,"pca_2":1.784683,"lineas_coste_imputado":0},{"customer_id":1062,"full_name":"Teo Dolores Maldonado","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":15.06,"numero_compras":1,"recencia_dias":969,"frecuencia_mensual":0.0314,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.450383,"pca_2":0.586859,"lineas_coste_imputado":0},{"customer_id":1139,"full_name":"Tania Ferrer Wamba","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.1,"numero_compras":1,"recencia_dias":1445,"frecuencia_mensual":0.0211,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.53154,"pca_2":1.365723,"lineas_coste_imputado":0},{"customer_id":1178,"full_name":"Bruno Guijarro Salcedo","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":14.74,"numero_compras":1,"recencia_dias":990,"frecuencia_mensual":0.0307,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.450704,"pca_2":0.618235,"lineas_coste_imputado":0},{"customer_id":1252,"full_name":"Ximena Rosales Camposano","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.21,"numero_compras":1,"recencia_dias":1429,"frecuencia_mensual":0.0213,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.531522,"pca_2":1.342545,"lineas_coste_imputado":0},{"customer_id":1584,"full_name":"Cora Zamora Pacheco","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":15.63,"numero_compras":1,"recencia_dias":934,"frecuencia_mensual":0.0326,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.449808,"pca_2":0.534476,"lineas_coste_imputado":0},{"customer_id":1657,"full_name":"Zaida Ferrer Orellana","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.29,"numero_compras":1,"recencia_dias":1418,"frecuencia_mensual":0.0215,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.531483,"pca_2":1.326488,"lineas_coste_imputado":0},{"customer_id":1684,"full_name":"Ximena Tejada Herranz","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.56,"numero_compras":1,"recencia_dias":1382,"frecuencia_mensual":0.022,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.531406,"pca_2":1.274225,"lineas_coste_imputado":0},{"customer_id":1715,"full_name":"Héctor Keller Huertas","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":15.02,"numero_compras":1,"recencia_dias":972,"frecuencia_mensual":0.0313,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.450425,"pca_2":0.591337,"lineas_coste_imputado":0},{"customer_id":1808,"full_name":"Alba Del Rosal Ayala","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":14.91,"numero_compras":1,"recencia_dias":979,"frecuencia_mensual":0.0311,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.450522,"pca_2":0.601735,"lineas_coste_imputado":0},{"customer_id":1895,"full_name":"Alba Barón Canales","ingresos_netos":99.9,"margen_neto_estimado":39.96,"cltv_historico_margen":39.96,"cltv_estimado_12m_margen":10.47,"numero_compras":1,"recencia_dias":1394,"frecuencia_mensual":0.0218,"tasa_devolucion_importe":0,"churn_risk_score":60,"churn_risk_level":"Alto","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes dormidos","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":1.531444,"pca_2":1.291709,"lineas_coste_imputado":0},{"customer_id":5751,"full_name":"Hélder Andrade Carrillo","ingresos_netos":1199.97,"margen_neto_estimado":480,"cltv_historico_margen":480,"cltv_estimado_12m_margen":192.24,"numero_compras":1,"recencia_dias":912,"frecuencia_mensual":0.0334,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-1.00313,"pca_2":-0.073497,"lineas_coste_imputado":0},{"customer_id":2718,"full_name":"Araceli Amorrortu Arévalo","ingresos_netos":1199.97,"margen_neto_estimado":480,"cltv_historico_margen":480,"cltv_estimado_12m_margen":125.59,"numero_compras":1,"recencia_dias":1396,"frecuencia_mensual":0.0218,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.874672,"pca_2":0.763823,"lineas_coste_imputado":0},{"customer_id":3509,"full_name":"Anabel Caparrós Balaguer","ingresos_netos":1049.97,"margen_neto_estimado":420,"cltv_historico_margen":420,"cltv_estimado_12m_margen":112.38,"numero_compras":1,"recencia_dias":1365,"frecuencia_mensual":0.0223,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.614745,"pca_2":0.72479,"lineas_coste_imputado":0},{"customer_id":1193,"full_name":"Ximena Aranda Quintana","ingresos_netos":899.97,"margen_neto_estimado":360,"cltv_historico_margen":360,"cltv_estimado_12m_margen":94.19,"numero_compras":1,"recencia_dias":1396,"frecuencia_mensual":0.0218,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.351203,"pca_2":0.779294,"lineas_coste_imputado":0},{"customer_id":1394,"full_name":"Quim Miralles Maldonado","ingresos_netos":899.97,"margen_neto_estimado":360,"cltv_historico_margen":360,"cltv_estimado_12m_margen":143.24,"numero_compras":1,"recencia_dias":918,"frecuencia_mensual":0.0332,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.466262,"pca_2":-0.036392,"lineas_coste_imputado":0},{"customer_id":2496,"full_name":"Leticia Ferro Calleja","ingresos_netos":899.97,"margen_neto_estimado":360,"cltv_historico_margen":360,"cltv_estimado_12m_margen":139,"numero_compras":1,"recencia_dias":946,"frecuencia_mensual":0.0322,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.462911,"pca_2":0.008327,"lineas_coste_imputado":0},{"customer_id":4823,"full_name":"Fermín Bandeira Casillas","ingresos_netos":899.97,"margen_neto_estimado":360,"cltv_historico_margen":360,"cltv_estimado_12m_margen":99.24,"numero_compras":1,"recencia_dias":1325,"frecuencia_mensual":0.023,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.432573,"pca_2":0.592692,"lineas_coste_imputado":0},{"customer_id":5700,"full_name":"Almudena Durán Bandeira","ingresos_netos":899.97,"margen_neto_estimado":360,"cltv_historico_margen":360,"cltv_estimado_12m_margen":75.4,"numero_compras":1,"recencia_dias":1744,"frecuencia_mensual":0.0175,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.33836,"pca_2":1.295204,"lineas_coste_imputado":0},{"customer_id":1042,"full_name":"Rita Doménech Del Río","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":83.91,"numero_compras":1,"recencia_dias":1393,"frecuencia_mensual":0.0219,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.166696,"pca_2":0.777309,"lineas_coste_imputado":0},{"customer_id":1373,"full_name":"Karen Doménech Ferrer","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":117.7,"numero_compras":1,"recencia_dias":993,"frecuencia_mensual":0.0307,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.26987,"pca_2":0.088343,"lineas_coste_imputado":0},{"customer_id":1464,"full_name":"Gisela Catalá Burgos","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":85,"numero_compras":1,"recencia_dias":1375,"frecuencia_mensual":0.0221,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.167442,"pca_2":0.750581,"lineas_coste_imputado":0},{"customer_id":1616,"full_name":"Xavi Aranda Del Río","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":84.88,"numero_compras":1,"recencia_dias":1377,"frecuencia_mensual":0.0221,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.167368,"pca_2":0.753508,"lineas_coste_imputado":0},{"customer_id":1848,"full_name":"Fidel Ferrán Barahona","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":116.53,"numero_compras":1,"recencia_dias":1003,"frecuencia_mensual":0.0303,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.268919,"pca_2":0.104147,"lineas_coste_imputado":0},{"customer_id":1918,"full_name":"Dara Esparza Carbajo","ingresos_netos":799.98,"margen_neto_estimado":320,"cltv_historico_margen":320,"cltv_estimado_12m_margen":83.97,"numero_compras":1,"recencia_dias":1392,"frecuencia_mensual":0.0219,"tasa_devolucion_importe":0,"churn_risk_score":75,"churn_risk_level":"Critico","recommended_action":"Recuperacion prioritaria de alto valor","segmento_rfm":"Valiosos en riesgo","cluster_id":2,"cluster_name":"Clientes inactivos o en riesgo","pca_1":-0.166733,"pca_2":0.775845,"lineas_coste_imputado":0},{"customer_id":1117,"full_name":"Iago Gaztelu Wenceslao","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":226.46,"numero_compras":1,"recencia_dias":116,"frecuencia_mensual":0.2624,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.756927,"pca_2":-1.528856,"lineas_coste_imputado":0},{"customer_id":3262,"full_name":"Genoveva Colunga Casillas","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":245.5,"numero_compras":1,"recencia_dias":107,"frecuencia_mensual":0.2845,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.734291,"pca_2":-1.597173,"lineas_coste_imputado":0},{"customer_id":3330,"full_name":"Elisa Alcántara Andrade","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":241,"numero_compras":1,"recencia_dias":109,"frecuencia_mensual":0.2792,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.73967,"pca_2":-1.581062,"lineas_coste_imputado":0},{"customer_id":4163,"full_name":"Caleb Coronado Casillas","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":238.81,"numero_compras":1,"recencia_dias":110,"frecuencia_mensual":0.2767,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.742259,"pca_2":-1.573333,"lineas_coste_imputado":0},{"customer_id":5643,"full_name":"Fermín Almeida Barrenechea","ingresos_netos":179.8,"margen_neto_estimado":71.92,"cltv_historico_margen":71.92,"cltv_estimado_12m_margen":245.5,"numero_compras":1,"recencia_dias":107,"frecuencia_mensual":0.2845,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.734291,"pca_2":-1.597173,"lineas_coste_imputado":0},{"customer_id":783,"full_name":"Hugo Jara Doménech","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":303.58,"numero_compras":1,"recencia_dias":77,"frecuencia_mensual":0.3953,"tasa_devolucion_importe":0,"churn_risk_score":16,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.614544,"pca_2":-1.974055,"lineas_coste_imputado":0},{"customer_id":804,"full_name":"Karla Garrido Yuste","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":768,"numero_compras":1,"recencia_dias":1,"frecuencia_mensual":1,"tasa_devolucion_importe":0,"churn_risk_score":16,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.026481,"pca_2":-3.55809,"lineas_coste_imputado":0},{"customer_id":827,"full_name":"Tania Maldonado Huertas","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":216.44,"numero_compras":1,"recencia_dias":108,"frecuencia_mensual":0.2818,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.800549,"pca_2":-1.572659,"lineas_coste_imputado":0},{"customer_id":856,"full_name":"Fiona Escalante Burgos","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":205.05,"numero_compras":1,"recencia_dias":114,"frecuencia_mensual":0.267,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.814674,"pca_2":-1.527932,"lineas_coste_imputado":0},{"customer_id":957,"full_name":"Zaida Tejada Tejada","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":768,"numero_compras":1,"recencia_dias":29,"frecuencia_mensual":1,"tasa_devolucion_importe":0,"churn_risk_score":16,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.026236,"pca_2":-3.518328,"lineas_coste_imputado":0},{"customer_id":1029,"full_name":"Fabián Quirós Doménech","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":275.01,"numero_compras":1,"recencia_dias":85,"frecuencia_mensual":0.3581,"tasa_devolucion_importe":0,"churn_risk_score":16,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.727771,"pca_2":-1.791876,"lineas_coste_imputado":0},{"customer_id":1035,"full_name":"Pau Rosales Fajardo","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":254.09,"numero_compras":1,"recencia_dias":92,"frecuencia_mensual":0.3308,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.753794,"pca_2":-1.715212,"lineas_coste_imputado":0},{"customer_id":1074,"full_name":"Leo Salcedo Valcárcel","ingresos_netos":159.99,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":198.1,"numero_compras":1,"recencia_dias":118,"frecuencia_mensual":0.2579,"tasa_devolucion_importe":0,"churn_risk_score":29,"churn_risk_level":"Bajo","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.823316,"pca_2":-1.500028,"lineas_coste_imputado":0},{"customer_id":1136,"full_name":"Ona Rosales Zúñiga","ingresos_netos":159.98,"margen_neto_estimado":64,"cltv_historico_margen":64,"cltv_estimado_12m_margen":667.89,"numero_compras":1,"recencia_dias":35,"frecuencia_mensual":0.8696,"tasa_devolucion_importe":0,"churn_risk_score":16,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes fieles recientes","cluster_id":0,"cluster_name":"Clientes recientes con potencial","pca_1":0.150916,"pca_2":-3.19097,"lineas_coste_imputado":0},{"customer_id":183,"full_name":"Alejandro Pérez Pérez","ingresos_netos":23932.15,"margen_neto_estimado":9573.44,"cltv_historico_margen":9573.44,"cltv_estimado_12m_margen":1599.59,"numero_compras":33,"recencia_dias":73,"frecuencia_mensual":0.4595,"tasa_devolucion_importe":0.0397,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-13.71569,"pca_2":1.39392,"lineas_coste_imputado":2},{"customer_id":228,"full_name":"Carlos García López","ingresos_netos":22148.45,"margen_neto_estimado":8859.88,"cltv_historico_margen":8859.88,"cltv_estimado_12m_margen":1485.12,"numero_compras":30,"recencia_dias":8,"frecuencia_mensual":0.4191,"tasa_devolucion_importe":0.0054,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.517369,"pca_2":0.585044,"lineas_coste_imputado":0},{"customer_id":140,"full_name":"Javier Sánchez Ruiz","ingresos_netos":21038.75,"margen_neto_estimado":8416,"cltv_historico_margen":8416,"cltv_estimado_12m_margen":1466.58,"numero_compras":28,"recencia_dias":169,"frecuencia_mensual":0.4066,"tasa_devolucion_importe":0.0182,"churn_risk_score":36,"churn_risk_level":"Medio","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.923324,"pca_2":1.195796,"lineas_coste_imputado":3},{"customer_id":456,"full_name":"David Díaz Díaz","ingresos_netos":20916.09,"margen_neto_estimado":8361.53,"cltv_historico_margen":8361.53,"cltv_estimado_12m_margen":1438.55,"numero_compras":31,"recencia_dias":157,"frecuencia_mensual":0.4444,"tasa_devolucion_importe":0.0301,"churn_risk_score":36,"churn_risk_level":"Medio","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.889493,"pca_2":1.18631,"lineas_coste_imputado":1},{"customer_id":212,"full_name":"Sergio Álvarez Martínez","ingresos_netos":20781.53,"margen_neto_estimado":8313.08,"cltv_historico_margen":8313.08,"cltv_estimado_12m_margen":1398.6,"numero_compras":34,"recencia_dias":147,"frecuencia_mensual":0.4767,"tasa_devolucion_importe":0.0235,"churn_risk_score":36,"churn_risk_level":"Medio","recommended_action":"Mantener seguimiento comercial","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.164303,"pca_2":0.742812,"lineas_coste_imputado":0},{"customer_id":343,"full_name":"Alejandro Fernández Pérez","ingresos_netos":20682.93,"margen_neto_estimado":8273.6,"cltv_historico_margen":8273.6,"cltv_estimado_12m_margen":1517.8,"numero_compras":30,"recencia_dias":46,"frecuencia_mensual":0.4586,"tasa_devolucion_importe":0.0229,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.620872,"pca_2":0.647432,"lineas_coste_imputado":1},{"customer_id":559,"full_name":"Alejandro Pérez López","ingresos_netos":20298.94,"margen_neto_estimado":8119.92,"cltv_historico_margen":8119.92,"cltv_estimado_12m_margen":1406.26,"numero_compras":26,"recencia_dias":21,"frecuencia_mensual":0.3752,"tasa_devolucion_importe":0.0384,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.181546,"pca_2":0.833837,"lineas_coste_imputado":0},{"customer_id":14,"full_name":"Ana Martínez Fernández","ingresos_netos":19501.69,"margen_neto_estimado":7801,"cltv_historico_margen":7801,"cltv_estimado_12m_margen":1316.08,"numero_compras":22,"recencia_dias":31,"frecuencia_mensual":0.3093,"tasa_devolucion_importe":0,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-9.414268,"pca_2":0.206569,"lineas_coste_imputado":1},{"customer_id":542,"full_name":"Carlos García Pérez","ingresos_netos":19492.83,"margen_neto_estimado":7797.64,"cltv_historico_margen":7797.64,"cltv_estimado_12m_margen":1327.16,"numero_compras":25,"recencia_dias":12,"frecuencia_mensual":0.3546,"tasa_devolucion_importe":0.0274,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.216374,"pca_2":1.055129,"lineas_coste_imputado":2},{"customer_id":3,"full_name":"Alejandro López Álvarez","ingresos_netos":19416.56,"margen_neto_estimado":7767.04,"cltv_historico_margen":7767.04,"cltv_estimado_12m_margen":1446.67,"numero_compras":24,"recencia_dias":53,"frecuencia_mensual":0.3725,"tasa_devolucion_importe":0.0225,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.136867,"pca_2":0.802977,"lineas_coste_imputado":1},{"customer_id":448,"full_name":"Marta Díaz Ruiz","ingresos_netos":19406.65,"margen_neto_estimado":7763.04,"cltv_historico_margen":7763.04,"cltv_estimado_12m_margen":1330.57,"numero_compras":27,"recencia_dias":37,"frecuencia_mensual":0.3856,"tasa_devolucion_importe":0.0298,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-10.756236,"pca_2":0.826213,"lineas_coste_imputado":1},{"customer_id":214,"full_name":"Javier Ruiz García","ingresos_netos":19312.32,"margen_neto_estimado":7725.36,"cltv_historico_margen":7725.36,"cltv_estimado_12m_margen":1376.43,"numero_compras":29,"recencia_dias":8,"frecuencia_mensual":0.4306,"tasa_devolucion_importe":0.0282,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.627876,"pca_2":1.039951,"lineas_coste_imputado":2},{"customer_id":301,"full_name":"Carlos Martínez López","ingresos_netos":19295.22,"margen_neto_estimado":7718.52,"cltv_historico_margen":7718.52,"cltv_estimado_12m_margen":1290.25,"numero_compras":27,"recencia_dias":67,"frecuencia_mensual":0.3761,"tasa_devolucion_importe":0.0474,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.160597,"pca_2":1.144549,"lineas_coste_imputado":1},{"customer_id":750,"full_name":"Laura García Ruiz","ingresos_netos":19201.55,"margen_neto_estimado":7681.04,"cltv_historico_margen":7681.04,"cltv_estimado_12m_margen":1310.98,"numero_compras":31,"recencia_dias":38,"frecuencia_mensual":0.4409,"tasa_devolucion_importe":0.0357,"churn_risk_score":23,"churn_risk_level":"Bajo","recommended_action":"Fidelizacion y venta cruzada","segmento_rfm":"Clientes estrella","cluster_id":1,"cluster_name":"Clientes de alto valor","pca_1":-11.664303,"pca_2":1.190769,"lineas_coste_imputado":3}];
window.__STATS__ = {"total":5750,"sumIngresos":9402367.86000154,"sumMargen":3761148.119999932,"avgChurn":48.30313043478261,"bySeg":{"Clientes medios":2023,"Alto valor":356,"Clientes dormidos":1057,"Valiosos en riesgo":726,"Clientes fieles recientes":370,"Clientes estrella":1218},"byChurn":{"Bajo":1745,"Alto":2456,"Critico":619,"Medio":930},"marginBySeg":{"Clientes medios":66491.95999999969,"Alto valor":155690.48000000013,"Clientes dormidos":20479.079999999885,"Valiosos en riesgo":93669.55999999995,"Clientes fieles recientes":19993.359999999942,"Clientes estrella":3404823.6799999964},"churnBySeg":{"Clientes medios":45.59515570934256,"Alto valor":65.49157303370787,"Clientes dormidos":63.152317880794705,"Valiosos en riesgo":71.81542699724518,"Clientes fieles recientes":20.045945945945945,"Clientes estrella":29.45977011494253},"byCluster":{"Clientes recientes con potencial":1469,"Clientes inactivos o en riesgo":3134,"Clientes con mas devoluciones":401,"Clientes de alto valor":746},"churnByCluster":{"Clientes recientes con potencial":20.513274336283185,"Clientes inactivos o en riesgo":62.71920867900447,"Clientes con mas devoluciones":67.58852867830424,"Clientes de alto valor":32.09651474530831},"clusterSummary":[{"cluster_name":"Clientes recientes con potencial","clientes":1469,"ingresos":277210.3599999975,"margen":110890.52000000027,"churn_medio":20.513274336283185,"tasa_dev_media":0.007714840027229407},{"cluster_name":"Clientes inactivos o en riesgo","clientes":3134,"ingresos":506059.91999998724,"margen":202437.03999999975,"churn_medio":62.71920867900447,"tasa_dev_media":0.0015549138481174222},{"cluster_name":"Clientes con mas devoluciones","clientes":401,"ingresos":10490.099999999984,"margen":4196.320000000001,"churn_medio":67.58852867830424,"tasa_dev_media":0.8985870324189525},{"cluster_name":"Clientes de alto valor","clientes":746,"ingresos":8608607.48,"margen":3443624.2400000035,"churn_medio":32.09651474530831,"tasa_dev_media":0.025274932975871325}],"pcaSample":[{"x":1.130835,"y":-1.399208,"cluster":"Clientes recientes con potencial","id":"5740"},{"x":1.810489,"y":3.70857,"cluster":"Clientes con mas devoluciones","id":"5749"},{"x":-7.0703,"y":0.51335,"cluster":"Clientes de alto valor","id":"6"},{"x":-2.083803,"y":0.052161,"cluster":"Clientes inactivos o en riesgo","id":"15"},{"x":-5.492328,"y":0.504606,"cluster":"Clientes de alto valor","id":"24"},{"x":-4.717229,"y":0.013123,"cluster":"Clientes de alto valor","id":"33"},{"x":-7.064529,"y":0.34822,"cluster":"Clientes de alto valor","id":"42"},{"x":-5.944476,"y":1.064918,"cluster":"Clientes de alto valor","id":"51"},{"x":-6.285093,"y":0.293949,"cluster":"Clientes de alto valor","id":"60"},{"x":-7.72076,"y":0.471712,"cluster":"Clientes de alto valor","id":"69"},{"x":-4.896549,"y":0.516924,"cluster":"Clientes de alto valor","id":"78"},{"x":-4.331165,"y":-0.055426,"cluster":"Clientes de alto valor","id":"87"},{"x":-7.94657,"y":1.108095,"cluster":"Clientes de alto valor","id":"96"},{"x":-7.150376,"y":0.409765,"cluster":"Clientes de alto valor","id":"105"},{"x":-6.373208,"y":0.647135,"cluster":"Clientes de alto valor","id":"114"},{"x":-7.790003,"y":0.70896,"cluster":"Clientes de alto valor","id":"123"},{"x":-6.624494,"y":-0.144635,"cluster":"Clientes de alto valor","id":"132"},{"x":-8.620071,"y":-0.358029,"cluster":"Clientes de alto valor","id":"141"},{"x":-8.494285,"y":1.065348,"cluster":"Clientes de alto valor","id":"518"},{"x":-7.94173,"y":0.834516,"cluster":"Clientes de alto valor","id":"158"},{"x":-6.447164,"y":1.477216,"cluster":"Clientes de alto valor","id":"167"},{"x":-5.857125,"y":0.280978,"cluster":"Clientes de alto valor","id":"176"},{"x":-3.90481,"y":0.303817,"cluster":"Clientes de alto valor","id":"185"},{"x":-5.051776,"y":0.598298,"cluster":"Clientes de alto valor","id":"194"},{"x":-7.521664,"y":0.626315,"cluster":"Clientes de alto valor","id":"203"},{"x":-11.164303,"y":0.742812,"cluster":"Clientes de alto valor","id":"212"},{"x":-6.052922,"y":0.468023,"cluster":"Clientes de alto valor","id":"221"},{"x":-8.820217,"y":0.430918,"cluster":"Clientes de alto valor","id":"230"},{"x":-5.717692,"y":0.362514,"cluster":"Clientes de alto valor","id":"239"},{"x":-7.692159,"y":0.794911,"cluster":"Clientes de alto valor","id":"248"},{"x":-3.779726,"y":0.093354,"cluster":"Clientes de alto valor","id":"257"},{"x":-5.176149,"y":0.29298,"cluster":"Clientes de alto valor","id":"266"},{"x":-6.955628,"y":0.648991,"cluster":"Clientes de alto valor","id":"275"},{"x":-7.389741,"y":0.722914,"cluster":"Clientes de alto valor","id":"284"},{"x":-8.201283,"y":0.040187,"cluster":"Clientes de alto valor","id":"293"},{"x":-6.671897,"y":0.568072,"cluster":"Clientes de alto valor","id":"302"},{"x":-6.750285,"y":0.242686,"cluster":"Clientes de alto valor","id":"311"},{"x":-5.918558,"y":0.275206,"cluster":"Clientes de alto valor","id":"320"},{"x":-3.988068,"y":0.321556,"cluster":"Clientes de alto valor","id":"329"},{"x":-6.900798,"y":0.70184,"cluster":"Clientes de alto valor","id":"338"},{"x":-6.194364,"y":0.798204,"cluster":"Clientes de alto valor","id":"347"},{"x":-5.990623,"y":0.782374,"cluster":"Clientes de alto valor","id":"356"},{"x":-5.300519,"y":0.758422,"cluster":"Clientes de alto valor","id":"365"},{"x":-10.633345,"y":1.048978,"cluster":"Clientes de alto valor","id":"373"},{"x":-3.708586,"y":0.304807,"cluster":"Clientes de alto valor","id":"382"},{"x":-5.553486,"y":0.45674,"cluster":"Clientes de alto valor","id":"391"},{"x":-5.540471,"y":0.136901,"cluster":"Clientes de alto valor","id":"400"},{"x":-7.149354,"y":0.693346,"cluster":"Clientes de alto valor","id":"409"},{"x":-8.598313,"y":0.786928,"cluster":"Clientes de alto valor","id":"418"},{"x":-5.146046,"y":0.086383,"cluster":"Clientes de alto valor","id":"427"},{"x":-8.653268,"y":0.814917,"cluster":"Clientes de alto valor","id":"436"},{"x":-4.911961,"y":0.231801,"cluster":"Clientes de alto valor","id":"444"},{"x":-5.406606,"y":0.281653,"cluster":"Clientes de alto valor","id":"453"},{"x":-7.583186,"y":0.90194,"cluster":"Clientes de alto valor","id":"462"},{"x":-5.85295,"y":0.249619,"cluster":"Clientes de alto valor","id":"471"},{"x":-7.140447,"y":0.185939,"cluster":"Clientes de alto valor","id":"480"},{"x":-2.421957,"y":0.157526,"cluster":"Clientes inactivos o en riesgo","id":"489"},{"x":-7.955561,"y":0.142996,"cluster":"Clientes de alto valor","id":"498"},{"x":-6.452218,"y":0.415315,"cluster":"Clientes de alto valor","id":"507"},{"x":-4.507496,"y":0.77488,"cluster":"Clientes de alto valor","id":"516"},{"x":-4.619297,"y":0.350402,"cluster":"Clientes de alto valor","id":"526"},{"x":-8.722489,"y":1.276309,"cluster":"Clientes de alto valor","id":"535"},{"x":-2.832814,"y":0.106676,"cluster":"Clientes de alto valor","id":"544"},{"x":-4.330007,"y":0.283428,"cluster":"Clientes de alto valor","id":"553"},{"x":-5.269193,"y":0.1911,"cluster":"Clientes de alto valor","id":"562"},{"x":-8.569842,"y":0.884624,"cluster":"Clientes de alto valor","id":"571"},{"x":-6.048902,"y":0.379263,"cluster":"Clientes de alto valor","id":"580"},{"x":-8.998264,"y":0.732496,"cluster":"Clientes de alto valor","id":"589"},{"x":-7.461513,"y":0.800421,"cluster":"Clientes de alto valor","id":"599"},{"x":-6.394359,"y":0.220076,"cluster":"Clientes de alto valor","id":"608"},{"x":-3.341401,"y":-0.116696,"cluster":"Clientes de alto valor","id":"617"},{"x":-6.723882,"y":1.352567,"cluster":"Clientes de alto valor","id":"626"},{"x":-5.893622,"y":0.954254,"cluster":"Clientes de alto valor","id":"635"},{"x":-6.108826,"y":0.835985,"cluster":"Clientes de alto valor","id":"644"},{"x":-5.626124,"y":0.994043,"cluster":"Clientes de alto valor","id":"653"},{"x":-7.511413,"y":0.640681,"cluster":"Clientes de alto valor","id":"662"},{"x":-7.956628,"y":1.533665,"cluster":"Clientes de alto valor","id":"671"},{"x":-8.992434,"y":1.305883,"cluster":"Clientes de alto valor","id":"680"},{"x":-6.37083,"y":0.288264,"cluster":"Clientes de alto valor","id":"689"},{"x":-6.089744,"y":0.748639,"cluster":"Clientes de alto valor","id":"698"},{"x":-4.302413,"y":0.781631,"cluster":"Clientes de alto valor","id":"707"},{"x":-6.163589,"y":0.23132,"cluster":"Clientes de alto valor","id":"716"},{"x":-8.498571,"y":0.847449,"cluster":"Clientes de alto valor","id":"725"},{"x":-7.34962,"y":0.753758,"cluster":"Clientes de alto valor","id":"734"},{"x":-8.456394,"y":0.53048,"cluster":"Clientes de alto valor","id":"743"},{"x":-0.181747,"y":-2.173204,"cluster":"Clientes recientes con potencial","id":"753"},{"x":0.7835,"y":0.25354,"cluster":"Clientes inactivos o en riesgo","id":"762"},{"x":1.261303,"y":1.207242,"cluster":"Clientes inactivos o en riesgo","id":"771"},{"x":1.059409,"y":-2.76769,"cluster":"Clientes recientes con potencial","id":"780"},{"x":1.277035,"y":-1.776909,"cluster":"Clientes recientes con potencial","id":"789"},{"x":1.485702,"y":0.575122,"cluster":"Clientes inactivos o en riesgo","id":"798"},{"x":1.394895,"y":-0.164527,"cluster":"Clientes inactivos o en riesgo","id":"807"},{"x":1.467845,"y":0.568351,"cluster":"Clientes inactivos o en riesgo","id":"816"},{"x":0.29599,"y":-1.771578,"cluster":"Clientes recientes con potencial","id":"825"},{"x":1.556378,"y":1.34468,"cluster":"Clientes inactivos o en riesgo","id":"834"},{"x":0.808389,"y":0.236518,"cluster":"Clientes inactivos o en riesgo","id":"843"},{"x":1.432051,"y":-0.170836,"cluster":"Clientes inactivos o en riesgo","id":"852"},{"x":0.329235,"y":-2.342071,"cluster":"Clientes recientes con potencial","id":"861"},{"x":0.938477,"y":-2.359028,"cluster":"Clientes recientes con potencial","id":"870"},{"x":0.879106,"y":-1.551729,"cluster":"Clientes recientes con potencial","id":"879"},{"x":1.739448,"y":0.797322,"cluster":"Clientes inactivos o en riesgo","id":"888"},{"x":1.207676,"y":0.121294,"cluster":"Clientes con mas devoluciones","id":"897"},{"x":1.625548,"y":0.013504,"cluster":"Clientes inactivos o en riesgo","id":"906"},{"x":1.702467,"y":0.798646,"cluster":"Clientes inactivos o en riesgo","id":"915"},{"x":1.28402,"y":0.372835,"cluster":"Clientes inactivos o en riesgo","id":"924"},{"x":1.246232,"y":-1.336095,"cluster":"Clientes recientes con potencial","id":"933"},{"x":0.929292,"y":-1.458869,"cluster":"Clientes recientes con potencial","id":"942"},{"x":0.72334,"y":-3.044669,"cluster":"Clientes recientes con potencial","id":"951"},{"x":1.454959,"y":-1.163544,"cluster":"Clientes recientes con potencial","id":"960"},{"x":1.323627,"y":1.11152,"cluster":"Clientes inactivos o en riesgo","id":"969"},{"x":1.177344,"y":1.784683,"cluster":"Clientes con mas devoluciones","id":"978"},{"x":0.089602,"y":-3.496336,"cluster":"Clientes recientes con potencial","id":"987"},{"x":1.323815,"y":1.184194,"cluster":"Clientes inactivos o en riesgo","id":"996"},{"x":0.98495,"y":-2.804617,"cluster":"Clientes recientes con potencial","id":"1005"},{"x":-3.578276,"y":-5.48652,"cluster":"Clientes recientes con potencial","id":"1014"},{"x":1.199849,"y":-0.376264,"cluster":"Clientes inactivos o en riesgo","id":"1023"},{"x":1.432787,"y":-1.328909,"cluster":"Clientes recientes con potencial","id":"1032"},{"x":1.511439,"y":0.61962,"cluster":"Clientes inactivos o en riesgo","id":"1041"},{"x":0.185791,"y":-3.331693,"cluster":"Clientes recientes con potencial","id":"1050"},{"x":1.440985,"y":-1.10642,"cluster":"Clientes recientes con potencial","id":"1059"},{"x":-0.099633,"y":-2.455776,"cluster":"Clientes recientes con potencial","id":"1068"},{"x":1.604035,"y":-0.077674,"cluster":"Clientes inactivos o en riesgo","id":"1077"},{"x":1.240617,"y":0.352672,"cluster":"Clientes inactivos o en riesgo","id":"1086"},{"x":0.972682,"y":-1.432707,"cluster":"Clientes recientes con potencial","id":"1095"},{"x":-1.12855,"y":-4.338765,"cluster":"Clientes recientes con potencial","id":"1104"},{"x":0.986998,"y":0.273657,"cluster":"Clientes inactivos o en riesgo","id":"1113"},{"x":0.996099,"y":0.209369,"cluster":"Clientes inactivos o en riesgo","id":"1122"},{"x":1.73921,"y":0.733679,"cluster":"Clientes inactivos o en riesgo","id":"1131"},{"x":1.091369,"y":-2.759777,"cluster":"Clientes recientes con potencial","id":"1140"},{"x":0.775767,"y":-2.551409,"cluster":"Clientes recientes con potencial","id":"1149"},{"x":0.448428,"y":0.036353,"cluster":"Clientes inactivos o en riesgo","id":"1158"},{"x":-2.759084,"y":-3.869194,"cluster":"Clientes recientes con potencial","id":"1167"},{"x":1.566229,"y":1.342113,"cluster":"Clientes inactivos o en riesgo","id":"1176"},{"x":1.566156,"y":1.276691,"cluster":"Clientes inactivos o en riesgo","id":"1185"},{"x":1.601054,"y":1.300884,"cluster":"Clientes inactivos o en riesgo","id":"1194"},{"x":1.444297,"y":-1.27148,"cluster":"Clientes recientes con potencial","id":"1203"},{"x":0.960072,"y":0.181912,"cluster":"Clientes inactivos o en riesgo","id":"1212"},{"x":1.063262,"y":0.942748,"cluster":"Clientes inactivos o en riesgo","id":"1221"},{"x":1.453111,"y":2.29339,"cluster":"Clientes con mas devoluciones","id":"1230"},{"x":1.690833,"y":3.078804,"cluster":"Clientes con mas devoluciones","id":"1239"},{"x":1.192657,"y":-2.173033,"cluster":"Clientes recientes con potencial","id":"1248"},{"x":1.113153,"y":-2.521618,"cluster":"Clientes recientes con potencial","id":"1257"},{"x":0.723314,"y":-3.040409,"cluster":"Clientes recientes con potencial","id":"1266"},{"x":0.357232,"y":0.815104,"cluster":"Clientes inactivos o en riesgo","id":"1275"},{"x":0.841686,"y":-2.327869,"cluster":"Clientes recientes con potencial","id":"1284"},{"x":1.485252,"y":0.527297,"cluster":"Clientes inactivos o en riesgo","id":"1293"},{"x":0.400289,"y":-1.419344,"cluster":"Clientes recientes con potencial","id":"1302"},{"x":0.978385,"y":0.213192,"cluster":"Clientes inactivos o en riesgo","id":"1311"},{"x":-0.597026,"y":-4.022256,"cluster":"Clientes recientes con potencial","id":"1320"},{"x":1.510776,"y":0.531643,"cluster":"Clientes inactivos o en riesgo","id":"1329"},{"x":1.817521,"y":1.494422,"cluster":"Clientes inactivos o en riesgo","id":"1338"},{"x":0.671366,"y":-0.529066,"cluster":"Clientes inactivos o en riesgo","id":"1347"},{"x":1.521608,"y":0.618489,"cluster":"Clientes inactivos o en riesgo","id":"1356"},{"x":0.916331,"y":-2.032908,"cluster":"Clientes recientes con potencial","id":"1365"},{"x":0.961321,"y":0.245395,"cluster":"Clientes inactivos o en riesgo","id":"1374"},{"x":1.662922,"y":0.015311,"cluster":"Clientes inactivos o en riesgo","id":"1383"},{"x":1.223374,"y":0.407191,"cluster":"Clientes inactivos o en riesgo","id":"1392"},{"x":1.060841,"y":1.04178,"cluster":"Clientes inactivos o en riesgo","id":"1401"},{"x":1.107916,"y":-0.344728,"cluster":"Clientes inactivos o en riesgo","id":"1410"},{"x":1.199875,"y":-0.37955,"cluster":"Clientes inactivos o en riesgo","id":"1419"},{"x":1.650878,"y":-0.018288,"cluster":"Clientes inactivos o en riesgo","id":"1428"},{"x":1.018547,"y":-1.706445,"cluster":"Clientes recientes con potencial","id":"1437"},{"x":1.467306,"y":0.518859,"cluster":"Clientes inactivos o en riesgo","id":"1446"},{"x":0.355837,"y":-3.330637,"cluster":"Clientes recientes con potencial","id":"1455"},{"x":-0.167442,"y":0.750581,"cluster":"Clientes inactivos o en riesgo","id":"1464"},{"x":1.036376,"y":1.017842,"cluster":"Clientes inactivos o en riesgo","id":"1473"},{"x":0.077732,"y":-2.405377,"cluster":"Clientes recientes con potencial","id":"1482"},{"x":0.424683,"y":-1.761148,"cluster":"Clientes recientes con potencial","id":"1492"},{"x":0.355215,"y":-3.31394,"cluster":"Clientes recientes con potencial","id":"1501"},{"x":0.84322,"y":-1.671712,"cluster":"Clientes recientes con potencial","id":"1510"},{"x":0.072838,"y":0.053245,"cluster":"Clientes inactivos o en riesgo","id":"1519"},{"x":0.34604,"y":-2.990758,"cluster":"Clientes recientes con potencial","id":"1528"},{"x":1.271294,"y":-1.745307,"cluster":"Clientes recientes con potencial","id":"1537"},{"x":0.563769,"y":-3.12116,"cluster":"Clientes recientes con potencial","id":"1546"},{"x":0.196502,"y":-3.44547,"cluster":"Clientes recientes con potencial","id":"1555"},{"x":1.091141,"y":-2.722854,"cluster":"Clientes recientes con potencial","id":"1564"},{"x":1.064766,"y":-2.771342,"cluster":"Clientes recientes con potencial","id":"1573"},{"x":0.842843,"y":0.189729,"cluster":"Clientes inactivos o en riesgo","id":"1582"},{"x":0.736058,"y":-0.521204,"cluster":"Clientes inactivos o en riesgo","id":"1591"},{"x":0.29599,"y":-1.771578,"cluster":"Clientes recientes con potencial","id":"1600"},{"x":0.781949,"y":0.195789,"cluster":"Clientes inactivos o en riesgo","id":"1609"},{"x":1.066846,"y":-0.251531,"cluster":"Clientes con mas devoluciones","id":"1618"},{"x":1.642058,"y":-0.063724,"cluster":"Clientes inactivos o en riesgo","id":"1627"},{"x":1.039668,"y":-2.567583,"cluster":"Clientes recientes con potencial","id":"1636"},{"x":0.511151,"y":-3.155307,"cluster":"Clientes recientes con potencial","id":"1645"},{"x":1.143292,"y":-0.38182,"cluster":"Clientes inactivos o en riesgo","id":"1654"},{"x":1.377994,"y":-1.235527,"cluster":"Clientes recientes con potencial","id":"1663"},{"x":0.599246,"y":-2.017456,"cluster":"Clientes recientes con potencial","id":"1672"},{"x":1.808836,"y":1.433136,"cluster":"Clientes inactivos o en riesgo","id":"1681"},{"x":0.985073,"y":-2.824498,"cluster":"Clientes recientes con potencial","id":"1690"},{"x":1.235161,"y":0.644105,"cluster":"Clientes con mas devoluciones","id":"1699"},{"x":0.965871,"y":0.954331,"cluster":"Clientes inactivos o en riesgo","id":"1708"},{"x":0.950977,"y":0.229886,"cluster":"Clientes inactivos o en riesgo","id":"1717"},{"x":0.776519,"y":-3.017278,"cluster":"Clientes recientes con potencial","id":"1726"},{"x":0.59199,"y":-1.679072,"cluster":"Clientes recientes con potencial","id":"1735"},{"x":1.242533,"y":2.269841,"cluster":"Clientes con mas devoluciones","id":"1744"},{"x":1.07554,"y":-1.603219,"cluster":"Clientes recientes con potencial","id":"1754"},{"x":1.070506,"y":0.937065,"cluster":"Clientes inactivos o en riesgo","id":"1763"},{"x":1.064626,"y":-2.74862,"cluster":"Clientes recientes con potencial","id":"1772"},{"x":1.146728,"y":-0.368086,"cluster":"Clientes con mas devoluciones","id":"1781"},{"x":1.383559,"y":-0.191859,"cluster":"Clientes inactivos o en riesgo","id":"1790"},{"x":0.616922,"y":-3.08951,"cluster":"Clientes recientes con potencial","id":"1799"},{"x":1.450522,"y":0.601735,"cluster":"Clientes inactivos o en riesgo","id":"1808"},{"x":-1.318446,"y":-2.617243,"cluster":"Clientes recientes con potencial","id":"1817"},{"x":0.951463,"y":0.255552,"cluster":"Clientes inactivos o en riesgo","id":"1826"},{"x":0.815567,"y":0.220312,"cluster":"Clientes inactivos o en riesgo","id":"1835"},{"x":0.578783,"y":-0.525654,"cluster":"Clientes inactivos o en riesgo","id":"1844"},{"x":1.653301,"y":0.003127,"cluster":"Clientes inactivos o en riesgo","id":"1853"},{"x":0.784765,"y":1.009227,"cluster":"Clientes inactivos o en riesgo","id":"1862"},{"x":1.144571,"y":-0.357996,"cluster":"Clientes inactivos o en riesgo","id":"1871"},{"x":0.801697,"y":-2.429015,"cluster":"Clientes recientes con potencial","id":"1880"},{"x":0.238907,"y":-3.401665,"cluster":"Clientes recientes con potencial","id":"1889"},{"x":0.421972,"y":-2.503714,"cluster":"Clientes recientes con potencial","id":"1898"},{"x":0.003194,"y":-2.45555,"cluster":"Clientes recientes con potencial","id":"1907"},{"x":1.071332,"y":-1.833631,"cluster":"Clientes recientes con potencial","id":"1916"},{"x":1.450842,"y":0.634538,"cluster":"Clientes inactivos o en riesgo","id":"1925"},{"x":1.566224,"y":1.3291,"cluster":"Clientes inactivos o en riesgo","id":"1934"},{"x":1.358282,"y":0.515873,"cluster":"Clientes con mas devoluciones","id":"1943"},{"x":-0.381165,"y":-2.569907,"cluster":"Clientes recientes con potencial","id":"1952"},{"x":1.618526,"y":1.295708,"cluster":"Clientes inactivos o en riesgo","id":"1961"},{"x":0.997174,"y":0.272533,"cluster":"Clientes inactivos o en riesgo","id":"1970"},{"x":1.729885,"y":0.687028,"cluster":"Clientes inactivos o en riesgo","id":"1979"},{"x":-0.051964,"y":-3.289001,"cluster":"Clientes recientes con potencial","id":"1988"},{"x":1.206386,"y":0.464816,"cluster":"Clientes inactivos o en riesgo","id":"1997"},{"x":0.195916,"y":-3.434454,"cluster":"Clientes recientes con potencial","id":"2006"},{"x":1.621531,"y":2.322236,"cluster":"Clientes con mas devoluciones","id":"2015"},{"x":1.046027,"y":0.983045,"cluster":"Clientes inactivos o en riesgo","id":"2024"},{"x":0.92579,"y":-1.471658,"cluster":"Clientes recientes con potencial","id":"2033"},{"x":1.076796,"y":-0.381281,"cluster":"Clientes inactivos o en riesgo","id":"2042"},{"x":-0.659455,"y":-4.027938,"cluster":"Clientes recientes con potencial","id":"2051"},{"x":0.817319,"y":0.274649,"cluster":"Clientes inactivos o en riesgo","id":"2060"},{"x":0.723705,"y":-2.972884,"cluster":"Clientes recientes con potencial","id":"2069"},{"x":0.082517,"y":-2.10603,"cluster":"Clientes recientes con potencial","id":"2078"},{"x":1.551452,"y":2.310699,"cluster":"Clientes con mas devoluciones","id":"2087"},{"x":0.783177,"y":0.241345,"cluster":"Clientes inactivos o en riesgo","id":"2096"},{"x":1.623688,"y":-0.054037,"cluster":"Clientes inactivos o en riesgo","id":"2105"},{"x":1.781184,"y":1.515089,"cluster":"Clientes inactivos o en riesgo","id":"2114"},{"x":1.548838,"y":1.367824,"cluster":"Clientes inactivos o en riesgo","id":"2123"},{"x":1.737509,"y":0.797233,"cluster":"Clientes inactivos o en riesgo","id":"2132"},{"x":-0.340663,"y":-3.818152,"cluster":"Clientes recientes con potencial","id":"2141"},{"x":0.620058,"y":-0.568742,"cluster":"Clientes inactivos o en riesgo","id":"2150"},{"x":1.246023,"y":-1.932662,"cluster":"Clientes recientes con potencial","id":"2159"},{"x":-0.245386,"y":-3.781383,"cluster":"Clientes recientes con potencial","id":"2168"},{"x":1.467446,"y":0.532308,"cluster":"Clientes inactivos o en riesgo","id":"2177"},{"x":1.712778,"y":0.790209,"cluster":"Clientes inactivos o en riesgo","id":"2186"},{"x":1.294716,"y":0.418174,"cluster":"Clientes inactivos o en riesgo","id":"2195"},{"x":-0.722516,"y":-2.319042,"cluster":"Clientes recientes con potencial","id":"2204"},{"x":-0.056907,"y":-3.132742,"cluster":"Clientes recientes con potencial","id":"2213"},{"x":1.432829,"y":-0.146368,"cluster":"Clientes inactivos o en riesgo","id":"2222"},{"x":-0.165892,"y":0.805675,"cluster":"Clientes inactivos o en riesgo","id":"2231"},{"x":1.018435,"y":-2.046086,"cluster":"Clientes recientes con potencial","id":"2240"},{"x":0.366126,"y":-1.825092,"cluster":"Clientes recientes con potencial","id":"2249"},{"x":0.444292,"y":-2.025327,"cluster":"Clientes recientes con potencial","id":"2258"},{"x":0.09018,"y":-3.505932,"cluster":"Clientes recientes con potencial","id":"2267"},{"x":1.261338,"y":1.220284,"cluster":"Clientes inactivos o en riesgo","id":"2276"},{"x":0.840889,"y":-2.585988,"cluster":"Clientes recientes con potencial","id":"2285"},{"x":0.35461,"y":-3.073669,"cluster":"Clientes recientes con potencial","id":"2294"},{"x":1.435928,"y":-1.131985,"cluster":"Clientes recientes con potencial","id":"2303"},{"x":1.449766,"y":0.531425,"cluster":"Clientes inactivos o en riesgo","id":"2312"},{"x":1.738858,"y":0.694972,"cluster":"Clientes inactivos o en riesgo","id":"2321"},{"x":0.238968,"y":-3.411606,"cluster":"Clientes recientes con potencial","id":"2330"},{"x":1.531391,"y":1.264059,"cluster":"Clientes inactivos o en riesgo","id":"2339"},{"x":0.116461,"y":-2.21058,"cluster":"Clientes recientes con potencial","id":"2348"},{"x":0.357847,"y":0.852013,"cluster":"Clientes inactivos o en riesgo","id":"2357"},{"x":-0.326122,"y":-3.063858,"cluster":"Clientes recientes con potencial","id":"2366"},{"x":0.883794,"y":-1.536424,"cluster":"Clientes recientes con potencial","id":"2375"},{"x":1.651633,"y":-0.05791,"cluster":"Clientes inactivos o en riesgo","id":"2384"},{"x":0.647882,"y":-0.437876,"cluster":"Clientes recientes con potencial","id":"2393"},{"x":1.521081,"y":0.546969,"cluster":"Clientes inactivos o en riesgo","id":"2402"},{"x":0.908196,"y":-1.896288,"cluster":"Clientes recientes con potencial","id":"2411"},{"x":1.086637,"y":-0.38905,"cluster":"Clientes inactivos o en riesgo","id":"2420"},{"x":1.451043,"y":-0.160942,"cluster":"Clientes inactivos o en riesgo","id":"2429"},{"x":1.085324,"y":-0.409743,"cluster":"Clientes inactivos o en riesgo","id":"2438"},{"x":1.075736,"y":-0.398415,"cluster":"Clientes inactivos o en riesgo","id":"2447"},{"x":1.271329,"y":1.168223,"cluster":"Clientes inactivos o en riesgo","id":"2456"},{"x":0.896472,"y":1.000551,"cluster":"Clientes inactivos o en riesgo","id":"2465"},{"x":1.808838,"y":1.449156,"cluster":"Clientes inactivos o en riesgo","id":"2474"},{"x":1.815747,"y":1.514648,"cluster":"Clientes inactivos o en riesgo","id":"2483"},{"x":1.35827,"y":-0.15153,"cluster":"Clientes inactivos o en riesgo","id":"2492"},{"x":1.011509,"y":-2.785952,"cluster":"Clientes recientes con potencial","id":"2501"},{"x":1.024138,"y":-2.023424,"cluster":"Clientes recientes con potencial","id":"2510"},{"x":1.148065,"y":-1.332049,"cluster":"Clientes recientes con potencial","id":"2519"},{"x":1.412717,"y":0.820049,"cluster":"Clientes con mas devoluciones","id":"2528"},{"x":1.149217,"y":-2.454624,"cluster":"Clientes recientes con potencial","id":"2537"},{"x":1.760933,"y":3.107385,"cluster":"Clientes con mas devoluciones","id":"2546"},{"x":0.784219,"y":0.282285,"cluster":"Clientes inactivos o en riesgo","id":"2555"},{"x":0.87218,"y":1.040995,"cluster":"Clientes inactivos o en riesgo","id":"2564"},{"x":1.764092,"y":1.475439,"cluster":"Clientes inactivos o en riesgo","id":"2573"},{"x":0.262274,"y":-2.373629,"cluster":"Clientes recientes con potencial","id":"2582"},{"x":1.738884,"y":0.699436,"cluster":"Clientes inactivos o en riesgo","id":"2591"},{"x":1.601073,"y":1.38513,"cluster":"Clientes inactivos o en riesgo","id":"2600"},{"x":0.249024,"y":-3.395703,"cluster":"Clientes recientes con potencial","id":"2609"},{"x":1.467424,"y":0.514385,"cluster":"Clientes inactivos o en riesgo","id":"2618"},{"x":0.563813,"y":-3.128261,"cluster":"Clientes recientes con potencial","id":"2627"},{"x":1.206545,"y":0.464821,"cluster":"Clientes inactivos o en riesgo","id":"2636"},{"x":1.432623,"y":-0.152891,"cluster":"Clientes inactivos o en riesgo","id":"2645"},{"x":1.063807,"y":1.052086,"cluster":"Clientes inactivos o en riesgo","id":"2654"},{"x":0.7605,"y":-1.695231,"cluster":"Clientes recientes con potencial","id":"2663"},{"x":0.827516,"y":-1.722345,"cluster":"Clientes recientes con potencial","id":"2672"},{"x":1.521217,"y":0.564853,"cluster":"Clientes inactivos o en riesgo","id":"2681"},{"x":0.591265,"y":-1.751466,"cluster":"Clientes recientes con potencial","id":"2690"},{"x":0.227996,"y":-2.043622,"cluster":"Clientes recientes con potencial","id":"2699"},{"x":1.357938,"y":-0.159756,"cluster":"Clientes inactivos o en riesgo","id":"2708"},{"x":1.791528,"y":1.477655,"cluster":"Clientes inactivos o en riesgo","id":"2717"},{"x":0.381459,"y":-1.872578,"cluster":"Clientes recientes con potencial","id":"2726"},{"x":0.672094,"y":-0.520464,"cluster":"Clientes inactivos o en riesgo","id":"2735"},{"x":1.791522,"y":1.511116,"cluster":"Clientes inactivos o en riesgo","id":"2744"},{"x":1.600486,"y":1.863357,"cluster":"Clientes inactivos o en riesgo","id":"2753"},{"x":1.34177,"y":-0.440211,"cluster":"Clientes inactivos o en riesgo","id":"2762"},{"x":1.372008,"y":-0.411988,"cluster":"Clientes inactivos o en riesgo","id":"2771"},{"x":1.289595,"y":1.688912,"cluster":"Clientes inactivos o en riesgo","id":"2780"},{"x":1.289758,"y":1.638466,"cluster":"Clientes inactivos o en riesgo","id":"2789"},{"x":1.488795,"y":1.51285,"cluster":"Clientes inactivos o en riesgo","id":"2798"},{"x":1.341384,"y":1.738954,"cluster":"Clientes inactivos o en riesgo","id":"2807"},{"x":0.995296,"y":0.165646,"cluster":"Clientes inactivos o en riesgo","id":"2816"},{"x":0.87729,"y":-0.749237,"cluster":"Clientes inactivos o en riesgo","id":"2825"},{"x":1.617715,"y":-0.20537,"cluster":"Clientes inactivos o en riesgo","id":"2834"},{"x":1.262148,"y":1.655101,"cluster":"Clientes inactivos o en riesgo","id":"2843"},{"x":1.605418,"y":0.504385,"cluster":"Clientes inactivos o en riesgo","id":"2852"},{"x":0.869943,"y":0.15153,"cluster":"Clientes inactivos o en riesgo","id":"2861"},{"x":1.365045,"y":-0.382098,"cluster":"Clientes inactivos o en riesgo","id":"2870"},{"x":1.565884,"y":1.884187,"cluster":"Clientes inactivos o en riesgo","id":"2879"},{"x":1.565847,"y":1.901446,"cluster":"Clientes inactivos o en riesgo","id":"2888"},{"x":1.791386,"y":1.396295,"cluster":"Clientes inactivos o en riesgo","id":"2897"},{"x":-1.825241,"y":-3.348555,"cluster":"Clientes recientes con potencial","id":"2906"},{"x":1.196154,"y":0.659699,"cluster":"Clientes con mas devoluciones","id":"2915"},{"x":0.59008,"y":-0.811113,"cluster":"Clientes inactivos o en riesgo","id":"2924"},{"x":1.12539,"y":0.178619,"cluster":"Clientes inactivos o en riesgo","id":"2933"},{"x":0.714912,"y":-0.740705,"cluster":"Clientes inactivos o en riesgo","id":"2942"},{"x":1.424744,"y":-1.18827,"cluster":"Clientes recientes con potencial","id":"2951"},{"x":1.590271,"y":1.874443,"cluster":"Clientes inactivos o en riesgo","id":"2960"},{"x":0.424429,"y":-2.048964,"cluster":"Clientes recientes con potencial","id":"2969"},{"x":0.955099,"y":-1.934965,"cluster":"Clientes recientes con potencial","id":"2978"},{"x":1.597549,"y":-0.223783,"cluster":"Clientes inactivos o en riesgo","id":"2987"},{"x":1.210494,"y":0.951762,"cluster":"Clientes inactivos o en riesgo","id":"2996"},{"x":0.790282,"y":-0.000083,"cluster":"Clientes inactivos o en riesgo","id":"3005"},{"x":1.540775,"y":1.0748,"cluster":"Clientes inactivos o en riesgo","id":"3014"},{"x":0.802256,"y":-1.802271,"cluster":"Clientes recientes con potencial","id":"3023"},{"x":1.097507,"y":0.192297,"cluster":"Clientes inactivos o en riesgo","id":"3032"},{"x":0.9491,"y":0.139019,"cluster":"Clientes inactivos o en riesgo","id":"3041"},{"x":1.520486,"y":0.475231,"cluster":"Clientes inactivos o en riesgo","id":"3050"},{"x":0.712761,"y":-0.758217,"cluster":"Clientes inactivos o en riesgo","id":"3059"},{"x":1.462518,"y":1.196478,"cluster":"Clientes con mas devoluciones","id":"3068"},{"x":0.164035,"y":-2.079736,"cluster":"Clientes recientes con potencial","id":"3077"},{"x":1.045738,"y":0.929152,"cluster":"Clientes inactivos o en riesgo","id":"3086"},{"x":0.90652,"y":0.042952,"cluster":"Clientes inactivos o en riesgo","id":"3095"},{"x":1.790576,"y":2.035324,"cluster":"Clientes inactivos o en riesgo","id":"3104"},{"x":1.161454,"y":0.189792,"cluster":"Clientes inactivos o en riesgo","id":"3113"},{"x":1.099621,"y":-1.61413,"cluster":"Clientes recientes con potencial","id":"3122"},{"x":1.047938,"y":1.508705,"cluster":"Clientes inactivos o en riesgo","id":"3131"},{"x":1.192773,"y":0.911653,"cluster":"Clientes inactivos o en riesgo","id":"3140"},{"x":1.376115,"y":1.718099,"cluster":"Clientes inactivos o en riesgo","id":"3149"},{"x":0.875176,"y":1.56309,"cluster":"Clientes inactivos o en riesgo","id":"3158"},{"x":1.704887,"y":3.546548,"cluster":"Clientes con mas devoluciones","id":"3167"},{"x":0.754161,"y":-0.728449,"cluster":"Clientes inactivos o en riesgo","id":"3176"},{"x":1.618509,"y":1.253501,"cluster":"Clientes inactivos o en riesgo","id":"3185"},{"x":0.689733,"y":-1.989918,"cluster":"Clientes recientes con potencial","id":"3194"},{"x":0.834417,"y":-0.791132,"cluster":"Clientes inactivos o en riesgo","id":"3203"},{"x":0.968584,"y":1.557527,"cluster":"Clientes inactivos o en riesgo","id":"3212"},{"x":1.047872,"y":1.469615,"cluster":"Clientes inactivos o en riesgo","id":"3221"},{"x":1.396574,"y":0.349249,"cluster":"Clientes inactivos o en riesgo","id":"3230"},{"x":1.565999,"y":1.810681,"cluster":"Clientes inactivos o en riesgo","id":"3239"},{"x":1.329329,"y":-1.479296,"cluster":"Clientes recientes con potencial","id":"3248"},{"x":1.115207,"y":-1.556091,"cluster":"Clientes recientes con potencial","id":"3257"},{"x":0.968578,"y":1.566091,"cluster":"Clientes inactivos o en riesgo","id":"3266"},{"x":1.423917,"y":-0.360763,"cluster":"Clientes inactivos o en riesgo","id":"3275"},{"x":0.985778,"y":-0.186196,"cluster":"Clientes con mas devoluciones","id":"3284"},{"x":1.271006,"y":1.092412,"cluster":"Clientes inactivos o en riesgo","id":"3293"},{"x":1.080478,"y":0.899423,"cluster":"Clientes inactivos o en riesgo","id":"3302"},{"x":0.701174,"y":0.014902,"cluster":"Clientes inactivos o en riesgo","id":"3311"},{"x":1.252823,"y":0.964736,"cluster":"Clientes inactivos o en riesgo","id":"3320"},{"x":1.287339,"y":-1.542333,"cluster":"Clientes recientes con potencial","id":"3329"},{"x":0.092566,"y":-0.965137,"cluster":"Clientes recientes con potencial","id":"3338"},{"x":1.365556,"y":1.07763,"cluster":"Clientes inactivos o en riesgo","id":"3347"},{"x":0.611129,"y":0.000626,"cluster":"Clientes inactivos o en riesgo","id":"3356"},{"x":1.696644,"y":2.830155,"cluster":"Clientes con mas devoluciones","id":"3365"},{"x":1.523289,"y":1.123581,"cluster":"Clientes inactivos o en riesgo","id":"3374"},{"x":1.131581,"y":-1.494031,"cluster":"Clientes recientes con potencial","id":"3383"},{"x":1.634936,"y":3.576663,"cluster":"Clientes con mas devoluciones","id":"3392"},{"x":1.375228,"y":0.647876,"cluster":"Clientes con mas devoluciones","id":"3401"},{"x":1.245333,"y":0.920699,"cluster":"Clientes inactivos o en riesgo","id":"3410"},{"x":1.442979,"y":-0.363764,"cluster":"Clientes inactivos o en riesgo","id":"3419"},{"x":1.062002,"y":-0.576379,"cluster":"Clientes inactivos o en riesgo","id":"3428"},{"x":1.453507,"y":1.118529,"cluster":"Clientes inactivos o en riesgo","id":"3437"},{"x":0.537009,"y":1.368985,"cluster":"Clientes inactivos o en riesgo","id":"3446"},{"x":1.262109,"y":1.639044,"cluster":"Clientes inactivos o en riesgo","id":"3455"},{"x":1.364918,"y":-0.383953,"cluster":"Clientes inactivos o en riesgo","id":"3464"},{"x":1.565941,"y":1.85251,"cluster":"Clientes inactivos o en riesgo","id":"3473"},{"x":1.192912,"y":0.9351,"cluster":"Clientes inactivos o en riesgo","id":"3482"},{"x":1.747042,"y":3.546262,"cluster":"Clientes con mas devoluciones","id":"3491"},{"x":1.369966,"y":-0.439988,"cluster":"Clientes inactivos o en riesgo","id":"3500"},{"x":-0.614745,"y":0.72479,"cluster":"Clientes inactivos o en riesgo","id":"3509"},{"x":1.42402,"y":-0.358929,"cluster":"Clientes inactivos o en riesgo","id":"3518"},{"x":1.623549,"y":0.526468,"cluster":"Clientes inactivos o en riesgo","id":"3527"},{"x":1.548597,"y":1.223728,"cluster":"Clientes inactivos o en riesgo","id":"3536"},{"x":1.523267,"y":1.095961,"cluster":"Clientes inactivos o en riesgo","id":"3545"},{"x":1.826342,"y":1.388658,"cluster":"Clientes inactivos o en riesgo","id":"3554"},{"x":0.536834,"y":1.387989,"cluster":"Clientes inactivos o en riesgo","id":"3563"},{"x":0.864745,"y":1.497496,"cluster":"Clientes inactivos o en riesgo","id":"3572"},{"x":1.616348,"y":2.114401,"cluster":"Clientes con mas devoluciones","id":"3581"},{"x":1.133027,"y":-0.540096,"cluster":"Clientes inactivos o en riesgo","id":"3590"},{"x":-0.117065,"y":-2.037308,"cluster":"Clientes recientes con potencial","id":"3599"},{"x":1.38264,"y":-0.407318,"cluster":"Clientes inactivos o en riesgo","id":"3608"},{"x":0.547207,"y":1.424498,"cluster":"Clientes inactivos o en riesgo","id":"3617"},{"x":1.488259,"y":1.084672,"cluster":"Clientes inactivos o en riesgo","id":"3626"},{"x":0.710177,"y":-0.775848,"cluster":"Clientes inactivos o en riesgo","id":"3635"},{"x":1.566019,"y":1.804986,"cluster":"Clientes inactivos o en riesgo","id":"3644"},{"x":1.826343,"y":1.395954,"cluster":"Clientes inactivos o en riesgo","id":"3653"},{"x":1.752659,"y":4.376754,"cluster":"Clientes con mas devoluciones","id":"3662"},{"x":0.817776,"y":-1.59494,"cluster":"Clientes recientes con potencial","id":"3671"},{"x":1.711802,"y":0.629335,"cluster":"Clientes inactivos o en riesgo","id":"3680"},{"x":0.388138,"y":1.344123,"cluster":"Clientes inactivos o en riesgo","id":"3689"},{"x":1.69041,"y":2.928762,"cluster":"Clientes con mas devoluciones","id":"3698"},{"x":0.446595,"y":-0.012942,"cluster":"Clientes inactivos o en riesgo","id":"3707"},{"x":1.06299,"y":0.896014,"cluster":"Clientes inactivos o en riesgo","id":"3716"},{"x":1.161339,"y":0.183661,"cluster":"Clientes inactivos o en riesgo","id":"3725"},{"x":1.129003,"y":-1.503899,"cluster":"Clientes recientes con potencial","id":"3734"},{"x":1.486462,"y":1.170767,"cluster":"Clientes con mas devoluciones","id":"3743"},{"x":1.245402,"y":0.938212,"cluster":"Clientes inactivos o en riesgo","id":"3752"},{"x":1.070673,"y":0.90933,"cluster":"Clientes inactivos o en riesgo","id":"3761"},{"x":1.747591,"y":0.659575,"cluster":"Clientes inactivos o en riesgo","id":"3770"},{"x":1.433658,"y":1.01662,"cluster":"Clientes con mas devoluciones","id":"3779"},{"x":0.879884,"y":-1.595378,"cluster":"Clientes recientes con potencial","id":"3788"},{"x":0.577215,"y":-1.793006,"cluster":"Clientes recientes con potencial","id":"3797"},{"x":1.520706,"y":0.500644,"cluster":"Clientes inactivos o en riesgo","id":"3806"},{"x":0.707093,"y":-0.801789,"cluster":"Clientes inactivos o en riesgo","id":"3815"},{"x":1.062059,"y":1.589627,"cluster":"Clientes inactivos o en riesgo","id":"3824"},{"x":1.192824,"y":0.923282,"cluster":"Clientes inactivos o en riesgo","id":"3833"},{"x":0.994977,"y":0.149016,"cluster":"Clientes inactivos o en riesgo","id":"3842"},{"x":1.767051,"y":4.270722,"cluster":"Clientes con mas devoluciones","id":"3851"},{"x":1.323566,"y":1.094014,"cluster":"Clientes inactivos o en riesgo","id":"3860"},{"x":1.29794,"y":0.95596,"cluster":"Clientes inactivos o en riesgo","id":"3869"},{"x":1.306871,"y":1.744156,"cluster":"Clientes inactivos o en riesgo","id":"3878"},{"x":0.06656,"y":-2.187736,"cluster":"Clientes recientes con potencial","id":"3887"},{"x":1.538515,"y":0.492625,"cluster":"Clientes inactivos o en riesgo","id":"3896"},{"x":1.252629,"y":0.916493,"cluster":"Clientes inactivos o en riesgo","id":"3905"},{"x":1.343637,"y":-0.415722,"cluster":"Clientes inactivos o en riesgo","id":"3914"},{"x":1.473256,"y":0.474452,"cluster":"Clientes inactivos o en riesgo","id":"3923"},{"x":1.80888,"y":1.417311,"cluster":"Clientes inactivos o en riesgo","id":"3932"},{"x":0.33958,"y":-1.806228,"cluster":"Clientes recientes con potencial","id":"3941"},{"x":0.524237,"y":-1.882041,"cluster":"Clientes recientes con potencial","id":"3950"},{"x":0.07104,"y":-2.54421,"cluster":"Clientes recientes con potencial","id":"3959"},{"x":0.197257,"y":-1.090018,"cluster":"Clientes recientes con potencial","id":"3968"},{"x":0.736595,"y":-1.733558,"cluster":"Clientes recientes con potencial","id":"3977"},{"x":0.238109,"y":-2.434524,"cluster":"Clientes recientes con potencial","id":"3986"},{"x":0.804742,"y":-1.713112,"cluster":"Clientes recientes con potencial","id":"3995"},{"x":1.148111,"y":-0.591849,"cluster":"Clientes inactivos o en riesgo","id":"4004"},{"x":1.182608,"y":0.917073,"cluster":"Clientes inactivos o en riesgo","id":"4013"},{"x":1.186533,"y":0.330281,"cluster":"Clientes inactivos o en riesgo","id":"4022"},{"x":1.140778,"y":0.869964,"cluster":"Clientes con mas devoluciones","id":"4031"},{"x":-1.242413,"y":-3.161822,"cluster":"Clientes recientes con potencial","id":"4040"},{"x":0.018192,"y":1.340942,"cluster":"Clientes inactivos o en riesgo","id":"4049"},{"x":1.128943,"y":-0.590376,"cluster":"Clientes inactivos o en riesgo","id":"4058"},{"x":0.825522,"y":0.886989,"cluster":"Clientes inactivos o en riesgo","id":"4067"},{"x":1.466321,"y":-1.103506,"cluster":"Clientes recientes con potencial","id":"4076"},{"x":0.790282,"y":-0.000083,"cluster":"Clientes inactivos o en riesgo","id":"4085"},{"x":1.466659,"y":0.463243,"cluster":"Clientes inactivos o en riesgo","id":"4094"},{"x":1.047937,"y":1.510132,"cluster":"Clientes inactivos o en riesgo","id":"4103"},{"x":0.101255,"y":0.562167,"cluster":"Clientes inactivos o en riesgo","id":"4112"},{"x":0.864671,"y":1.475847,"cluster":"Clientes inactivos o en riesgo","id":"4121"},{"x":1.614788,"y":-0.259761,"cluster":"Clientes inactivos o en riesgo","id":"4130"},{"x":0.90235,"y":-0.049707,"cluster":"Clientes con mas devoluciones","id":"4139"},{"x":1.245222,"y":0.900135,"cluster":"Clientes inactivos o en riesgo","id":"4148"},{"x":1.210369,"y":0.929756,"cluster":"Clientes inactivos o en riesgo","id":"4157"},{"x":0.642061,"y":-0.790287,"cluster":"Clientes inactivos o en riesgo","id":"4166"},{"x":0.743867,"y":-0.742917,"cluster":"Clientes inactivos o en riesgo","id":"4175"},{"x":0.783374,"y":0.893064,"cluster":"Clientes inactivos o en riesgo","id":"4184"},{"x":1.324327,"y":1.63046,"cluster":"Clientes inactivos o en riesgo","id":"4193"},{"x":1.636752,"y":-0.206512,"cluster":"Clientes inactivos o en riesgo","id":"4202"},{"x":1.54638,"y":2.114314,"cluster":"Clientes con mas devoluciones","id":"4211"},{"x":1.807778,"y":1.99958,"cluster":"Clientes inactivos o en riesgo","id":"4220"},{"x":1.128272,"y":-0.599992,"cluster":"Clientes inactivos o en riesgo","id":"4229"},{"x":1.822826,"y":4.305267,"cluster":"Clientes con mas devoluciones","id":"4238"},{"x":0.63327,"y":-0.777893,"cluster":"Clientes inactivos o en riesgo","id":"4247"},{"x":0.710789,"y":-0.773823,"cluster":"Clientes inactivos o en riesgo","id":"4256"},{"x":0.186373,"y":-0.910132,"cluster":"Clientes recientes con potencial","id":"4265"},{"x":0.899409,"y":1.528609,"cluster":"Clientes inactivos o en riesgo","id":"4274"},{"x":1.204259,"y":0.322183,"cluster":"Clientes inactivos o en riesgo","id":"4283"},{"x":1.442423,"y":-0.374551,"cluster":"Clientes inactivos o en riesgo","id":"4292"},{"x":1.739921,"y":1.266363,"cluster":"Clientes inactivos o en riesgo","id":"4301"},{"x":1.376045,"y":1.630126,"cluster":"Clientes inactivos o en riesgo","id":"4310"},{"x":0.836241,"y":-0.773478,"cluster":"Clientes inactivos o en riesgo","id":"4319"},{"x":0.958045,"y":0.885384,"cluster":"Clientes inactivos o en riesgo","id":"4328"},{"x":1.298029,"y":0.932583,"cluster":"Clientes inactivos o en riesgo","id":"4337"},{"x":1.634947,"y":3.581112,"cluster":"Clientes con mas devoluciones","id":"4346"},{"x":1.438505,"y":-1.119003,"cluster":"Clientes recientes con potencial","id":"4355"},{"x":0.988145,"y":-0.722535,"cluster":"Clientes inactivos o en riesgo","id":"4364"},{"x":1.297985,"y":0.912237,"cluster":"Clientes inactivos o en riesgo","id":"4373"},{"x":1.814768,"y":1.978218,"cluster":"Clientes inactivos o en riesgo","id":"4382"},{"x":1.641999,"y":-0.25986,"cluster":"Clientes inactivos o en riesgo","id":"4391"},{"x":1.601531,"y":2.089419,"cluster":"Clientes con mas devoluciones","id":"4400"},{"x":0.444003,"y":-2.025454,"cluster":"Clientes recientes con potencial","id":"4409"},{"x":1.227982,"y":0.953743,"cluster":"Clientes inactivos o en riesgo","id":"4418"},{"x":1.816379,"y":2.061609,"cluster":"Clientes inactivos o en riesgo","id":"4427"},{"x":0.99239,"y":0.787028,"cluster":"Clientes inactivos o en riesgo","id":"4436"},{"x":1.600387,"y":1.900708,"cluster":"Clientes inactivos o en riesgo","id":"4445"},{"x":1.617781,"y":1.850717,"cluster":"Clientes inactivos o en riesgo","id":"4454"},{"x":1.523249,"y":1.090077,"cluster":"Clientes inactivos o en riesgo","id":"4463"},{"x":1.520486,"y":0.475231,"cluster":"Clientes inactivos o en riesgo","id":"4472"},{"x":1.660641,"y":0.529835,"cluster":"Clientes inactivos o en riesgo","id":"4481"},{"x":0.195649,"y":-1.098643,"cluster":"Clientes recientes con potencial","id":"4490"},{"x":1.211057,"y":-0.075032,"cluster":"Clientes con mas devoluciones","id":"4499"},{"x":1.159064,"y":1.21928,"cluster":"Clientes con mas devoluciones","id":"4508"},{"x":0.540496,"y":-1.762337,"cluster":"Clientes recientes con potencial","id":"4517"},{"x":1.790575,"y":2.036751,"cluster":"Clientes inactivos o en riesgo","id":"4526"},{"x":1.540771,"y":1.106681,"cluster":"Clientes inactivos o en riesgo","id":"4535"},{"x":0.94892,"y":0.145162,"cluster":"Clientes inactivos o en riesgo","id":"4544"},{"x":0.87485,"y":1.48044,"cluster":"Clientes inactivos o en riesgo","id":"4553"},{"x":-0.617151,"y":-2.951995,"cluster":"Clientes recientes con potencial","id":"4562"},{"x":0.967371,"y":0.734957,"cluster":"Clientes inactivos o en riesgo","id":"4571"},{"x":1.076396,"y":-1.507266,"cluster":"Clientes recientes con potencial","id":"4580"},{"x":0.871042,"y":0.922217,"cluster":"Clientes inactivos o en riesgo","id":"4589"},{"x":0.072529,"y":-1.947826,"cluster":"Clientes recientes con potencial","id":"4598"},{"x":0.963902,"y":1.933976,"cluster":"Clientes inactivos o en riesgo","id":"4607"},{"x":1.780349,"y":1.990223,"cluster":"Clientes inactivos o en riesgo","id":"4616"},{"x":1.790662,"y":1.996379,"cluster":"Clientes inactivos o en riesgo","id":"4625"},{"x":0.296421,"y":-0.945997,"cluster":"Clientes recientes con potencial","id":"4634"},{"x":1.520375,"y":0.464666,"cluster":"Clientes inactivos o en riesgo","id":"4643"},{"x":0.992438,"y":0.792941,"cluster":"Clientes inactivos o en riesgo","id":"4652"},{"x":1.260414,"y":-1.268876,"cluster":"Clientes recientes con potencial","id":"4661"},{"x":1.109185,"y":-1.578644,"cluster":"Clientes recientes con potencial","id":"4670"},{"x":1.604187,"y":1.847521,"cluster":"Clientes inactivos o en riesgo","id":"4679"},{"x":1.682708,"y":4.348929,"cluster":"Clientes con mas devoluciones","id":"4688"},{"x":1.634263,"y":-0.259051,"cluster":"Clientes inactivos o en riesgo","id":"4697"},{"x":1.288355,"y":1.070946,"cluster":"Clientes inactivos o en riesgo","id":"4706"},{"x":0.968452,"y":1.498222,"cluster":"Clientes inactivos o en riesgo","id":"4715"},{"x":1.227943,"y":0.946411,"cluster":"Clientes inactivos o en riesgo","id":"4724"},{"x":1.641741,"y":-0.265312,"cluster":"Clientes inactivos o en riesgo","id":"4733"},{"x":1.528911,"y":3.487823,"cluster":"Clientes con mas devoluciones","id":"4742"},{"x":1.179392,"y":0.190773,"cluster":"Clientes inactivos o en riesgo","id":"4751"},{"x":1.633797,"y":0.513378,"cluster":"Clientes inactivos o en riesgo","id":"4760"},{"x":1.660623,"y":0.523951,"cluster":"Clientes inactivos o en riesgo","id":"4769"},{"x":1.65882,"y":0.525272,"cluster":"Clientes inactivos o en riesgo","id":"4778"},{"x":0.279543,"y":-0.982796,"cluster":"Clientes recientes con potencial","id":"4787"},{"x":1.119387,"y":-1.501107,"cluster":"Clientes recientes con potencial","id":"4796"},{"x":1.736824,"y":0.650105,"cluster":"Clientes inactivos o en riesgo","id":"4805"},{"x":0.842509,"y":0.03953,"cluster":"Clientes inactivos o en riesgo","id":"4814"},{"x":-0.432573,"y":0.592692,"cluster":"Clientes inactivos o en riesgo","id":"4823"},{"x":1.450471,"y":1.208956,"cluster":"Clientes con mas devoluciones","id":"4832"},{"x":1.636014,"y":-0.222679,"cluster":"Clientes inactivos o en riesgo","id":"4841"},{"x":1.790548,"y":2.033715,"cluster":"Clientes inactivos o en riesgo","id":"4850"},{"x":1.239887,"y":0.304426,"cluster":"Clientes inactivos o en riesgo","id":"4859"},{"x":0.870662,"y":0.88696,"cluster":"Clientes inactivos o en riesgo","id":"4868"},{"x":1.42402,"y":-0.358929,"cluster":"Clientes inactivos o en riesgo","id":"4877"},{"x":1.002357,"y":0.755095,"cluster":"Clientes inactivos o en riesgo","id":"4886"},{"x":1.47074,"y":1.073937,"cluster":"Clientes inactivos o en riesgo","id":"4895"},{"x":1.525202,"y":2.51749,"cluster":"Clientes con mas devoluciones","id":"4904"},{"x":0.539105,"y":-0.835894,"cluster":"Clientes inactivos o en riesgo","id":"4913"},{"x":1.383935,"y":-0.387151,"cluster":"Clientes inactivos o en riesgo","id":"4922"},{"x":1.470802,"y":1.09874,"cluster":"Clientes inactivos o en riesgo","id":"4931"},{"x":0.545802,"y":-0.794506,"cluster":"Clientes inactivos o en riesgo","id":"4940"},{"x":1.548834,"y":1.849315,"cluster":"Clientes inactivos o en riesgo","id":"4949"},{"x":1.554719,"y":1.847665,"cluster":"Clientes inactivos o en riesgo","id":"4958"},{"x":0.881602,"y":-1.543929,"cluster":"Clientes recientes con potencial","id":"4967"},{"x":0.285538,"y":-1.00857,"cluster":"Clientes recientes con potencial","id":"4976"},{"x":-0.502931,"y":-1.085624,"cluster":"Clientes recientes con potencial","id":"4985"},{"x":0.976676,"y":0.129781,"cluster":"Clientes inactivos o en riesgo","id":"4994"},{"x":1.548804,"y":1.866581,"cluster":"Clientes inactivos o en riesgo","id":"5003"},{"x":0.761495,"y":1.586687,"cluster":"Clientes inactivos o en riesgo","id":"5012"},{"x":1.222086,"y":0.320048,"cluster":"Clientes inactivos o en riesgo","id":"5021"},{"x":1.647195,"y":-0.19119,"cluster":"Clientes inactivos o en riesgo","id":"5030"},{"x":1.314235,"y":-1.604918,"cluster":"Clientes recientes con potencial","id":"5039"},{"x":0.269025,"y":-1.83691,"cluster":"Clientes recientes con potencial","id":"5048"},{"x":1.227663,"y":0.892219,"cluster":"Clientes inactivos o en riesgo","id":"5057"},{"x":0.632737,"y":2.14276,"cluster":"Clientes con mas devoluciones","id":"5066"},{"x":1.618528,"y":1.249233,"cluster":"Clientes inactivos o en riesgo","id":"5075"},{"x":1.748684,"y":1.271096,"cluster":"Clientes inactivos o en riesgo","id":"5084"},{"x":1.633851,"y":0.520878,"cluster":"Clientes inactivos o en riesgo","id":"5093"},{"x":1.335136,"y":-1.520973,"cluster":"Clientes recientes con potencial","id":"5102"},{"x":0.018785,"y":1.386248,"cluster":"Clientes inactivos o en riesgo","id":"5111"},{"x":-0.562686,"y":-2.848856,"cluster":"Clientes recientes con potencial","id":"5120"},{"x":0.296421,"y":-0.945997,"cluster":"Clientes recientes con potencial","id":"5129"},{"x":1.488163,"y":1.046675,"cluster":"Clientes inactivos o en riesgo","id":"5138"},{"x":1.341124,"y":-0.526866,"cluster":"Clientes inactivos o en riesgo","id":"5147"},{"x":1.586396,"y":-0.235896,"cluster":"Clientes inactivos o en riesgo","id":"5156"},{"x":1.146697,"y":-0.608812,"cluster":"Clientes inactivos o en riesgo","id":"5165"},{"x":1.204997,"y":0.190605,"cluster":"Clientes inactivos o en riesgo","id":"5174"},{"x":1.565894,"y":1.872616,"cluster":"Clientes inactivos o en riesgo","id":"5183"},{"x":1.814837,"y":1.950837,"cluster":"Clientes inactivos o en riesgo","id":"5192"},{"x":1.780062,"y":2.929756,"cluster":"Clientes con mas devoluciones","id":"5201"},{"x":1.406546,"y":0.355827,"cluster":"Clientes inactivos o en riesgo","id":"5210"},{"x":0.866377,"y":-0.754174,"cluster":"Clientes inactivos o en riesgo","id":"5219"},{"x":1.420145,"y":-0.426364,"cluster":"Clientes inactivos o en riesgo","id":"5228"},{"x":1.062942,"y":0.890101,"cluster":"Clientes inactivos o en riesgo","id":"5237"},{"x":0.303537,"y":-2.07032,"cluster":"Clientes recientes con potencial","id":"5246"},{"x":0.640164,"y":-2.139881,"cluster":"Clientes recientes con potencial","id":"5255"},{"x":1.085335,"y":1.192819,"cluster":"Clientes con mas devoluciones","id":"5264"},{"x":0.788909,"y":1.577307,"cluster":"Clientes inactivos o en riesgo","id":"5273"},{"x":1.634858,"y":3.556401,"cluster":"Clientes con mas devoluciones","id":"5282"},{"x":-0.698963,"y":-2.297869,"cluster":"Clientes recientes con potencial","id":"5291"},{"x":1.566047,"y":1.789147,"cluster":"Clientes inactivos o en riesgo","id":"5300"},{"x":0.875176,"y":1.56309,"cluster":"Clientes inactivos o en riesgo","id":"5309"},{"x":1.713661,"y":1.242192,"cluster":"Clientes inactivos o en riesgo","id":"5318"},{"x":1.474087,"y":2.048267,"cluster":"Clientes con mas devoluciones","id":"5327"},{"x":1.729668,"y":0.651159,"cluster":"Clientes inactivos o en riesgo","id":"5336"},{"x":1.633764,"y":0.50748,"cluster":"Clientes inactivos o en riesgo","id":"5345"},{"x":1.171437,"y":-1.336576,"cluster":"Clientes recientes con potencial","id":"5354"},{"x":0.788468,"y":1.485978,"cluster":"Clientes inactivos o en riesgo","id":"5363"},{"x":1.057618,"y":-0.699709,"cluster":"Clientes inactivos o en riesgo","id":"5372"},{"x":1.021949,"y":-0.59634,"cluster":"Clientes inactivos o en riesgo","id":"5381"},{"x":1.655677,"y":-0.214849,"cluster":"Clientes inactivos o en riesgo","id":"5390"},{"x":1.36046,"y":-0.529759,"cluster":"Clientes inactivos o en riesgo","id":"5399"},{"x":1.614306,"y":-0.268896,"cluster":"Clientes inactivos o en riesgo","id":"5408"},{"x":1.324302,"y":1.652015,"cluster":"Clientes inactivos o en riesgo","id":"5417"},{"x":0.983835,"y":-1.732804,"cluster":"Clientes recientes con potencial","id":"5426"},{"x":1.63386,"y":0.518031,"cluster":"Clientes inactivos o en riesgo","id":"5435"},{"x":1.71174,"y":0.623255,"cluster":"Clientes inactivos o en riesgo","id":"5444"},{"x":1.746909,"y":3.553548,"cluster":"Clientes con mas devoluciones","id":"5453"},{"x":1.442448,"y":0.362253,"cluster":"Clientes inactivos o en riesgo","id":"5462"},{"x":1.816194,"y":2.074588,"cluster":"Clientes inactivos o en riesgo","id":"5471"},{"x":0.646026,"y":-2.121524,"cluster":"Clientes recientes con potencial","id":"5480"},{"x":0.859381,"y":-0.719402,"cluster":"Clientes inactivos o en riesgo","id":"5489"},{"x":1.381135,"y":-0.429575,"cluster":"Clientes inactivos o en riesgo","id":"5498"},{"x":0.536877,"y":1.344423,"cluster":"Clientes inactivos o en riesgo","id":"5507"},{"x":1.047756,"y":1.499954,"cluster":"Clientes inactivos o en riesgo","id":"5516"},{"x":0.591927,"y":-0.798943,"cluster":"Clientes inactivos o en riesgo","id":"5525"},{"x":1.641604,"y":2.03822,"cluster":"Clientes con mas devoluciones","id":"5534"},{"x":1.664057,"y":3.305565,"cluster":"Clientes con mas devoluciones","id":"5543"},{"x":1.383853,"y":-0.38881,"cluster":"Clientes inactivos o en riesgo","id":"5552"},{"x":0.690658,"y":0.129921,"cluster":"Clientes inactivos o en riesgo","id":"5561"},{"x":0.866182,"y":-0.756095,"cluster":"Clientes inactivos o en riesgo","id":"5570"},{"x":0.984669,"y":0.729608,"cluster":"Clientes inactivos o en riesgo","id":"5579"},{"x":1.385825,"y":-0.356312,"cluster":"Clientes inactivos o en riesgo","id":"5588"},{"x":1.521479,"y":1.17171,"cluster":"Clientes con mas devoluciones","id":"5597"},{"x":1.41735,"y":-1.102904,"cluster":"Clientes recientes con potencial","id":"5606"},{"x":1.366422,"y":-0.360423,"cluster":"Clientes inactivos o en riesgo","id":"5615"},{"x":0.70059,"y":-0.002134,"cluster":"Clientes inactivos o en riesgo","id":"5624"},{"x":0.288233,"y":-0.993704,"cluster":"Clientes recientes con potencial","id":"5633"},{"x":1.790549,"y":2.041011,"cluster":"Clientes inactivos o en riesgo","id":"5642"},{"x":1.478044,"y":1.059588,"cluster":"Clientes inactivos o en riesgo","id":"5651"},{"x":1.614355,"y":-0.270885,"cluster":"Clientes inactivos o en riesgo","id":"5660"},{"x":0.8459,"y":-1.662214,"cluster":"Clientes recientes con potencial","id":"5669"},{"x":1.203898,"y":0.293326,"cluster":"Clientes inactivos o en riesgo","id":"5678"},{"x":1.109425,"y":-0.592863,"cluster":"Clientes inactivos o en riesgo","id":"5687"},{"x":0.531079,"y":0.755432,"cluster":"Clientes inactivos o en riesgo","id":"5696"},{"x":1.239765,"y":0.296861,"cluster":"Clientes inactivos o en riesgo","id":"5705"},{"x":1.634086,"y":-0.262691,"cluster":"Clientes inactivos o en riesgo","id":"5714"},{"x":0.534647,"y":-2.167033,"cluster":"Clientes recientes con potencial","id":"5723"},{"x":1.586797,"y":-0.228573,"cluster":"Clientes inactivos o en riesgo","id":"5732"}]};
window.__RECS__ = [{"product_name":"Cinta kinesiologica","recommended_product_name":"Mascarilla facial purificante","confidence":0.1659,"lift":1.3921,"support":0.0114,"baskets_together":286,"recommendation_rank":1},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Oximetro de pulso","confidence":0.3757,"lift":1.3891,"support":0.0219,"baskets_together":86,"recommendation_rank":2},{"product_name":"Bascula digital corporal","recommended_product_name":"Proteina whey vainilla","confidence":0.0584,"lift":1.3874,"support":0.0253,"baskets_together":280,"recommendation_rank":3},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Magnesio bisglicinato","confidence":0.0963,"lift":1.387,"support":0.0251,"baskets_together":59,"recommendation_rank":4},{"product_name":"Pasta dental sensitive","recommended_product_name":"Hilo dental cera","confidence":0.2365,"lift":1.3861,"support":0.0258,"baskets_together":213,"recommendation_rank":5},{"product_name":"Te verde antioxidante","recommended_product_name":"Tensiometro de brazo","confidence":0.1713,"lift":1.3845,"support":0.0169,"baskets_together":130,"recommendation_rank":6},{"product_name":"Crema corporal hidratante","recommended_product_name":"Vitamina D3","confidence":0.1862,"lift":1.3835,"support":0.0099,"baskets_together":27,"recommendation_rank":7},{"product_name":"Antifaz dormir seda","recommended_product_name":"Proteina whey vainilla","confidence":0.3072,"lift":1.3823,"support":0.0151,"baskets_together":141,"recommendation_rank":8},{"product_name":"Vendas elasticas pack","recommended_product_name":"Botiquin primeros auxilios","confidence":0.1766,"lift":1.3819,"support":0.0239,"baskets_together":276,"recommendation_rank":9},{"product_name":"Tensiometro de brazo","recommended_product_name":"Mascarilla facial purificante","confidence":0.3553,"lift":1.3815,"support":0.0157,"baskets_together":233,"recommendation_rank":10},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Difusor aromaterapia","confidence":0.48,"lift":1.3809,"support":0.007,"baskets_together":186,"recommendation_rank":11},{"product_name":"Locion corporal aloe","recommended_product_name":"Multivitaminico diario","confidence":0.4318,"lift":1.3788,"support":0.0049,"baskets_together":72,"recommendation_rank":12},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Banda elastica resistencia","confidence":0.4313,"lift":1.378,"support":0.0136,"baskets_together":48,"recommendation_rank":13},{"product_name":"Multivitaminico diario","recommended_product_name":"Aceite esencial lavanda","confidence":0.1466,"lift":1.3756,"support":0.0081,"baskets_together":133,"recommendation_rank":14},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Crema corporal hidratante","confidence":0.1937,"lift":1.3731,"support":0.026,"baskets_together":178,"recommendation_rank":15},{"product_name":"Proteina whey vainilla","recommended_product_name":"Banda elastica resistencia","confidence":0.2408,"lift":1.3706,"support":0.0189,"baskets_together":223,"recommendation_rank":16},{"product_name":"Miel pura bio","recommended_product_name":"Difusor aromaterapia","confidence":0.1172,"lift":1.3702,"support":0.0087,"baskets_together":294,"recommendation_rank":17},{"product_name":"Aceite esencial lavanda","recommended_product_name":"Botiquin primeros auxilios","confidence":0.29,"lift":1.3659,"support":0.024,"baskets_together":37,"recommendation_rank":18},{"product_name":"Crema corporal hidratante","recommended_product_name":"Repelente mosquitos plantas","confidence":0.1985,"lift":1.3612,"support":0.012,"baskets_together":234,"recommendation_rank":19},{"product_name":"Difusor aromaterapia","recommended_product_name":"Miel pura bio","confidence":0.2873,"lift":1.3559,"support":0.0143,"baskets_together":155,"recommendation_rank":20},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Aceite esencial lavanda","confidence":0.4906,"lift":1.3504,"support":0.007,"baskets_together":277,"recommendation_rank":21},{"product_name":"Multivitaminico diario","recommended_product_name":"Vendas elasticas pack","confidence":0.2921,"lift":1.3497,"support":0.0034,"baskets_together":255,"recommendation_rank":22},{"product_name":"Termometro digital","recommended_product_name":"Crema corporal hidratante","confidence":0.1594,"lift":1.3486,"support":0.0234,"baskets_together":38,"recommendation_rank":23},{"product_name":"Banda elastica resistencia","recommended_product_name":"Bascula digital corporal","confidence":0.1097,"lift":1.3468,"support":0.0239,"baskets_together":156,"recommendation_rank":24},{"product_name":"Tensiometro de brazo","recommended_product_name":"Barra proteica cacao","confidence":0.4473,"lift":1.3449,"support":0.0206,"baskets_together":285,"recommendation_rank":25},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Repelente mosquitos plantas","confidence":0.0679,"lift":1.3411,"support":0.0099,"baskets_together":212,"recommendation_rank":26},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Crema corporal hidratante","confidence":0.1642,"lift":1.3395,"support":0.011,"baskets_together":116,"recommendation_rank":27},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Crema solar SPF50","confidence":0.4623,"lift":1.3354,"support":0.009,"baskets_together":116,"recommendation_rank":28},{"product_name":"Locion corporal aloe","recommended_product_name":"Vendas elasticas pack","confidence":0.2242,"lift":1.3325,"support":0.0067,"baskets_together":245,"recommendation_rank":29},{"product_name":"Hilo dental cera","recommended_product_name":"Banda elastica resistencia","confidence":0.123,"lift":1.3319,"support":0.0118,"baskets_together":174,"recommendation_rank":30},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Oximetro de pulso","confidence":0.4371,"lift":1.3285,"support":0.0104,"baskets_together":118,"recommendation_rank":31},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Termometro digital","confidence":0.1348,"lift":1.3284,"support":0.0084,"baskets_together":233,"recommendation_rank":32},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Pasta dental sensitive","confidence":0.1407,"lift":1.3267,"support":0.0068,"baskets_together":122,"recommendation_rank":33},{"product_name":"Oximetro de pulso","recommended_product_name":"Bascula digital corporal","confidence":0.4703,"lift":1.3259,"support":0.0164,"baskets_together":290,"recommendation_rank":34},{"product_name":"Oximetro de pulso","recommended_product_name":"Magnesio bisglicinato","confidence":0.1257,"lift":1.325,"support":0.0122,"baskets_together":202,"recommendation_rank":35},{"product_name":"Bascula digital corporal","recommended_product_name":"Rodillo masaje muscular","confidence":0.2043,"lift":1.3229,"support":0.0151,"baskets_together":113,"recommendation_rank":36},{"product_name":"Proteina whey vainilla","recommended_product_name":"Termometro digital","confidence":0.4371,"lift":1.32,"support":0.0058,"baskets_together":51,"recommendation_rank":37},{"product_name":"Bascula digital corporal","recommended_product_name":"Oximetro de pulso","confidence":0.3306,"lift":1.3192,"support":0.0023,"baskets_together":92,"recommendation_rank":38},{"product_name":"Vitamina D3","recommended_product_name":"Cinta kinesiologica","confidence":0.4863,"lift":1.3181,"support":0.0124,"baskets_together":168,"recommendation_rank":39},{"product_name":"Hilo dental cera","recommended_product_name":"Difusor aromaterapia","confidence":0.4804,"lift":1.317,"support":0.0125,"baskets_together":256,"recommendation_rank":40},{"product_name":"Cepillo dental electrico","recommended_product_name":"Infusion manzanilla noche","confidence":0.3328,"lift":1.3142,"support":0.0129,"baskets_together":119,"recommendation_rank":41},{"product_name":"Oximetro de pulso","recommended_product_name":"Almohada cervical viscoelastica","confidence":0.4269,"lift":1.312,"support":0.0253,"baskets_together":231,"recommendation_rank":42},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Magnesio bisglicinato","confidence":0.3397,"lift":1.3114,"support":0.0174,"baskets_together":33,"recommendation_rank":43},{"product_name":"Barra proteica cacao","recommended_product_name":"Termometro digital","confidence":0.0561,"lift":1.3052,"support":0.0165,"baskets_together":121,"recommendation_rank":44},{"product_name":"Proteina whey vainilla","recommended_product_name":"Tensiometro de brazo","confidence":0.4392,"lift":1.3038,"support":0.0102,"baskets_together":269,"recommendation_rank":45},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Magnesio bisglicinato","confidence":0.2348,"lift":1.302,"support":0.0067,"baskets_together":55,"recommendation_rank":46},{"product_name":"Multivitaminico diario","recommended_product_name":"Termometro digital","confidence":0.4499,"lift":1.3014,"support":0.0257,"baskets_together":23,"recommendation_rank":47},{"product_name":"Pulsometro deportivo","recommended_product_name":"Difusor aromaterapia","confidence":0.2551,"lift":1.3011,"support":0.0083,"baskets_together":121,"recommendation_rank":48},{"product_name":"Locion corporal aloe","recommended_product_name":"Difusor aromaterapia","confidence":0.2568,"lift":1.3009,"support":0.0057,"baskets_together":170,"recommendation_rank":49},{"product_name":"Bascula digital corporal","recommended_product_name":"Vitamina D3","confidence":0.3536,"lift":1.3002,"support":0.0231,"baskets_together":97,"recommendation_rank":50},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Cinta kinesiologica","confidence":0.0903,"lift":1.2987,"support":0.0269,"baskets_together":295,"recommendation_rank":51},{"product_name":"Termometro digital","recommended_product_name":"Cinta kinesiologica","confidence":0.3557,"lift":1.2981,"support":0.0103,"baskets_together":146,"recommendation_rank":52},{"product_name":"Cinta kinesiologica","recommended_product_name":"Bebida isotonica citrico","confidence":0.0705,"lift":1.2976,"support":0.0151,"baskets_together":230,"recommendation_rank":53},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Te verde antioxidante","confidence":0.452,"lift":1.2965,"support":0.0114,"baskets_together":50,"recommendation_rank":54},{"product_name":"Vendas elasticas pack","recommended_product_name":"Infusion manzanilla noche","confidence":0.0604,"lift":1.2924,"support":0.0112,"baskets_together":153,"recommendation_rank":55},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Crema solar SPF50","confidence":0.1952,"lift":1.2885,"support":0.0267,"baskets_together":117,"recommendation_rank":56},{"product_name":"Pasta dental sensitive","recommended_product_name":"Banda elastica resistencia","confidence":0.2878,"lift":1.2809,"support":0.0136,"baskets_together":136,"recommendation_rank":57},{"product_name":"Difusor aromaterapia","recommended_product_name":"Termometro digital","confidence":0.246,"lift":1.2808,"support":0.0027,"baskets_together":237,"recommendation_rank":58},{"product_name":"Crema solar SPF50","recommended_product_name":"Hilo dental cera","confidence":0.1866,"lift":1.2775,"support":0.0171,"baskets_together":43,"recommendation_rank":59},{"product_name":"Serum acido hialuronico","recommended_product_name":"Crema solar SPF50","confidence":0.1727,"lift":1.2775,"support":0.0052,"baskets_together":170,"recommendation_rank":60},{"product_name":"Te verde antioxidante","recommended_product_name":"Crema corporal hidratante","confidence":0.1342,"lift":1.2742,"support":0.0125,"baskets_together":65,"recommendation_rank":61},{"product_name":"Oximetro de pulso","recommended_product_name":"Termometro digital","confidence":0.4798,"lift":1.2712,"support":0.0213,"baskets_together":155,"recommendation_rank":62},{"product_name":"Hilo dental cera","recommended_product_name":"Infusion manzanilla noche","confidence":0.4868,"lift":1.2656,"support":0.0242,"baskets_together":47,"recommendation_rank":63},{"product_name":"Crema solar SPF50","recommended_product_name":"Magnesio bisglicinato","confidence":0.1994,"lift":1.2617,"support":0.0137,"baskets_together":37,"recommendation_rank":64},{"product_name":"Tensiometro de brazo","recommended_product_name":"Crema corporal hidratante","confidence":0.124,"lift":1.2605,"support":0.004,"baskets_together":200,"recommendation_rank":65},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Aceite esencial lavanda","confidence":0.2417,"lift":1.2598,"support":0.0143,"baskets_together":217,"recommendation_rank":66},{"product_name":"Hilo dental cera","recommended_product_name":"Vitamina D3","confidence":0.2085,"lift":1.2596,"support":0.0068,"baskets_together":23,"recommendation_rank":67},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Crema corporal hidratante","confidence":0.1363,"lift":1.2579,"support":0.0169,"baskets_together":283,"recommendation_rank":68},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Locion corporal aloe","confidence":0.3653,"lift":1.2574,"support":0.023,"baskets_together":123,"recommendation_rank":69},{"product_name":"Miel pura bio","recommended_product_name":"Aceite esencial lavanda","confidence":0.2556,"lift":1.257,"support":0.0247,"baskets_together":68,"recommendation_rank":70},{"product_name":"Vendas elasticas pack","recommended_product_name":"Cinta kinesiologica","confidence":0.1101,"lift":1.2549,"support":0.0139,"baskets_together":283,"recommendation_rank":71},{"product_name":"Serum acido hialuronico","recommended_product_name":"Infusion manzanilla noche","confidence":0.4627,"lift":1.2547,"support":0.0052,"baskets_together":52,"recommendation_rank":72},{"product_name":"Serum acido hialuronico","recommended_product_name":"Crema corporal hidratante","confidence":0.1181,"lift":1.2538,"support":0.026,"baskets_together":244,"recommendation_rank":73},{"product_name":"Cinta kinesiologica","recommended_product_name":"Serum acido hialuronico","confidence":0.4113,"lift":1.2503,"support":0.0067,"baskets_together":99,"recommendation_rank":74},{"product_name":"Rodillo masaje muscular","recommended_product_name":"Repelente mosquitos plantas","confidence":0.0876,"lift":1.2494,"support":0.0204,"baskets_together":100,"recommendation_rank":75},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Termometro digital","confidence":0.3311,"lift":1.247,"support":0.0032,"baskets_together":95,"recommendation_rank":76},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Miel pura bio","confidence":0.0512,"lift":1.2468,"support":0.0165,"baskets_together":67,"recommendation_rank":77},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Proteina whey vainilla","confidence":0.2717,"lift":1.2464,"support":0.0192,"baskets_together":203,"recommendation_rank":78},{"product_name":"Banda elastica resistencia","recommended_product_name":"Serum acido hialuronico","confidence":0.14,"lift":1.2443,"support":0.0203,"baskets_together":291,"recommendation_rank":79},{"product_name":"Rodillo masaje muscular","recommended_product_name":"Barra proteica cacao","confidence":0.1149,"lift":1.2402,"support":0.0233,"baskets_together":36,"recommendation_rank":80},{"product_name":"Locion corporal aloe","recommended_product_name":"Barra proteica cacao","confidence":0.3819,"lift":1.2393,"support":0.0041,"baskets_together":215,"recommendation_rank":81},{"product_name":"Tensiometro de brazo","recommended_product_name":"Hilo dental cera","confidence":0.1785,"lift":1.2392,"support":0.0083,"baskets_together":49,"recommendation_rank":82},{"product_name":"Crema corporal hidratante","recommended_product_name":"Serum acido hialuronico","confidence":0.4835,"lift":1.2351,"support":0.0122,"baskets_together":265,"recommendation_rank":83},{"product_name":"Cepillo dental electrico","recommended_product_name":"Rodillo masaje muscular","confidence":0.3931,"lift":1.2349,"support":0.0095,"baskets_together":251,"recommendation_rank":84},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Multivitaminico diario","confidence":0.4471,"lift":1.2324,"support":0.0083,"baskets_together":232,"recommendation_rank":85},{"product_name":"Cepillo dental electrico","recommended_product_name":"Tensiometro de brazo","confidence":0.4172,"lift":1.2289,"support":0.0191,"baskets_together":112,"recommendation_rank":86},{"product_name":"Serum acido hialuronico","recommended_product_name":"Magnesio bisglicinato","confidence":0.2813,"lift":1.2283,"support":0.0193,"baskets_together":79,"recommendation_rank":87},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Vitamina D3","confidence":0.1898,"lift":1.2236,"support":0.0074,"baskets_together":275,"recommendation_rank":88},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Miel pura bio","confidence":0.1298,"lift":1.2222,"support":0.0071,"baskets_together":79,"recommendation_rank":89},{"product_name":"Pasta dental sensitive","recommended_product_name":"Infusion manzanilla noche","confidence":0.209,"lift":1.2211,"support":0.0264,"baskets_together":294,"recommendation_rank":90},{"product_name":"Pasta dental sensitive","recommended_product_name":"Cepillo dental electrico","confidence":0.339,"lift":1.2206,"support":0.0262,"baskets_together":135,"recommendation_rank":91},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Miel pura bio","confidence":0.2946,"lift":1.219,"support":0.0103,"baskets_together":141,"recommendation_rank":92},{"product_name":"Pasta dental sensitive","recommended_product_name":"Proteina whey vainilla","confidence":0.4022,"lift":1.2187,"support":0.0198,"baskets_together":125,"recommendation_rank":93},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Tensiometro de brazo","confidence":0.323,"lift":1.2171,"support":0.024,"baskets_together":168,"recommendation_rank":94},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Crema solar SPF50","confidence":0.3578,"lift":1.2143,"support":0.0023,"baskets_together":108,"recommendation_rank":95},{"product_name":"Hilo dental cera","recommended_product_name":"Antifaz dormir seda","confidence":0.3417,"lift":1.2109,"support":0.0251,"baskets_together":141,"recommendation_rank":96},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Multivitaminico diario","confidence":0.384,"lift":1.2062,"support":0.0242,"baskets_together":299,"recommendation_rank":97},{"product_name":"Bascula digital corporal","recommended_product_name":"Pulsometro deportivo","confidence":0.1737,"lift":1.2061,"support":0.0223,"baskets_together":196,"recommendation_rank":98},{"product_name":"Te verde antioxidante","recommended_product_name":"Magnesio bisglicinato","confidence":0.3888,"lift":1.2055,"support":0.0164,"baskets_together":164,"recommendation_rank":99},{"product_name":"Miel pura bio","recommended_product_name":"Repelente mosquitos plantas","confidence":0.4551,"lift":1.2032,"support":0.0048,"baskets_together":250,"recommendation_rank":100},{"product_name":"Crema corporal hidratante","recommended_product_name":"Pulsometro deportivo","confidence":0.1678,"lift":1.1994,"support":0.0193,"baskets_together":240,"recommendation_rank":101},{"product_name":"Tensiometro de brazo","recommended_product_name":"Cinta kinesiologica","confidence":0.0554,"lift":1.1947,"support":0.0144,"baskets_together":66,"recommendation_rank":102},{"product_name":"Multivitaminico diario","recommended_product_name":"Crema solar SPF50","confidence":0.1143,"lift":1.1943,"support":0.0071,"baskets_together":215,"recommendation_rank":103},{"product_name":"Crema corporal hidratante","recommended_product_name":"Infusion manzanilla noche","confidence":0.3395,"lift":1.1933,"support":0.002,"baskets_together":215,"recommendation_rank":104},{"product_name":"Termometro digital","recommended_product_name":"Vitamina D3","confidence":0.0902,"lift":1.1891,"support":0.0162,"baskets_together":264,"recommendation_rank":105},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Bebida isotonica citrico","confidence":0.1854,"lift":1.1858,"support":0.0097,"baskets_together":121,"recommendation_rank":106},{"product_name":"Crema corporal hidratante","recommended_product_name":"Barra proteica cacao","confidence":0.3775,"lift":1.1845,"support":0.0221,"baskets_together":207,"recommendation_rank":107},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Locion corporal aloe","confidence":0.3936,"lift":1.1796,"support":0.0197,"baskets_together":108,"recommendation_rank":108},{"product_name":"Cinta kinesiologica","recommended_product_name":"Antifaz dormir seda","confidence":0.4968,"lift":1.178,"support":0.0267,"baskets_together":228,"recommendation_rank":109},{"product_name":"Pulsometro deportivo","recommended_product_name":"Locion corporal aloe","confidence":0.2764,"lift":1.1727,"support":0.021,"baskets_together":47,"recommendation_rank":110},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Cinta kinesiologica","confidence":0.3475,"lift":1.1726,"support":0.0032,"baskets_together":20,"recommendation_rank":111},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Proteina whey vainilla","confidence":0.3197,"lift":1.1725,"support":0.0043,"baskets_together":274,"recommendation_rank":112},{"product_name":"Botella isotermica acero","recommended_product_name":"Crema corporal hidratante","confidence":0.1742,"lift":1.1704,"support":0.0184,"baskets_together":209,"recommendation_rank":113},{"product_name":"Hilo dental cera","recommended_product_name":"Bebida isotonica citrico","confidence":0.1554,"lift":1.1682,"support":0.0127,"baskets_together":169,"recommendation_rank":114},{"product_name":"Termometro digital","recommended_product_name":"Crema solar SPF50","confidence":0.1624,"lift":1.1682,"support":0.0187,"baskets_together":106,"recommendation_rank":115},{"product_name":"Banda elastica resistencia","recommended_product_name":"Termometro digital","confidence":0.1795,"lift":1.1678,"support":0.0254,"baskets_together":75,"recommendation_rank":116},{"product_name":"Te verde antioxidante","recommended_product_name":"Multivitaminico diario","confidence":0.2662,"lift":1.1675,"support":0.017,"baskets_together":250,"recommendation_rank":117},{"product_name":"Botella isotermica acero","recommended_product_name":"Magnesio bisglicinato","confidence":0.2405,"lift":1.1653,"support":0.0053,"baskets_together":273,"recommendation_rank":118},{"product_name":"Antifaz dormir seda","recommended_product_name":"Crema solar SPF50","confidence":0.2999,"lift":1.163,"support":0.0127,"baskets_together":143,"recommendation_rank":119},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Serum acido hialuronico","confidence":0.0816,"lift":1.1612,"support":0.0223,"baskets_together":56,"recommendation_rank":120},{"product_name":"Crema corporal hidratante","recommended_product_name":"Pasta dental sensitive","confidence":0.2207,"lift":1.1586,"support":0.0153,"baskets_together":164,"recommendation_rank":121},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Pasta dental sensitive","confidence":0.1201,"lift":1.156,"support":0.0102,"baskets_together":94,"recommendation_rank":122},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Oximetro de pulso","confidence":0.249,"lift":1.1454,"support":0.0228,"baskets_together":102,"recommendation_rank":123},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Almohada cervical viscoelastica","confidence":0.2383,"lift":1.145,"support":0.0057,"baskets_together":45,"recommendation_rank":124},{"product_name":"Barra proteica cacao","recommended_product_name":"Rodillo masaje muscular","confidence":0.37,"lift":1.1443,"support":0.003,"baskets_together":215,"recommendation_rank":125},{"product_name":"Banda elastica resistencia","recommended_product_name":"Te verde antioxidante","confidence":0.2373,"lift":1.1432,"support":0.023,"baskets_together":278,"recommendation_rank":126},{"product_name":"Botella isotermica acero","recommended_product_name":"Termometro digital","confidence":0.4213,"lift":1.1402,"support":0.0218,"baskets_together":101,"recommendation_rank":127},{"product_name":"Vitamina D3","recommended_product_name":"Cepillo dental electrico","confidence":0.1693,"lift":1.1373,"support":0.0075,"baskets_together":77,"recommendation_rank":128},{"product_name":"Miel pura bio","recommended_product_name":"Termometro digital","confidence":0.3619,"lift":1.1369,"support":0.0112,"baskets_together":187,"recommendation_rank":129},{"product_name":"Vendas elasticas pack","recommended_product_name":"Locion corporal aloe","confidence":0.4133,"lift":1.1357,"support":0.0066,"baskets_together":95,"recommendation_rank":130},{"product_name":"Vendas elasticas pack","recommended_product_name":"Te verde antioxidante","confidence":0.3534,"lift":1.1343,"support":0.0063,"baskets_together":180,"recommendation_rank":131},{"product_name":"Rodillo masaje muscular","recommended_product_name":"Mascarilla facial purificante","confidence":0.18,"lift":1.1321,"support":0.0215,"baskets_together":89,"recommendation_rank":132},{"product_name":"Rodillo masaje muscular","recommended_product_name":"Vitamina D3","confidence":0.1377,"lift":1.1312,"support":0.0193,"baskets_together":166,"recommendation_rank":133},{"product_name":"Multivitaminico diario","recommended_product_name":"Proteina whey vainilla","confidence":0.3271,"lift":1.1312,"support":0.0032,"baskets_together":180,"recommendation_rank":134},{"product_name":"Crema solar SPF50","recommended_product_name":"Cinta kinesiologica","confidence":0.3962,"lift":1.1305,"support":0.0217,"baskets_together":81,"recommendation_rank":135},{"product_name":"Banda elastica resistencia","recommended_product_name":"Multivitaminico diario","confidence":0.2185,"lift":1.1298,"support":0.011,"baskets_together":149,"recommendation_rank":136},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Aceite esencial lavanda","confidence":0.2565,"lift":1.1294,"support":0.0108,"baskets_together":208,"recommendation_rank":137},{"product_name":"Rodillo masaje muscular","recommended_product_name":"Locion corporal aloe","confidence":0.1832,"lift":1.1289,"support":0.0148,"baskets_together":163,"recommendation_rank":138},{"product_name":"Vendas elasticas pack","recommended_product_name":"Crema solar SPF50","confidence":0.3528,"lift":1.1278,"support":0.0118,"baskets_together":111,"recommendation_rank":139},{"product_name":"Proteina whey vainilla","recommended_product_name":"Aceite esencial lavanda","confidence":0.4213,"lift":1.1262,"support":0.014,"baskets_together":269,"recommendation_rank":140},{"product_name":"Cinta kinesiologica","recommended_product_name":"Botella isotermica acero","confidence":0.4433,"lift":1.1251,"support":0.013,"baskets_together":103,"recommendation_rank":141},{"product_name":"Proteina whey vainilla","recommended_product_name":"Pulsometro deportivo","confidence":0.1152,"lift":1.1229,"support":0.0243,"baskets_together":241,"recommendation_rank":142},{"product_name":"Difusor aromaterapia","recommended_product_name":"Cinta kinesiologica","confidence":0.3598,"lift":1.1222,"support":0.0147,"baskets_together":283,"recommendation_rank":143},{"product_name":"Barra proteica cacao","recommended_product_name":"Vitamina D3","confidence":0.4523,"lift":1.1202,"support":0.0046,"baskets_together":67,"recommendation_rank":144},{"product_name":"Cinta kinesiologica","recommended_product_name":"Magnesio bisglicinato","confidence":0.158,"lift":1.1191,"support":0.0147,"baskets_together":143,"recommendation_rank":145},{"product_name":"Pulsometro deportivo","recommended_product_name":"Serum acido hialuronico","confidence":0.3667,"lift":1.1166,"support":0.0176,"baskets_together":175,"recommendation_rank":146},{"product_name":"Barra proteica cacao","recommended_product_name":"Multivitaminico diario","confidence":0.4309,"lift":1.1165,"support":0.0188,"baskets_together":212,"recommendation_rank":147},{"product_name":"Banda elastica resistencia","recommended_product_name":"Almohada cervical viscoelastica","confidence":0.1859,"lift":1.1163,"support":0.0121,"baskets_together":146,"recommendation_rank":148},{"product_name":"Botella isotermica acero","recommended_product_name":"Almohada cervical viscoelastica","confidence":0.4545,"lift":1.1152,"support":0.0153,"baskets_together":94,"recommendation_rank":149},{"product_name":"Difusor aromaterapia","recommended_product_name":"Vendas elasticas pack","confidence":0.1623,"lift":1.1148,"support":0.0141,"baskets_together":242,"recommendation_rank":150},{"product_name":"Hilo dental cera","recommended_product_name":"Locion corporal aloe","confidence":0.478,"lift":1.1139,"support":0.0117,"baskets_together":257,"recommendation_rank":151},{"product_name":"Oximetro de pulso","recommended_product_name":"Proteina whey vainilla","confidence":0.1859,"lift":1.1135,"support":0.0105,"baskets_together":124,"recommendation_rank":152},{"product_name":"Multivitaminico diario","recommended_product_name":"Repelente mosquitos plantas","confidence":0.4732,"lift":1.1118,"support":0.0179,"baskets_together":90,"recommendation_rank":153},{"product_name":"Difusor aromaterapia","recommended_product_name":"Crema solar SPF50","confidence":0.0986,"lift":1.1101,"support":0.0261,"baskets_together":184,"recommendation_rank":154},{"product_name":"Oximetro de pulso","recommended_product_name":"Cinta kinesiologica","confidence":0.1222,"lift":1.1089,"support":0.0225,"baskets_together":66,"recommendation_rank":155},{"product_name":"Pasta dental sensitive","recommended_product_name":"Vendas elasticas pack","confidence":0.1259,"lift":1.1065,"support":0.0071,"baskets_together":164,"recommendation_rank":156},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Tensiometro de brazo","confidence":0.0564,"lift":1.1064,"support":0.0223,"baskets_together":239,"recommendation_rank":157},{"product_name":"Botella isotermica acero","recommended_product_name":"Te verde antioxidante","confidence":0.3025,"lift":1.1055,"support":0.0101,"baskets_together":49,"recommendation_rank":158},{"product_name":"Te verde antioxidante","recommended_product_name":"Botella isotermica acero","confidence":0.2014,"lift":1.1049,"support":0.0152,"baskets_together":258,"recommendation_rank":159},{"product_name":"Botiquin primeros auxilios","recommended_product_name":"Termometro digital","confidence":0.2913,"lift":1.1041,"support":0.0267,"baskets_together":249,"recommendation_rank":160},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Bebida isotonica citrico","confidence":0.1698,"lift":1.1016,"support":0.0036,"baskets_together":90,"recommendation_rank":161},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Serum acido hialuronico","confidence":0.2147,"lift":1.1012,"support":0.0093,"baskets_together":85,"recommendation_rank":162},{"product_name":"Hilo dental cera","recommended_product_name":"Barra proteica cacao","confidence":0.3009,"lift":1.0972,"support":0.008,"baskets_together":214,"recommendation_rank":163},{"product_name":"Serum acido hialuronico","recommended_product_name":"Proteina whey vainilla","confidence":0.4534,"lift":1.0966,"support":0.0233,"baskets_together":193,"recommendation_rank":164},{"product_name":"Proteina whey vainilla","recommended_product_name":"Serum acido hialuronico","confidence":0.2361,"lift":1.0965,"support":0.0155,"baskets_together":154,"recommendation_rank":165},{"product_name":"Crema solar SPF50","recommended_product_name":"Vendas elasticas pack","confidence":0.1858,"lift":1.0938,"support":0.0246,"baskets_together":248,"recommendation_rank":166},{"product_name":"Antifaz dormir seda","recommended_product_name":"Pulsometro deportivo","confidence":0.1286,"lift":1.0883,"support":0.0263,"baskets_together":103,"recommendation_rank":167},{"product_name":"Cinta kinesiologica","recommended_product_name":"Multivitaminico diario","confidence":0.1238,"lift":1.0862,"support":0.0075,"baskets_together":216,"recommendation_rank":168},{"product_name":"Multivitaminico diario","recommended_product_name":"Barra proteica cacao","confidence":0.3303,"lift":1.083,"support":0.0216,"baskets_together":176,"recommendation_rank":169},{"product_name":"Termometro digital","recommended_product_name":"Rodillo masaje muscular","confidence":0.2468,"lift":1.0829,"support":0.0248,"baskets_together":99,"recommendation_rank":170},{"product_name":"Botella isotermica acero","recommended_product_name":"Locion corporal aloe","confidence":0.2548,"lift":1.0818,"support":0.0119,"baskets_together":60,"recommendation_rank":171},{"product_name":"Pasta dental sensitive","recommended_product_name":"Miel pura bio","confidence":0.2714,"lift":1.0805,"support":0.0024,"baskets_together":286,"recommendation_rank":172},{"product_name":"Cepillo dental electrico","recommended_product_name":"Proteina whey vainilla","confidence":0.1976,"lift":1.0791,"support":0.0151,"baskets_together":217,"recommendation_rank":173},{"product_name":"Bascula digital corporal","recommended_product_name":"Termometro digital","confidence":0.4095,"lift":1.079,"support":0.0143,"baskets_together":88,"recommendation_rank":174},{"product_name":"Proteina whey vainilla","recommended_product_name":"Cinta kinesiologica","confidence":0.2345,"lift":1.077,"support":0.0072,"baskets_together":229,"recommendation_rank":175},{"product_name":"Crema corporal hidratante","recommended_product_name":"Miel pura bio","confidence":0.3265,"lift":1.0769,"support":0.0073,"baskets_together":292,"recommendation_rank":176},{"product_name":"Infusion manzanilla noche","recommended_product_name":"Proteina whey vainilla","confidence":0.4587,"lift":1.0715,"support":0.0178,"baskets_together":160,"recommendation_rank":177},{"product_name":"Tensiometro de brazo","recommended_product_name":"Miel pura bio","confidence":0.4458,"lift":1.0676,"support":0.0104,"baskets_together":290,"recommendation_rank":178},{"product_name":"Termometro digital","recommended_product_name":"Tensiometro de brazo","confidence":0.0943,"lift":1.0667,"support":0.0252,"baskets_together":265,"recommendation_rank":179},{"product_name":"Banda elastica resistencia","recommended_product_name":"Cepillo dental electrico","confidence":0.1885,"lift":1.0616,"support":0.011,"baskets_together":75,"recommendation_rank":180},{"product_name":"Banda elastica resistencia","recommended_product_name":"Botiquin primeros auxilios","confidence":0.1532,"lift":1.0607,"support":0.0148,"baskets_together":89,"recommendation_rank":181},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Crema corporal hidratante","confidence":0.1334,"lift":1.0596,"support":0.0029,"baskets_together":24,"recommendation_rank":182},{"product_name":"Banda elastica resistencia","recommended_product_name":"Hilo dental cera","confidence":0.3886,"lift":1.0593,"support":0.0105,"baskets_together":123,"recommendation_rank":183},{"product_name":"Pulsometro deportivo","recommended_product_name":"Botiquin primeros auxilios","confidence":0.2356,"lift":1.0591,"support":0.0039,"baskets_together":120,"recommendation_rank":184},{"product_name":"Serum acido hialuronico","recommended_product_name":"Hilo dental cera","confidence":0.3201,"lift":1.0581,"support":0.0068,"baskets_together":223,"recommendation_rank":185},{"product_name":"Oximetro de pulso","recommended_product_name":"Miel pura bio","confidence":0.0649,"lift":1.0528,"support":0.0211,"baskets_together":80,"recommendation_rank":186},{"product_name":"Cepillo dental electrico","recommended_product_name":"Magnesio bisglicinato","confidence":0.2655,"lift":1.0485,"support":0.0104,"baskets_together":128,"recommendation_rank":187},{"product_name":"Termometro digital","recommended_product_name":"Te verde antioxidante","confidence":0.3211,"lift":1.0458,"support":0.0066,"baskets_together":158,"recommendation_rank":188},{"product_name":"Barra proteica cacao","recommended_product_name":"Aceite esencial lavanda","confidence":0.4881,"lift":1.0404,"support":0.0221,"baskets_together":269,"recommendation_rank":189},{"product_name":"Antifaz dormir seda","recommended_product_name":"Difusor aromaterapia","confidence":0.3672,"lift":1.0387,"support":0.0153,"baskets_together":133,"recommendation_rank":190},{"product_name":"Cinta kinesiologica","recommended_product_name":"Pasta dental sensitive","confidence":0.197,"lift":1.0361,"support":0.0254,"baskets_together":139,"recommendation_rank":191},{"product_name":"Vendas elasticas pack","recommended_product_name":"Proteina whey vainilla","confidence":0.1028,"lift":1.0355,"support":0.0115,"baskets_together":285,"recommendation_rank":192},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Serum acido hialuronico","confidence":0.3388,"lift":1.035,"support":0.0235,"baskets_together":62,"recommendation_rank":193},{"product_name":"Pulsometro deportivo","recommended_product_name":"Repelente mosquitos plantas","confidence":0.311,"lift":1.035,"support":0.0246,"baskets_together":36,"recommendation_rank":194},{"product_name":"Bebida isotonica citrico","recommended_product_name":"Infusion manzanilla noche","confidence":0.1708,"lift":1.0302,"support":0.0208,"baskets_together":117,"recommendation_rank":195},{"product_name":"Crema solar SPF50","recommended_product_name":"Bascula digital corporal","confidence":0.2965,"lift":1.0284,"support":0.0182,"baskets_together":95,"recommendation_rank":196},{"product_name":"Vendas elasticas pack","recommended_product_name":"Bascula digital corporal","confidence":0.3377,"lift":1.0276,"support":0.0128,"baskets_together":250,"recommendation_rank":197},{"product_name":"Serum acido hialuronico","recommended_product_name":"Miel pura bio","confidence":0.1558,"lift":1.0256,"support":0.0246,"baskets_together":174,"recommendation_rank":198},{"product_name":"Vitamina D3","recommended_product_name":"Miel pura bio","confidence":0.1954,"lift":1.0251,"support":0.0218,"baskets_together":281,"recommendation_rank":199},{"product_name":"Pulsometro deportivo","recommended_product_name":"Pasta dental sensitive","confidence":0.1868,"lift":1.0224,"support":0.0168,"baskets_together":274,"recommendation_rank":200},{"product_name":"Crema solar SPF50","recommended_product_name":"Cepillo dental electrico","confidence":0.3548,"lift":1.0104,"support":0.0102,"baskets_together":85,"recommendation_rank":201},{"product_name":"Aceite esencial lavanda","recommended_product_name":"Cinta kinesiologica","confidence":0.0643,"lift":1.0097,"support":0.0065,"baskets_together":281,"recommendation_rank":202},{"product_name":"Locion corporal aloe","recommended_product_name":"Antifaz dormir seda","confidence":0.3527,"lift":1.0097,"support":0.0215,"baskets_together":294,"recommendation_rank":203},{"product_name":"Botella isotermica acero","recommended_product_name":"Infusion manzanilla noche","confidence":0.1927,"lift":1.0095,"support":0.0089,"baskets_together":74,"recommendation_rank":204},{"product_name":"Magnesio bisglicinato","recommended_product_name":"Cinta kinesiologica","confidence":0.4153,"lift":1.007,"support":0.0238,"baskets_together":260,"recommendation_rank":205},{"product_name":"Tensiometro de brazo","recommended_product_name":"Serum acido hialuronico","confidence":0.1033,"lift":1.0055,"support":0.0107,"baskets_together":62,"recommendation_rank":206},{"product_name":"Locion corporal aloe","recommended_product_name":"Te verde antioxidante","confidence":0.3698,"lift":1.0037,"support":0.0252,"baskets_together":218,"recommendation_rank":207},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Crema solar SPF50","confidence":0.2536,"lift":0.9812,"support":0.0248,"baskets_together":71,"recommendation_rank":208},{"product_name":"Termometro digital","recommended_product_name":"Almohada cervical viscoelastica","confidence":0.3612,"lift":0.9751,"support":0.0062,"baskets_together":290,"recommendation_rank":209},{"product_name":"Barra proteica cacao","recommended_product_name":"Banda elastica resistencia","confidence":0.4141,"lift":0.9506,"support":0.0115,"baskets_together":68,"recommendation_rank":210},{"product_name":"Proteina whey vainilla","recommended_product_name":"Miel pura bio","confidence":0.2696,"lift":0.9444,"support":0.0052,"baskets_together":286,"recommendation_rank":211},{"product_name":"Pasta dental sensitive","recommended_product_name":"Te verde antioxidante","confidence":0.4815,"lift":0.9385,"support":0.0264,"baskets_together":112,"recommendation_rank":212},{"product_name":"Repelente mosquitos plantas","recommended_product_name":"Bebida isotonica citrico","confidence":0.4847,"lift":0.9294,"support":0.0165,"baskets_together":142,"recommendation_rank":213},{"product_name":"Difusor aromaterapia","recommended_product_name":"Mascarilla facial purificante","confidence":0.1883,"lift":0.9132,"support":0.0051,"baskets_together":34,"recommendation_rank":214},{"product_name":"Difusor aromaterapia","recommended_product_name":"Pasta dental sensitive","confidence":0.1417,"lift":0.9023,"support":0.0207,"baskets_together":181,"recommendation_rank":215},{"product_name":"Locion corporal aloe","recommended_product_name":"Botiquin primeros auxilios","confidence":0.4633,"lift":0.8968,"support":0.0152,"baskets_together":63,"recommendation_rank":216},{"product_name":"Termometro digital","recommended_product_name":"Pasta dental sensitive","confidence":0.3723,"lift":0.8928,"support":0.0195,"baskets_together":283,"recommendation_rank":217},{"product_name":"Locion corporal aloe","recommended_product_name":"Termometro digital","confidence":0.2647,"lift":0.8758,"support":0.0257,"baskets_together":165,"recommendation_rank":218},{"product_name":"Oximetro de pulso","recommended_product_name":"Vitamina D3","confidence":0.0828,"lift":0.8363,"support":0.0173,"baskets_together":79,"recommendation_rank":219},{"product_name":"Crema corporal hidratante","recommended_product_name":"Hilo dental cera","confidence":0.3273,"lift":0.8211,"support":0.0249,"baskets_together":289,"recommendation_rank":220},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Botiquin primeros auxilios","confidence":0.2935,"lift":0.8113,"support":0.0214,"baskets_together":285,"recommendation_rank":221},{"product_name":"Difusor aromaterapia","recommended_product_name":"Te verde antioxidante","confidence":0.2057,"lift":0.7781,"support":0.0051,"baskets_together":98,"recommendation_rank":222},{"product_name":"Serum acido hialuronico","recommended_product_name":"Antifaz dormir seda","confidence":0.2239,"lift":0.7766,"support":0.0179,"baskets_together":92,"recommendation_rank":223},{"product_name":"Multivitaminico diario","recommended_product_name":"Botiquin primeros auxilios","confidence":0.4246,"lift":0.7665,"support":0.0041,"baskets_together":96,"recommendation_rank":224},{"product_name":"Aceite esencial lavanda","recommended_product_name":"Miel pura bio","confidence":0.2416,"lift":0.7627,"support":0.0083,"baskets_together":253,"recommendation_rank":225},{"product_name":"Te verde antioxidante","recommended_product_name":"Termometro digital","confidence":0.1035,"lift":0.7152,"support":0.0199,"baskets_together":71,"recommendation_rank":226},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Multivitaminico diario","confidence":0.4892,"lift":0.7067,"support":0.0139,"baskets_together":247,"recommendation_rank":227},{"product_name":"Aceite esencial lavanda","recommended_product_name":"Pulsometro deportivo","confidence":0.4079,"lift":0.687,"support":0.02,"baskets_together":85,"recommendation_rank":228},{"product_name":"Aceite esencial lavanda","recommended_product_name":"Termometro digital","confidence":0.4822,"lift":0.649,"support":0.0268,"baskets_together":144,"recommendation_rank":229},{"product_name":"Cepillo dental electrico","recommended_product_name":"Botella isotermica acero","confidence":0.2858,"lift":0.6403,"support":0.0073,"baskets_together":127,"recommendation_rank":230},{"product_name":"Mascarilla facial purificante","recommended_product_name":"Rodillo masaje muscular","confidence":0.2377,"lift":0.6382,"support":0.0052,"baskets_together":293,"recommendation_rank":231},{"product_name":"Vendas elasticas pack","recommended_product_name":"Serum acido hialuronico","confidence":0.3971,"lift":0.6231,"support":0.0187,"baskets_together":97,"recommendation_rank":232},{"product_name":"Crema corporal hidratante","recommended_product_name":"Rodillo masaje muscular","confidence":0.2965,"lift":0.609,"support":0.0073,"baskets_together":218,"recommendation_rank":233},{"product_name":"Almohada cervical viscoelastica","recommended_product_name":"Botella isotermica acero","confidence":0.1327,"lift":0.6083,"support":0.0086,"baskets_together":159,"recommendation_rank":234},{"product_name":"Banda elastica resistencia","recommended_product_name":"Mascarilla facial purificante","confidence":0.152,"lift":0.6028,"support":0.026,"baskets_together":156,"recommendation_rank":235}];
</script>
<script type="text/babel">
// Plotly chart helpers — shared layout for the dashboard.
const PLOTLY_BASE_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: { family: 'Inter, system-ui, sans-serif', size: 11.5, color: '#e6edf3' },
  margin: { l: 8, r: 12, t: 10, b: 8 },
  xaxis: { gridcolor: '#1f2630', zeroline: false, color: '#8b96a5', tickfont: { size: 10.5 } },
  yaxis: { gridcolor: '#1f2630', zeroline: false, color: '#8b96a5', tickfont: { size: 10.5 } },
  hoverlabel: { bgcolor: '#11161d', bordercolor: '#2a323d', font: { color: '#e6edf3', size: 12 } },
  legend: { bgcolor: 'rgba(0,0,0,0)', font: { color: '#8b96a5', size: 11 } },
};

const PLOTLY_CONFIG = { displayModeBar: false, responsive: true };

const PALETTE = ['#5ec2b6', '#7aa2d8', '#c9a66b', '#b07ab0', '#d98a7a', '#8a9fb0', '#6f8f7a'];

const CHURN_COLOR = {
  'Bajo': '#5ec2b6',
  'Medio': '#c9a66b',
  'Alto': '#d98a7a',
  'Critico': '#c46a6a',
  'Crítico': '#c46a6a',
};

function PlotlyChart({ data, layout, height = 320, style }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (!ref.current) return;
    const merged = {
      ...PLOTLY_BASE_LAYOUT,
      ...layout,
      height,
      xaxis: { ...PLOTLY_BASE_LAYOUT.xaxis, ...(layout?.xaxis || {}) },
      yaxis: { ...PLOTLY_BASE_LAYOUT.yaxis, ...(layout?.yaxis || {}) },
    };
    window.Plotly.react(ref.current, data, merged, PLOTLY_CONFIG);
    const onResize = () => window.Plotly.Plots.resize(ref.current);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [data, layout, height]);
  return <div ref={ref} className="chart" style={{ height, ...style }} />;
}

// Formatters
function fmtEur(x) {
  if (x == null || isNaN(x)) return '—';
  return '€ ' + Math.round(x).toLocaleString('es-ES').replace(/,/g, ' ');
}
function fmtInt(x) {
  if (x == null || isNaN(x)) return '—';
  return Math.round(x).toLocaleString('es-ES').replace(/,/g, ' ');
}
function fmtPct(x, d = 1) {
  if (x == null || isNaN(x)) return '—';
  return (x * 100).toFixed(d) + '%';
}
function fmtNum(x, d = 2) {
  if (x == null || isNaN(x)) return '—';
  return x.toFixed(d);
}

// KPI primitive
function Kpi({ label, value, delta, deltaTone = 'accent', spark }) {
  return (
    <div className="kpi">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {delta && <div className={`kpi-delta ${deltaTone}`}>{delta}</div>}
      {spark}
    </div>
  );
}

function ChurnPill({ level }) {
  if (!level) return null;
  return <span className={`pill churn-${level === 'Crítico' ? 'Critico' : level}`}>{level}</span>;
}

Object.assign(window, { PlotlyChart, PLOTLY_BASE_LAYOUT, PALETTE, CHURN_COLOR, Kpi, ChurnPill, fmtEur, fmtInt, fmtPct, fmtNum });

</script>
<script type="text/babel">
// Pages 1-3: Overview, Customer 360, Segmentation
const RFM_ORDER = [
  'Clientes estrella', 'Alto valor', 'Clientes fieles recientes',
  'Clientes medios', 'Valiosos en riesgo', 'Clientes dormidos',
];
const CHURN_ORDER = ['Bajo', 'Medio', 'Alto', 'Critico'];

// ============================================================
// 1. OVERVIEW
// ============================================================
function PageOverview({ stats }) {
  const kpis = [
    { label: 'Clientes', value: fmtInt(stats.total), delta: '5 750 en DWH' },
    { label: 'Ingresos netos', value: '€ ' + (stats.sumIngresos/1e6).toFixed(2) + ' M', delta: fmtEur(stats.sumIngresos) },
    { label: 'Margen estimado', value: '€ ' + (stats.sumMargen/1e6).toFixed(2) + ' M', delta: '40.0% s/ingresos' },
    { label: 'Churn medio', value: stats.avgChurn.toFixed(1), delta: '0–100 score' },
    { label: 'Con cluster', value: fmtInt(stats.total) },
    { label: 'Validaciones', value: '14 / 14', delta: 'OK', deltaTone: 'accent' },
  ];

  // Margen por RFM (horizontal bar)
  const segs = RFM_ORDER.filter(s => stats.marginBySeg[s] != null);
  const marginPlot = [{
    type: 'bar', orientation: 'h',
    x: segs.map(s => stats.marginBySeg[s]),
    y: segs,
    marker: { color: '#5ec2b6' },
    hovertemplate: '%{y}<br>€ %{x:,.0f}<extra></extra>',
  }];

  // Clientes por nivel de churn (vertical bar)
  const churnPlot = [{
    type: 'bar',
    x: CHURN_ORDER,
    y: CHURN_ORDER.map(l => stats.byChurn[l] || 0),
    marker: { color: CHURN_ORDER.map(l => CHURN_COLOR[l]) },
    hovertemplate: '%{x}: %{y} clientes<extra></extra>',
  }];

  const findings = [
    ['Concentración de margen', '1 218 clientes estrella aportan la mayor parte del margen total del negocio.'],
    ['Riesgo accionable', '726 clientes valiosos en riesgo: candidatos prioritarios a campaña de reactivación.'],
    ['Reglas de afinidad', '235 recomendaciones producto-producto generadas, 207 con lift > 1.'],
    ['Calidad de datos', 'Producto 29 (Sensor temperatura) sin coste maestro: 711 líneas con coste imputado.'],
    ['Cobertura analítica', '5 750 / 5 750 clientes con churn score y cluster K-Means asignado.'],
  ];

  return (
    <div>
      <h1 className="page-title">Resumen ejecutivo</h1>
      <div className="page-sub">Saleshealth · cierre 2025-12-30 · DWH dwh.customer_360</div>

      <div className="grid grid-6">
        {kpis.map((k, i) => <Kpi key={i} {...k} />)}
      </div>

      <div className="spacer-20" />

      <div className="grid grid-12">
        <div className="panel">
          <div className="panel-head">
            <div className="section-title">Margen por segmento RFM</div>
            <span className="pill">€ ingresos netos × margen %</span>
          </div>
          <PlotlyChart
            data={marginPlot}
            layout={{
              xaxis: { tickformat: ',.0f', tickprefix: '€ ', title: '' },
              yaxis: { automargin: true },
              margin: { l: 10, r: 12, t: 6, b: 24 },
            }}
            height={300}
          />
        </div>
        <div className="panel">
          <div className="panel-head">
            <div className="section-title">Clientes por nivel de churn</div>
            <span className="pill">{fmtInt(stats.total)} clientes</span>
          </div>
          <PlotlyChart
            data={churnPlot}
            layout={{ margin: { l: 36, r: 12, t: 6, b: 28 } }}
            height={300}
          />
        </div>
      </div>

      <div className="spacer-28" />
      <div className="section-title">Principales hallazgos</div>
      <div className="findings">
        {findings.map(([t, d], i) => (
          <div className="finding-row" key={i}>
            <div className="finding-title">{t}</div>
            <div className="finding-text">{d}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// 2. CUSTOMER 360
// ============================================================
function PageCustomer360({ customers }) {
  const sorted = React.useMemo(
    () => [...customers].sort((a, b) => b.margen_neto_estimado - a.margen_neto_estimado),
    [customers]
  );
  const [query, setQuery] = React.useState('');
  const [selectedId, setSelectedId] = React.useState(sorted[0]?.customer_id);

  const filtered = sorted.filter(c =>
    c.full_name.toLowerCase().includes(query.toLowerCase()) ||
    String(c.customer_id).includes(query)
  );
  const cust = sorted.find(c => c.customer_id === selectedId) || sorted[0];

  return (
    <div>
      <h1 className="page-title">Customer 360</h1>
      <div className="page-sub">Ficha analítica por cliente · 5 750 perfiles disponibles</div>

      <div className="grid grid-2" style={{ gridTemplateColumns: '1.4fr 1fr', marginBottom: 18 }}>
        <div>
          <div className="field-label">Buscar cliente</div>
          <input
            className="input"
            placeholder="Nombre o customer_id…"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
        <div>
          <div className="field-label">Seleccionar</div>
          <select
            className="select"
            value={cust.customer_id}
            onChange={e => setSelectedId(+e.target.value)}
          >
            {filtered.slice(0, 60).map(c => (
              <option key={c.customer_id} value={c.customer_id}>
                {c.full_name} · #{c.customer_id} · {c.segmento_rfm}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="cust-hero">
        <div className="cust-hero-row">
          <div className="cust-name">{cust.full_name}</div>
          <div className="cust-id mono">customer_id · {cust.customer_id}</div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 8, alignItems: 'center' }}>
            <span className="pill">churn score · <b className="mono" style={{ color: '#e6edf3' }}>{cust.churn_risk_score}</b></span>
            <ChurnPill level={cust.churn_risk_level} />
          </div>
        </div>
        <div className="cust-meta">
          <b>{cust.segmento_rfm}</b>  ·  <b>{cust.cluster_name}</b>  ·  
          recencia <b>{cust.recencia_dias} d</b>  ·  
          frecuencia <b>{cust.frecuencia_mensual.toFixed(2)}/mes</b>
        </div>
      </div>

      <div className="grid grid-4">
        <Kpi label="Ingresos netos" value={fmtEur(cust.ingresos_netos)} />
        <Kpi label="Margen estimado" value={fmtEur(cust.margen_neto_estimado)} />
        <Kpi label="CLTV histórico" value={fmtEur(cust.cltv_historico_margen)} delta="margen acumulado" />
        <Kpi label="CLTV 12m" value={fmtEur(cust.cltv_estimado_12m_margen)} delta="proyectado" />
      </div>

      <div className="spacer-12" />

      <div className="grid grid-4">
        <Kpi label="Nº de compras" value={fmtInt(cust.numero_compras)} />
        <Kpi label="Recencia" value={`${cust.recencia_dias} d`} />
        <Kpi label="Frec. mensual" value={cust.frecuencia_mensual.toFixed(2)} />
        <Kpi label="Tasa devolución" value={fmtPct(cust.tasa_devolucion_importe, 2)} />
      </div>

      <div className="spacer-20" />

      <div className="section-title">Acción recomendada</div>
      <div className="action-card">
        <div style={{ fontSize: 11, letterSpacing: '0.08em', textTransform: 'uppercase', color: '#5ec2b6', marginBottom: 6 }}>
          recommended_action
        </div>
        {cust.recommended_action || 'Sin recomendación.'}
      </div>
    </div>
  );
}

// ============================================================
// 3. SEGMENTATION
// ============================================================
function PageSegmentation({ stats, customers }) {
  const segs = RFM_ORDER.filter(s => stats.bySeg[s] != null);
  const segPlot = [{
    type: 'bar', orientation: 'h',
    x: segs.map(s => stats.bySeg[s]), y: segs,
    marker: { color: '#5ec2b6' },
    hovertemplate: '%{y}<br>%{x} clientes<extra></extra>',
  }];

  const clusters = Object.keys(stats.byCluster);
  const clusterPlot = [{
    type: 'bar', orientation: 'h',
    x: clusters.map(c => stats.byCluster[c]), y: clusters,
    marker: { color: clusters.map((_, i) => PALETTE[i % PALETTE.length]) },
    hovertemplate: '%{y}<br>%{x} clientes<extra></extra>',
  }];

  // PCA scatter — group points by cluster
  const pcaTraces = clusters.map((cl, i) => {
    const pts = stats.pcaSample.filter(p => p.cluster === cl);
    return {
      type: 'scattergl',
      mode: 'markers',
      x: pts.map(p => p.x),
      y: pts.map(p => p.y),
      name: cl,
      marker: { color: PALETTE[i % PALETTE.length], size: 5, opacity: 0.7, line: { width: 0 } },
      hovertemplate: `${cl}<br>pca_1: %{x:.2f}<br>pca_2: %{y:.2f}<extra></extra>`,
    };
  });

  return (
    <div>
      <h1 className="page-title">Segmentación</h1>
      <div className="page-sub">RFM · Clustering K-Means sobre PCA (4 clusters)</div>

      <div className="grid grid-2">
        <div className="panel">
          <div className="section-title">Distribución por RFM</div>
          <PlotlyChart
            data={segPlot}
            layout={{ yaxis: { automargin: true }, margin: { l: 10, r: 12, t: 6, b: 24 } }}
            height={280}
          />
        </div>
        <div className="panel">
          <div className="section-title">Distribución por cluster</div>
          <PlotlyChart
            data={clusterPlot}
            layout={{ yaxis: { automargin: true }, margin: { l: 10, r: 12, t: 6, b: 24 } }}
            height={280}
          />
        </div>
      </div>

      <div className="spacer-20" />

      <div className="panel">
        <div className="panel-head">
          <div>
            <div className="section-title">PCA · pca_1 vs pca_2</div>
            <div className="section-sub">{stats.pcaSample.length} puntos muestreados de 5 750</div>
          </div>
          <span className="pill">scatter · K-Means k=4</span>
        </div>
        <PlotlyChart
          data={pcaTraces}
          layout={{
            xaxis: { title: { text: 'pca_1', font: { color: '#8b96a5', size: 10 } } },
            yaxis: { title: { text: 'pca_2', font: { color: '#8b96a5', size: 10 } } },
            legend: { orientation: 'h', y: -0.18, x: 0 },
            margin: { l: 36, r: 12, t: 6, b: 60 },
          }}
          height={420}
        />
      </div>

      <div className="spacer-20" />
      <div className="section-title">Resumen por cluster</div>
      <div className="table-wrap">
        <table className="tbl">
          <thead>
            <tr>
              <th>Cluster</th>
              <th className="num">Clientes</th>
              <th className="num">Ingresos</th>
              <th className="num">Margen</th>
              <th className="num">Churn medio</th>
              <th className="num">Tasa devolución</th>
            </tr>
          </thead>
          <tbody>
            {[...stats.clusterSummary].sort((a, b) => b.margen - a.margen).map((r, i) => (
              <tr key={i}>
                <td>{r.cluster_name}</td>
                <td className="num mono">{fmtInt(r.clientes)}</td>
                <td className="num mono">{fmtEur(r.ingresos)}</td>
                <td className="num mono">{fmtEur(r.margen)}</td>
                <td className="num mono">{r.churn_medio.toFixed(1)}</td>
                <td className="num mono">{(r.tasa_dev_media * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

Object.assign(window, { PageOverview, PageCustomer360, PageSegmentation, RFM_ORDER, CHURN_ORDER });

</script>
<script type="text/babel">
// Pages 4-6: Churn, Market Basket, Data Quality

// ============================================================
// 4. CHURN
// ============================================================
function PageChurn({ stats, customers }) {
  const nAlto = stats.byChurn['Alto'] || 0;
  const nCritico = (stats.byChurn['Critico'] || 0) + (stats.byChurn['Crítico'] || 0);

  const segs = RFM_ORDER.filter(s => stats.churnBySeg[s] != null);
  const segPlot = [{
    type: 'bar', orientation: 'h',
    x: segs.map(s => stats.churnBySeg[s]), y: segs,
    marker: { color: '#5ec2b6' },
    hovertemplate: '%{y}<br>churn medio: %{x:.1f}<extra></extra>',
  }];

  const clusters = Object.keys(stats.churnByCluster);
  const clPlot = [{
    type: 'bar', orientation: 'h',
    x: clusters.map(c => stats.churnByCluster[c]), y: clusters,
    marker: { color: clusters.map((_, i) => PALETTE[i % PALETTE.length]) },
    hovertemplate: '%{y}<br>churn medio: %{x:.1f}<extra></extra>',
  }];

  // Top clients at risk
  const atRisk = customers
    .filter(c => c.churn_risk_level === 'Alto' || c.churn_risk_level === 'Critico' || c.churn_risk_level === 'Crítico')
    .sort((a, b) => (b.churn_risk_score - a.churn_risk_score) || (b.margen_neto_estimado - a.margen_neto_estimado))
    .slice(0, 30);

  const margenRiesgo = customers
    .filter(c => c.churn_risk_level === 'Alto' || c.churn_risk_level === 'Critico' || c.churn_risk_level === 'Crítico')
    .reduce((a, c) => a + c.margen_neto_estimado, 0);

  return (
    <div>
      <h1 className="page-title">Churn</h1>
      <div className="page-sub">Riesgo de fuga y acción comercial recomendada</div>

      <div className="grid grid-4">
        <Kpi label="Riesgo Alto" value={fmtInt(nAlto)} delta="acción media" deltaTone="warn" />
        <Kpi label="Riesgo Crítico" value={fmtInt(nCritico)} delta="acción urgente" deltaTone="danger" />
        <Kpi label="Margen en riesgo (top)" value={fmtEur(margenRiesgo)} delta="muestra top-30" />
        <Kpi label="Score medio" value={stats.avgChurn.toFixed(1)} delta="0–100" />
      </div>

      <div className="spacer-20" />

      <div className="grid grid-2">
        <div className="panel">
          <div className="section-title">Churn medio por segmento RFM</div>
          <PlotlyChart
            data={segPlot}
            layout={{
              xaxis: { range: [0, 100], title: '' },
              yaxis: { automargin: true },
              margin: { l: 10, r: 12, t: 6, b: 28 },
            }}
            height={300}
          />
        </div>
        <div className="panel">
          <div className="section-title">Churn medio por cluster</div>
          <PlotlyChart
            data={clPlot}
            layout={{
              xaxis: { range: [0, 100], title: '' },
              yaxis: { automargin: true },
              margin: { l: 10, r: 12, t: 6, b: 28 },
            }}
            height={300}
          />
        </div>
      </div>

      <div className="spacer-20" />
      <div className="panel-head">
        <div>
          <div className="section-title">Top clientes en riesgo</div>
          <div className="section-sub">Ordenados por churn_risk_score y margen</div>
        </div>
        <span className="pill">muestra · {atRisk.length} de top-50</span>
      </div>

      <div className="table-wrap">
        <table className="tbl">
          <thead>
            <tr>
              <th>Cliente</th>
              <th className="mono">id</th>
              <th>Segmento</th>
              <th>Cluster</th>
              <th className="num">Score</th>
              <th>Nivel</th>
              <th className="num">Margen</th>
              <th className="num">Recencia</th>
              <th>Acción recomendada</th>
            </tr>
          </thead>
          <tbody>
            {atRisk.map((c, i) => (
              <tr key={i}>
                <td>{c.full_name}</td>
                <td className="muted mono">#{c.customer_id}</td>
                <td className="muted">{c.segmento_rfm}</td>
                <td className="muted">{c.cluster_name}</td>
                <td className="num mono">{c.churn_risk_score}</td>
                <td><ChurnPill level={c.churn_risk_level} /></td>
                <td className="num mono">{fmtEur(c.margen_neto_estimado)}</td>
                <td className="num mono">{c.recencia_dias} d</td>
                <td className="muted">{c.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ============================================================
// 5. MARKET BASKET
// ============================================================
function PageMarketBasket({ recs }) {
  const products = React.useMemo(
    () => Array.from(new Set(recs.map(r => r.product_name))).sort(),
    [recs]
  );
  const [base, setBase] = React.useState('(todos)');

  const filtered = React.useMemo(() => {
    const v = base === '(todos)' ? recs : recs.filter(r => r.product_name === base);
    return [...v].sort((a, b) => b.lift - a.lift);
  }, [recs, base]);

  const top = filtered.slice(0, 12);
  const liftPlot = [{
    type: 'bar', orientation: 'h',
    x: top.map(r => r.lift),
    y: top.map(r => r.recommended_product_name),
    marker: { color: '#5ec2b6' },
    hovertemplate: '%{y}<br>lift: %{x:.3f}<extra></extra>',
  }];

  const liftMean = filtered.length ? filtered.reduce((a, r) => a + r.lift, 0) / filtered.length : 0;
  const confMean = filtered.length ? filtered.reduce((a, r) => a + r.confidence, 0) / filtered.length : 0;

  return (
    <div>
      <h1 className="page-title">Market Basket</h1>
      <div className="page-sub">Productos comprados juntos · 1 225 pares analizados · 235 reglas generadas</div>

      <div className="grid grid-2" style={{ gridTemplateColumns: '1fr 2fr', marginBottom: 18 }}>
        <div>
          <div className="field-label">Producto base</div>
          <select className="select" value={base} onChange={e => setBase(e.target.value)}>
            <option value="(todos)">(todos los productos)</option>
            {products.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div className="grid grid-3" style={{ gap: 12 }}>
          <Kpi label="Reglas filtradas" value={fmtInt(filtered.length)} />
          <Kpi label="Lift medio" value={liftMean.toFixed(3)} />
          <Kpi label="Confidence media" value={fmtPct(confMean, 1)} />
        </div>
      </div>

      <div className="grid grid-12">
        <div className="panel">
          <div className="panel-head">
            <div className="section-title">Top recomendaciones por lift</div>
            <span className="pill mono">top 12</span>
          </div>
          <PlotlyChart
            data={liftPlot}
            layout={{
              yaxis: { automargin: true, autorange: 'reversed' },
              xaxis: { title: { text: 'lift', font: { color: '#8b96a5', size: 10 } } },
              margin: { l: 10, r: 12, t: 6, b: 36 },
            }}
            height={420}
          />
        </div>
        <div className="panel" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '14px 18px 8px' }}>
            <div className="section-title">Detalle de reglas</div>
            <div className="section-sub">A → B · ordenado por lift</div>
          </div>
          <div style={{ maxHeight: 420, overflowY: 'auto' }}>
            <table className="tbl">
              <thead>
                <tr>
                  <th>Producto A</th>
                  <th>Producto B</th>
                  <th className="num">Conf.</th>
                  <th className="num">Lift</th>
                  <th className="num">Sup.</th>
                  <th className="num">Tickets</th>
                </tr>
              </thead>
              <tbody>
                {filtered.slice(0, 60).map((r, i) => (
                  <tr key={i}>
                    <td>{r.product_name}</td>
                    <td>{r.recommended_product_name}</td>
                    <td className="num mono">{(r.confidence * 100).toFixed(1)}%</td>
                    <td className="num mono" style={{ color: r.lift > 1 ? '#5ec2b6' : '#8b96a5' }}>{r.lift.toFixed(3)}</td>
                    <td className="num mono">{(r.support * 100).toFixed(2)}%</td>
                    <td className="num mono">{r.baskets_together}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="legend-explain">
        <div className="item">
          <h4>support</h4>
          <p>Frecuencia del par sobre el total de tickets. Mide cuánto de común es la combinación.</p>
        </div>
        <div className="item">
          <h4>confidence</h4>
          <p>Probabilidad de que un ticket contenga <b>B</b> dado que ya contiene <b>A</b>.</p>
        </div>
        <div className="item">
          <h4>lift</h4>
          <p>Fuerza de asociación. <b>lift &gt; 1</b> indica que A aumenta la probabilidad de B respecto al azar.</p>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 6. DATA QUALITY
// ============================================================
function PageDataQuality() {
  const checks = [
    'row_count_fact_sales', 'row_count_dim_customer', 'row_count_customer_360',
    'customer_360_no_nulls_pk', 'fact_sales_fk_customer', 'fact_sales_fk_product',
    'fact_sales_fk_date', 'margen_pct_rango', 'churn_score_rango',
    'rfm_score_rango', 'cltv_no_negativo', 'cluster_completitud',
    'product_recommendations_lift', 'coste_imputado_trazado',
  ];

  return (
    <div>
      <h1 className="page-title">Calidad de datos</h1>
      <div className="page-sub">Validaciones del DWH · Trazabilidad de imputaciones</div>

      <div className="grid grid-4">
        <Kpi label="Validaciones" value="14 / 14" delta="OK" deltaTone="accent" />
        <Kpi label="Líneas con coste imputado" value="711" delta="lineas_coste_imputado=1" />
        <Kpi label="Unidades afectadas" value="1 426" />
        <Kpi label="Margen recuperado" value="€ 11 408" delta="estimación 60% precio" />
      </div>

      <div className="spacer-20" />

      <div className="section-title">Producto 29 — Sensor temperatura inteligente</div>
      <div className="callout">
        El producto <span className="mono">product_id = 29</span> (<b>Sensor temperatura inteligente</b>)
        aparece en ventas pero no existe en <span className="mono">central_product</span>. Para no perder
        trazabilidad, el DWH conserva el coste original nulo y añade un <b>coste analítico imputado</b>
        igual al 60 % del precio de venta.
        <div className="spacer-12" />
        Las filas afectadas se marcan con <span className="mono">lineas_coste_imputado = 1</span> en
        <span className="mono"> dwh.customer_360</span>. Los ingresos siguen siendo correctos; el margen
        queda como estimación. Se recomienda completar el catálogo en <span className="mono">central_product</span>
        y reejecutar <span className="mono">scripts/run_pipeline.sh</span>.
      </div>

      <div className="spacer-20" />
      <div className="grid grid-3">
        <div className="panel panel-tight">
          <div className="kpi-label">Ingresos afectados</div>
          <div className="kpi-value sm">€ 28 506</div>
          <div className="kpi-delta">trazados, no perdidos</div>
        </div>
        <div className="panel panel-tight">
          <div className="kpi-label">Coste analítico imputado</div>
          <div className="kpi-value sm">€ 17 098</div>
          <div className="kpi-delta">60 % del precio de venta</div>
        </div>
        <div className="panel panel-tight">
          <div className="kpi-label">Margen estimado recuperado</div>
          <div className="kpi-value sm">€ 11 408</div>
          <div className="kpi-delta">aporta a CLTV</div>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="section-title">Resultado de las 14 validaciones</div>
      <div className="checks">
        {checks.map(c => (
          <div className="check" key={c}>
            <span className="mono" style={{ color: '#cfd6df' }}>{c}</span>
            <span className="ok">OK</span>
          </div>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { PageChurn, PageMarketBasket, PageDataQuality });

</script>
<script type="text/babel">
// Main shell: sidebar + page router
const PAGES = [
  { id: 'overview', label: 'Resumen ejecutivo', num: '01' },
  { id: 'customer360', label: 'Customer 360', num: '02' },
  { id: 'segmentation', label: 'Segmentación', num: '03' },
  { id: 'churn', label: 'Churn', num: '04' },
  { id: 'basket', label: 'Market Basket', num: '05' },
  { id: 'quality', label: 'Calidad de datos', num: '06' },
];

function Sidebar({ active, onChange }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">◆</div>
        <div>
          <div className="brand-name">Saleshealth</div>
          <div className="brand-sub">Customer Intel.</div>
        </div>
      </div>

      <div className="nav-section">Navegación</div>
      {PAGES.map(p => (
        <div
          key={p.id}
          className={`nav-item ${active === p.id ? 'active' : ''}`}
          onClick={() => onChange(p.id)}
        >
          <span className="nav-num">{p.num}</span>
          <span>{p.label}</span>
        </div>
      ))}

      <div className="sidebar-footer">
        <div className="sf-row"><span className="dot" /><span>Fuente · <b>CSV local</b></span></div>
        <div className="sf-row" style={{ paddingLeft: 15 }}>notebooks/customer_analytics.csv</div>
        <div className="sf-row" style={{ marginTop: 6 }}>Validaciones · <b>14 / 14 OK</b></div>
        <div className="sf-row">Clientes · <b>5 750</b></div>
        <div className="sf-row">DWH · <b className="mono">dwh.customer_360</b></div>
      </div>
    </aside>
  );
}

function Topbar({ active }) {
  const page = PAGES.find(p => p.id === active);
  return (
    <div className="topbar">
      <div className="crumbs">
        Saleshealth  /  <b>{page.label}</b>
      </div>
      <div className="topbar-actions">
        <span className="chip"><span className="chip-dot" />Live · 2025-12-30</span>
        <span className="chip mono">build · 1.4.0</span>
      </div>
    </div>
  );
}

function resizeStreamlitFrame() {
  const root = document.getElementById('root');
  const app = document.querySelector('.app');
  const main = document.querySelector('.main');
  const height = Math.ceil(Math.max(
    document.documentElement.scrollHeight,
    document.body.scrollHeight,
    root ? root.scrollHeight : 0,
    app ? app.scrollHeight : 0,
    main ? main.scrollHeight : 0,
    window.innerHeight
  ));

  window.parent.postMessage(
    { isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height },
    '*'
  );
}

function App() {
  const [active, setActive] = React.useState('overview');
  const [customers, setCustomers] = React.useState(null);
  const [stats, setStats] = React.useState(null);
  const [recs, setRecs] = React.useState(null);

  React.useEffect(() => {
    setCustomers(window.__CUSTOMERS__);
    setStats(window.__STATS__);
    setRecs(window.__RECS__);
  }, []);

  React.useEffect(() => {
    window.requestAnimationFrame(() => {
      setTimeout(resizeStreamlitFrame, 40);
    });
  }, [active, customers, stats, recs]);

  if (!customers || !stats || !recs) {
    return (
      <div style={{ padding: 40, color: '#8b96a5' }}>Cargando dashboard…</div>
    );
  }

  return (
    <div className="app">
      <Sidebar active={active} onChange={setActive} />
      <main className="main" data-screen-label={`0${PAGES.findIndex(p=>p.id===active)+1} ${PAGES.find(p=>p.id===active).label}`}>
        <Topbar active={active} />
        {active === 'overview' && <PageOverview stats={stats} />}
        {active === 'customer360' && <PageCustomer360 customers={customers} />}
        {active === 'segmentation' && <PageSegmentation stats={stats} customers={customers} />}
        {active === 'churn' && <PageChurn stats={stats} customers={customers} />}
        {active === 'basket' && <PageMarketBasket recs={recs} />}
        {active === 'quality' && <PageDataQuality />}
      </main>
    </div>
  );
}

const rootElement = document.getElementById('root');
ReactDOM.createRoot(rootElement).render(<App />);

window.addEventListener('load', () => setTimeout(resizeStreamlitFrame, 80));
window.addEventListener('resize', () => window.requestAnimationFrame(resizeStreamlitFrame));

if ('ResizeObserver' in window) {
  const resizeObserver = new ResizeObserver(() => {
    window.requestAnimationFrame(resizeStreamlitFrame);
  });
  resizeObserver.observe(document.body);
  if (rootElement) resizeObserver.observe(rootElement);
}

setTimeout(resizeStreamlitFrame, 120);
setInterval(resizeStreamlitFrame, 800);

</script>
</body>
</html>"""

components.html(DASHBOARD_HTML, height=1200, scrolling=False)
