# Saleshealth Customer Intelligence

Proyecto Final - Gestión de Datos - Data Warehouse, Customer 360, CLTV/RFM, churn, clustering, Market Basket y dashboard Streamlit.

Dashboard interactivo: [https://dwhsaleshealth-kytcsnxwhx3vl42ti7353a.streamlit.app/]

Este proyecto transforma la base operacional `saleshealth` en una plataforma analítica completa para estudiar clientes, ventas, margen, devoluciones, inventario y afinidad entre productos. La solución final incluye exploración del origen, Data Warehouse dimensional, ETL reproducible en SQL, control de calidad de datos, métricas de cliente, scoring de churn, clustering K-Means, Market Basket Analysis, mart `customer_360`, notebooks por fases, memoria final y dashboard ejecutivo.

## Resumen ejecutivo

La base original contiene ventas retail de productos de salud. El objetivo del proyecto es convertir esos datos transaccionales en informacion accionable para negocio: detectar clientes valiosos, priorizar recuperacion de clientes en riesgo, medir margen con trazabilidad, identificar patrones de devolucion y proponer recomendaciones producto-producto.

| Indicador | Resultado final |
|---|---:|
| Clientes analizados | 5 750 |
| Ventas originales | 20 000 |
| Líneas de venta | 42 555 |
| Devoluciones | 2 330 |
| Ingresos netos | 9 402 367.86 |
| Margen neto estimado | 3 761 148.12 |
| Líneas con coste imputado trazado | 711 |
| Clientes con metricas, RFM y churn | 5 750 |
| Clientes con cluster asignado | 5 750 |
| Pares producto-producto analizados | 1 225 |
| Recomendaciones producto-producto | 235 |
| Validaciones finales | 14/14 OK |

## Hallazgos clave

| Hallazgo | Resultado |
|---|---:|
| Cluster de alto valor | 746 clientes y 3 443 624.24 de margen neto estimado |
| Cluster inactivo o en riesgo | 3 134 clientes, recencia media 1 064.89 dias |
| Cluster con más devoluciones | 401 clientes, tasa media de devolución 0.8986 |
| Clientes estrella RFM | 1 218 clientes |
| Valiosos en riesgo RFM | 726 clientes |
| Producto con coste faltante | Producto 29, 711 líneas y 1 426 unidades |
| Margen recuperado por imputación | 11 408.00 |
| Market Basket | 207 reglas significativas y 235 recomendaciones |
| Lift máximo detectado | 1.3921 |

## Arquitectura

```text
PostgreSQL - base operacional saleshealth
        |
        v
Exploracion del origen
ER, inventario, relaciones implícitas, calidad de datos
        |
        v
Data Warehouse dimensional - esquema dwh
8 dimensiones + 4 hechos
        |
        v
Métricas de cliente
CLTV + RFM + churn risk + acciones recomendadas
        |
        v
Clustering
PCA + K-Means + customer_clusters
        |
        v
Market Basket Analysis
product_affinity + product_recommendations
        |
        v
Mart final
dwh.customer_360
        |
        v
Dashboard Streamlit
app.py
```

## Modelo de datos final

El esquema analítico principal es `dwh`.

| Capa | Objetos |
|---|---|
| Dimensiones | `dim_date`, `dim_customer`, `dim_product`, `dim_store`, `dim_offer`, `dim_return_reason`, `dim_warehouse`, `dim_warehouse_location` |
| Hechos | `fact_sales`, `fact_returns`, `fact_store_inventory`, `fact_central_inventory` |
| Métricas | `customer_metrics`, `customer_rfm`, `customer_clusters`, `product_affinity`, `product_recommendations` |
| Vista analítica | `v_customer_analytics` |
| Mart final | `customer_360` |

El grano principal de `fact_sales` es una línea de venta (`sale_item_id`). Las devoluciones se modelan como hecho propio (`fact_returns`) y el inventario se conserva en hechos separados para tienda y almacén central.

## Decisiones de modelado y calidad

### Relaciones implícitas

El análisis del origen detecto relaciones no declaradas que se incorporan al DWH:

| Area | Hallazgo | Decision |
|---|---|---|
| Tiendas | `postal_code` permite cruzar con `city_zone` | `dim_store` enriquecida con distrito y area |
| Ofertas | Líneas sin `offer_id` | Registro técnico "Sin oferta" |
| Devoluciones | Motivo no informado | Registro técnico "Sin motivo" |
| Catálogo | Producto 29 sin coste | Coste analítico imputado y trazado |

### Coste imputado

El producto `product_id = 29` aparece vendido, pero no tiene coste en `central_product`. Para no perder margen analítico, el DWH conserva el dato original y añade una imputación trazable:

```text
analytic_unit_cost = sale_price * 0.60
cost_source = IMPUTED_60_PCT_PRICE
is_cost_imputed = true
```

Impacto:

| Producto | Líneas | Unidades | Ingresos afectados | Coste imputado | Margen recuperado |
|---|---:|---:|---:|---:|---:|
| Sensor temperatura inteligente | 711 | 1 426 | 28 505.74 | 17 097.74 | 11 408.00 |

## Analítica de cliente

### CLTV, RFM y churn

`dwh.customer_metrics` y `dwh.customer_360` incorporan:

- fechas de primera y última compra
- ingresos brutos y netos
- margen neto estimado
- devoluciones y tasa de devolución
- CLTV histórico por ingresos
- CLTV histórico por margen
- CLTV estimado a 12 meses
- RFM score y segmento comercial
- `churn_risk_score`
- `churn_risk_level`
- `recommended_action`

El scoring de churn combina recencia, frecuencia mensual, tasa de devolución y valor histórico por margen. No sustituye a RFM: lo complementa para priorizar acciones.

| Nivel de churn | Uso comercial |
|---|---|
| Bajo | Seguimiento normal |
| Medio | Atención comercial |
| Alto | Campaña de reactivación |
| Critico | Recuperación prioritaria |

### Clustering K-Means

El clustering se genera con `scripts/build_customer_clusters.py` a partir de `notebooks/customer_analytics.csv`. El script crea:

- `notebooks/customer_clusters.csv`
- `reports/figures/clientes_pca_clusters.png`

Despues, `sql/05_load_customer_clusters.sql` carga los resultados en PostgreSQL e integra los clusters en `dwh.customer_360`.

| Cluster | Interpretacion | Clientes | Margen neto estimado | Churn medio |
|---:|---|---:|---:|---:|
| 0 | Clientes recientes con potencial | 1 469 | 110 890.52 | 20.51 |
| 1 | Clientes de alto valor | 746 | 3 443 624.24 | 32.10 |
| 2 | Clientes inactivos o en riesgo | 3 134 | 202 437.04 | 62.72 |
| 3 | Clientes con más devoluciones | 401 | 4 196.32 | 67.59 |

## Market Basket Analysis

La ampliación final implementa afinidad producto-producto sobre tickets de venta. El objetivo es detectar productos que se compran juntos para diseñar packs, promociones cruzadas y recomendaciones comerciales.

Objetos generados:

- `dwh.product_affinity`: pares de productos con `support`, `confidence` y `lift`.
- `dwh.product_recommendations`: recomendaciones direccionales producto base -> producto recomendado.

| Metrica | Interpretación |
|---|---|
| `support` | Porcentaje de tickets donde aparece el par |
| `confidence` | Probabilidad de comprar B dado que se compra A |
| `lift` | Fuerza de asociación frente al azar; `lift > 1` indica asociación positiva |

Resultado:

| Indicador | Valor |
|---|---:|
| Pares producto-producto | 1 225 |
| Reglas con `lift > 1` y 10+ tickets | 207 |
| Recomendaciones generadas | 235 |
| Lift máximo | 1.3921 |

## Dashboard Streamlit

El dashboard final esta implementado en `app.py`. Usa una estética oscura de tipo clínico/médico y funciona con CSVs versionados, por lo que puede abrirse sin tener PostgreSQL activo.

Fuentes del dashboard:

- `notebooks/customer_analytics.csv`
- `notebooks/customer_clusters.csv`
- `notebooks/product_recommendations.csv`

Vistas del dashboard:

| Pagina | Contenido |
|---|---|
| 01. Resumen ejecutivo | KPIs, margen, RFM, churn y lectura ejecutiva |
| 02. Customer 360 | Buscador de cliente y ficha individual |
| 03. Segmentacion | RFM, clusters y visualizacion PCA |
| 04. Churn | Clientes en riesgo, niveles y acciones |
| 05. Market Basket | Recomendaciones producto-producto y métricas MBA |
| 06. Calidad de datos | Validaciones y caso del producto 29 |

Ejecutar:

```bash
source venv/bin/activate
streamlit run app.py
```

URL local por defecto:

```text
http://localhost:8501
```

## Pipeline exacto

El pipeline automatizado esta en `scripts/run_pipeline.sh`.

```bash
scripts/run_pipeline.sh
```

Por defecto usa la base `saleshealth`. Para otra base:

```bash
DB_NAME=otra_base scripts/run_pipeline.sh
```

Orden exacto de ejecucion:

| Paso | Script | Funcion |
|---:|---|---|
| 1 | `sql/01_crear_dwh.sql` | Crea el esquema `dwh`, dimensiones, hechos, métricas y marts |
| 2 | `sql/02_etl.sql` | Carga dimensiones y hechos desde la base operacional |
| 3 | `sql/03_metricas_cltv.sql` | Calcula métricas de cliente, CLTV, RFM, churn y `customer_360` |
| 4 | `scripts/build_customer_clusters.py` | Genera PCA, K-Means, CSV de clusters y figura |
| 5 | `sql/05_load_customer_clusters.sql` | Carga clusters en PostgreSQL e integra `customer_360` |
| 6 | `sql/06_market_basket.sql` | Calcula afinidad producto-producto y recomendaciones |
| 7 | `sql/04_validaciones_dwh.sql` | Ejecuta las 14 validaciones finales |

`sql/00_explorar_base_original.sql` queda como script de exploración inicial del origen y puede ejecutarse antes del pipeline si se quiere revisar el estado de la base.

## Instalación y ejecución desde cero

### 1. Crear entorno Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Restaurar la base operacional

El dump esta en `saleshealthBackupGD.sql` y es un dump custom de PostgreSQL.

```bash
createdb saleshealth
pg_restore -d saleshealth --no-owner --no-privileges saleshealthBackupGD.sql
```

Si la base ya existe:

```bash
dropdb saleshealth
createdb saleshealth
pg_restore -d saleshealth --no-owner --no-privileges saleshealthBackupGD.sql
```

### 3. Ejecutar el pipeline completo

```bash
scripts/run_pipeline.sh
```

### 4. Abrir el dashboard

```bash
streamlit run app.py
```

## Ejecución manual

```bash
psql -d saleshealth -f sql/00_explorar_base_original.sql
psql -d saleshealth -f sql/01_crear_dwh.sql
psql -d saleshealth -f sql/02_etl.sql
psql -d saleshealth -f sql/03_metricas_cltv.sql
venv/bin/python scripts/build_customer_clusters.py
psql -d saleshealth -f sql/05_load_customer_clusters.sql
psql -d saleshealth -f sql/06_market_basket.sql
psql -d saleshealth -f sql/04_validaciones_dwh.sql
```

Para regenerar el CSV analítico desde PostgreSQL:

```bash
psql -d saleshealth -c "\\copy (select * from dwh.v_customer_analytics) to 'notebooks/customer_analytics.csv' with (format csv, header true, encoding 'UTF8')"
```

## Notebooks

Los notebooks documentan el proyecto por fases. Los primeros notebooks se apoyan en PostgreSQL; los ultimos pueden reutilizar los CSVs versionados.

| Notebook | Objetivo |
|---|---|
| `00_test_conexion.ipynb` | Comprueba conexión Python-PostgreSQL y disponibilidad de esquemas |
| `01_inventario_esquema.ipynb` | Inventaria tablas, columnas, claves y volumen del esquema origen |
| `02_relaciones_implicitas.ipynb` | Valida relaciones no evidentes y problemas de calidad |
| `03_eda_negocio.ipynb` | Analiza ventas, devoluciones, productos y concentración de ingresos |
| `04_cltv_churn_customer360.ipynb` | Explora CLTV, RFM, churn risk y acciones recomendadas |
| `05_pca_clustering.ipynb` | Analiza PCA y clusters sobre los CSVs versionados |
| `06_market_basket.ipynb` | Analiza afinidad producto-producto, support, confidence y lift |
| `analisis_clientes.ipynb` | Resumen ejecutivo final sin repetir todo el desarrollo metodológico |

Abrir notebooks:

```bash
source venv/bin/activate
jupyter notebook
```

Regenerar notebooks desde el script generador:

```bash
venv/bin/python scripts/create_analysis_notebooks.py
```

## Validaciones

`sql/04_validaciones_dwh.sql` comprueba:

- volumen de tablas frente al origen
- claves dimensionales obligatorias
- completitud de `customer_360`
- metricas para los 5 750 clientes
- churn score en rango
- RFM en rango
- CLTV no negativo
- clusters para todos los clientes
- reglas de Market Basket con `lift > 1`
- recomendaciones producto-producto
- trazabilidad de las 711 lineas con coste imputado

Resultado esperado:

```text
14 controles OK / 0 controles REVISAR
```

## Estructura del proyecto

```text
.
├── README.md
├── MEMORIA.tex
├── MEMORIA.pdf
├── GD_ProyectoFinal.pdf
├── saleshealthBackupGD.sql
├── requirements.txt
├── app.py
├── data/
│   ├── raw/
│   └── processed/
├── diagrams/
│   ├── modelos.drawio
│   ├── modelo_er_original.png
│   └── modelo_dimensional_dwh.png
├── docs/
│   ├── analisis_base_original.md
│   ├── conclusiones_ejecutivas.md
│   ├── diccionario_datos.md
│   ├── fases_proyecto.md
│   └── memoria_proyecto.md
├── notebooks/
│   ├── 00_test_conexion.ipynb
│   ├── 01_inventario_esquema.ipynb
│   ├── 02_relaciones_implicitas.ipynb
│   ├── 03_eda_negocio.ipynb
│   ├── 04_cltv_churn_customer360.ipynb
│   ├── 05_pca_clustering.ipynb
│   ├── 06_market_basket.ipynb
│   ├── analisis_clientes.ipynb
│   ├── customer_analytics.csv
│   ├── customer_clusters.csv
│   └── product_recommendations.csv
├── reports/
│   └── figures/
│       └── clientes_pca_clusters.png
├── scripts/
│   ├── build_customer_clusters.py
│   ├── create_analysis_notebooks.py
│   └── run_pipeline.sh
└── sql/
    ├── 00_explorar_base_original.sql
    ├── 01_crear_dwh.sql
    ├── 02_etl.sql
    ├── 03_metricas_cltv.sql
    ├── 04_validaciones_dwh.sql
    ├── 05_load_customer_clusters.sql
    └── 06_market_basket.sql
```

## Consultas útiles

Top clientes por margen:

```sql
select customer_id, full_name, margen_neto_estimado, churn_risk_level, segmento_rfm
from dwh.customer_360
order by margen_neto_estimado desc
limit 10;
```

Clientes con riesgo alto o crítico:

```sql
select customer_id, full_name, recencia_dias, margen_neto_estimado,
       churn_risk_score, churn_risk_level, recommended_action
from dwh.customer_360
where churn_risk_level in ('Critico', 'Alto')
order by churn_risk_score desc, margen_neto_estimado desc;
```

Perfil de clusters:

```sql
select cluster_id, cluster_name, count(*) as clientes,
       round(sum(margen_neto_estimado)::numeric, 2) as margen,
       round(avg(churn_risk_score)::numeric, 2) as churn_medio
from dwh.customer_360
group by cluster_id, cluster_name
order by margen desc;
```

Top recomendaciones producto-producto:

```sql
select product_name, recommended_product_name, baskets_together,
       confidence, lift, support
from dwh.product_recommendations
order by lift desc, confidence desc
limit 10;
```

## Entregables finales

| Entregable | Archivo |
|---|---|
| Memoria final | `MEMORIA.pdf` |
| Dashboard | `app.py` |
| Pipeline SQL/Python | `scripts/run_pipeline.sh` + carpeta `sql/` |
| Notebooks de analisis | carpeta `notebooks/` |
| Diagramas | carpeta `diagrams/` |
| Figura PCA/clustering | `reports/figures/clientes_pca_clusters.png` |

## Valor diferencial

El proyecto no se limita a consultas SQL aisladas. Aporta una cadena completa de datos a decisión:

- análisis documentado de la base original
- modelo ER y modelo dimensional
- ETL SQL reproducible
- control de calidad de datos con imputación trazable
- CLTV histórico y estimado
- segmentación RFM
- scoring de churn
- PCA y K-Means integrados en PostgreSQL
- Market Basket Analysis para recomendaciones y packs
- mart `customer_360`
- validaciones automáticas 14/14 OK
- dashboard Streamlit final para defensa
