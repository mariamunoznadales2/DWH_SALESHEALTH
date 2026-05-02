# Memoria tecnica del proyecto

## 1. Introduccion

Este proyecto construye una solucion analitica completa sobre la base operacional `saleshealth`, una base de ventas retail de productos de salud y bienestar. El objetivo es transformar registros transaccionales en informacion accionable para analizar clientes, ventas, margen, devoluciones, inventario y riesgo de abandono.

La solucion final incluye:

- Data Warehouse dimensional.
- ETL reproducible.
- Calculo de CLTV.
- Segmentacion RFM.
- Scoring de churn.
- Clustering K-Means con PCA.
- Market Basket Analysis.
- Mart final `dwh.customer_360`.
- Validaciones automaticas.
- Notebooks por fases para trazabilidad.

## 2. Base operacional

La base original contiene 17 tablas. Las mas relevantes para el proyecto son:

- `customer`
- `sale`
- `sale_item`
- `product`
- `central_product`
- `store`
- `return_item`
- `return_reason`
- `inventory`
- `central_inventory`

Resumen validado:

| Indicador | Valor |
|---|---:|
| Clientes | 5750 |
| Ventas | 20000 |
| Lineas de venta | 42555 |
| Devoluciones | 2330 |
| Productos | 50 |
| Tiendas | 20 |

El nucleo operacional es:

```text
customer -> sale -> sale_item -> product
              |
            store

sale_item -> return_item -> return_reason
sale_item -> offer
```

## 3. Modelo dimensional

Se disena un Data Warehouse en el esquema `dwh`, con modelo dimensional orientado a ventas, devoluciones e inventario.

Dimensiones:

- `dim_date`
- `dim_customer`
- `dim_product`
- `dim_store`
- `dim_offer`
- `dim_return_reason`
- `dim_warehouse`
- `dim_warehouse_location`

Hechos:

- `fact_sales`
- `fact_returns`
- `fact_store_inventory`
- `fact_central_inventory`

El grano principal es una linea de venta: cada fila de `fact_sales` representa un `sale_item_id`.

## 4. ETL

El ETL se implementa en `sql/02_etl.sql`. Carga dimensiones y hechos desde la base operacional.

Transformaciones principales:

- Generacion de dimension calendario.
- Enriquecimiento de tienda con zona geografica.
- Registro tecnico `Sin oferta`.
- Registro tecnico `Sin motivo informado`.
- Calculo de costes, margen y valor de stock.
- Tratamiento trazable de coste faltante.

## 5. Calidad de datos: producto 29

Se detecta que el producto `product_id = 29`, `Sensor temperatura inteligente`, aparece en ventas pero no existe correctamente en `central_product` con coste unitario.

Decision:

- Mantener `unit_cost` original como nulo.
- Crear `analytic_unit_cost` imputado como 60% del precio de venta.
- Marcar la trazabilidad con `cost_source = IMPUTED_60_PCT_PRICE`.
- Marcar `is_cost_imputed = true`.

Impacto:

| Indicador | Valor |
|---|---:|
| Lineas afectadas | 711 |
| Unidades afectadas | 1426 |
| Ingresos afectados | 28505.74 |
| Coste imputado total | 17097.74 |
| Margen estimado recuperado | 11408.00 |

## 6. Metricas de cliente

`sql/03_metricas_cltv.sql` genera la capa de cliente:

- `dwh.customer_metrics`
- `dwh.customer_rfm`
- `dwh.v_customer_analytics`
- `dwh.customer_360`

Metricas calculadas:

- numero de compras
- unidades compradas y devueltas
- ingresos brutos, devueltos y netos
- margen bruto y neto estimado
- ticket medio
- antiguedad y recencia
- frecuencia mensual y anual
- tasa de devolucion
- CLTV historico
- CLTV estimado a 12 meses
- RFM
- churn risk
- accion recomendada

## 7. Churn risk

El scoring de churn combina:

- recencia
- frecuencia mensual
- tasa de devolucion
- valor historico por margen

Campos generados:

- `churn_risk_score`
- `churn_risk_level`
- `recommended_action`

Niveles:

| Nivel | Interpretacion |
|---|---|
| Bajo | Seguimiento normal. |
| Medio | Atencion comercial. |
| Alto | Campana de reactivacion. |
| Critico | Recuperacion prioritaria. |

## 8. Clustering

El clustering se genera con `scripts/build_customer_clusters.py` usando las metricas del cliente.

Salida:

- `notebooks/customer_clusters.csv`
- `reports/figures/clientes_pca_clusters.png`
- `dwh.customer_clusters`

Resultado:

| Cluster | Interpretacion | Clientes | Churn medio |
|---:|---|---:|---:|
| 0 | Clientes recientes con potencial | 1469 | 20.51 |
| 1 | Clientes de alto valor | 746 | 32.10 |
| 2 | Clientes inactivos o en riesgo | 3134 | 62.72 |
| 3 | Clientes con mas devoluciones | 401 | 67.59 |

## 9. Market Basket Analysis

La ampliacion de Market Basket detecta afinidades producto-producto a partir de tickets de venta.

Archivo:

- `sql/06_market_basket.sql`

Objetos:

- `dwh.product_affinity`
- `dwh.product_recommendations`

Metricas:

- `support`: proporcion de tickets que contienen el par.
- `confidence`: probabilidad de recomendar un producto dado otro.
- `lift`: fuerza de asociacion frente a la compra esperada por azar.

Resultado:

| Indicador | Valor |
|---|---:|
| Pares producto-producto | 1225 |
| Recomendaciones | 235 |
| Reglas con `lift > 1` y minimo 10 tickets | 207 |
| Lift maximo | 1.3921 |

Esta capa permite proponer packs, recomendaciones y promociones cruzadas.

## 10. Validaciones

`sql/04_validaciones_dwh.sql` ejecuta controles sobre el resultado final.

Resultado:

```text
14 controles OK / 0 controles REVISAR
```

Controles principales:

- cargas coinciden con origen
- claves dimensionales no nulas
- metricas para todos los clientes
- churn score para todos los clientes
- clusters para todos los clientes
- `customer_360` completo
- reglas de Market Basket
- recomendaciones producto-producto
- coste imputado trazado

## 11. Notebooks

El trabajo se documenta con notebooks por fases:

| Notebook | Funcion |
|---|---|
| `00_test_conexion.ipynb` | Test de conexion. |
| `01_inventario_esquema.ipynb` | Inventario del esquema origen. |
| `02_relaciones_implicitas.ipynb` | Relaciones implicitas y calidad. |
| `03_eda_negocio.ipynb` | EDA de negocio. |
| `04_cltv_churn_customer360.ipynb` | Analisis de CLTV, RFM, churn y customer 360. |
| `05_pca_clustering.ipynb` | PCA y clustering. |
| `06_market_basket.ipynb` | Market Basket Analysis. |
| `analisis_clientes.ipynb` | Resumen ejecutivo final. |

## 12. Conclusiones

La solucion permite convertir datos operacionales en una herramienta analitica orientada a decisiones. El negocio puede:

- identificar clientes de mayor valor
- priorizar recuperacion de clientes en riesgo
- detectar patrones de devolucion
- medir margen con trazabilidad
- segmentar clientes con RFM y clustering
- recomendar productos y disenar packs con afinidad historica
- consultar una vision 360 de cada cliente

El dashboard queda como siguiente paso natural, usando `dwh.customer_360` y los CSVs versionados como fuente.
