# Fases del Proyecto Final

Este documento resume el flujo real del proyecto despues de las mejoras: Data Warehouse, metricas de cliente, churn, clustering integrado, Market Basket Analysis, validaciones y notebooks por fases.

## Fase 0 - Preparacion del entorno

Objetivo: dejar PostgreSQL y Python listos para ejecutar el proyecto.

Archivos relacionados:

- `saleshealthBackupGD.sql`
- `requirements.txt`
- `scripts/run_pipeline.sh`
- `notebooks/00_test_conexion.ipynb`

Tareas:

- Crear la base `saleshealth`.
- Restaurar el backup original.
- Crear y activar el entorno virtual.
- Instalar dependencias Python.
- Validar la conexion desde Python y `psql`.

Resultado:

La base operacional queda disponible y Python puede conectarse a PostgreSQL.

## Fase 1 - Inventario del esquema origen

Objetivo: entender las tablas fuente, columnas, tipos, claves y volumen.

Archivos relacionados:

- `sql/00_explorar_base_original.sql`
- `docs/analisis_base_original.md`
- `notebooks/01_inventario_esquema.ipynb`

Resultado validado:

| Elemento | Valor |
|---|---:|
| Tablas origen | 17 |
| Clientes | 5750 |
| Ventas | 20000 |
| Lineas de venta | 42555 |
| Devoluciones | 2330 |
| Productos | 50 |
| Tiendas | 20 |

## Fase 2 - Relaciones implicitas y calidad de datos

Objetivo: investigar relaciones utiles para el modelo analitico que no siempre aparecen como FK directas.

Archivos relacionados:

- `notebooks/02_relaciones_implicitas.ipynb`
- `docs/analisis_base_original.md`

Relaciones/decisiones detectadas:

- `store.postal_code` se enlaza con `city_zone.postal_code` usando los cinco primeros caracteres.
- Ventas sin oferta se normalizan con un registro tecnico `Sin oferta`.
- Devoluciones sin motivo se cubren con un registro tecnico `Sin motivo informado`.
- `product_id = 29` se vende, pero no tiene coste en `central_product`.

Resultado:

La incidencia del producto 29 se trata con coste imputado trazable en el DWH.

## Fase 3 - EDA de negocio

Objetivo: analizar ventas, devoluciones, productos y concentracion de ingresos antes de construir el DWH final.

Archivos relacionados:

- `notebooks/03_eda_negocio.ipynb`
- `docs/conclusiones_ejecutivas.md`

Analisis incluidos:

- Evolucion mensual de ingresos.
- Top productos.
- Motivos de devolucion.
- Concentracion de ingresos por cliente.

Resultado:

El analisis exploratorio confirma que el proyecto debe centrarse en cliente, margen, devoluciones y valor historico.

## Fase 4 - Modelo Entidad-Relacion

Objetivo: documentar visualmente el modelo operacional.

Archivos relacionados:

- `diagrams/modelos.drawio`
- `diagrams/modelo_er_original.png`

Nucleo operacional:

```text
customer -> sale -> sale_item -> product
              |
            store

sale_item -> return_item -> return_reason
sale_item -> offer
```

Resultado:

Modelo ER disponible como diagrama editable y exportado en PNG.

## Fase 5 - Data Warehouse dimensional

Objetivo: crear un modelo dimensional para ventas, devoluciones e inventario.

Archivos relacionados:

- `sql/01_crear_dwh.sql`
- `diagrams/modelo_dimensional_dwh.png`
- `docs/diccionario_datos.md`

Modelo:

| Tipo | Objetos |
|---|---|
| Dimensiones | 8 dimensiones |
| Hechos | 4 tablas de hechos |
| Grano principal | 1 linea de venta = 1 `sale_item_id` |

Resultado:

Esquema `dwh` creado con claves surrogate, dimensiones compartidas y hechos separados.

## Fase 6 - ETL y calidad de margen

Objetivo: cargar el DWH desde la base operacional.

Archivo relacionado:

- `sql/02_etl.sql`

Mejora clave:

El producto `product_id = 29` no tiene coste original. El ETL conserva esa incidencia y crea:

- `analytic_unit_cost`
- `cost_source`
- `is_cost_imputed`

Regla aplicada:

```text
analytic_unit_cost = sale_price * 0.60
```

Impacto validado:

| Indicador | Valor |
|---|---:|
| Lineas con coste imputado | 711 |
| Unidades afectadas | 1426 |
| Ingresos afectados | 28505.74 |
| Margen estimado recuperado | 11408.00 |

## Fase 7 - CLTV, RFM, churn y Customer 360

Objetivo: construir la capa analitica de cliente.

Archivos relacionados:

- `sql/03_metricas_cltv.sql`
- `notebooks/04_cltv_churn_customer360.ipynb`

Objetos generados:

- `dwh.customer_metrics`
- `dwh.customer_rfm`
- `dwh.v_customer_analytics`
- `dwh.customer_360`

Metricas:

- ingresos brutos y netos
- margen bruto y neto estimado
- ticket medio
- recencia y frecuencia
- tasa de devolucion
- CLTV historico por ingresos y margen
- CLTV estimado a 12 meses
- RFM
- `churn_risk_score`
- `churn_risk_level`
- `recommended_action`

Resultado:

5750 clientes quedan con metricas, RFM y churn score.

## Fase 8 - PCA y clustering

Objetivo: segmentar clientes con tecnicas de reduccion dimensional y K-Means.

Archivos relacionados:

- `scripts/build_customer_clusters.py`
- `sql/05_load_customer_clusters.sql`
- `notebooks/05_pca_clustering.ipynb`
- `notebooks/customer_clusters.csv`
- `reports/figures/clientes_pca_clusters.png`

Resultado validado:

| Cluster | Interpretacion | Clientes |
|---:|---|---:|
| 0 | Clientes recientes con potencial | 1469 |
| 1 | Clientes de alto valor | 746 |
| 2 | Clientes inactivos o en riesgo | 3134 |
| 3 | Clientes con mas devoluciones | 401 |

Los clusters se cargan en `dwh.customer_clusters` y se integran en `dwh.customer_360`.

## Fase 9 - Market Basket Analysis

Objetivo: detectar productos comprados juntos para disenar recomendaciones, packs comerciales y promociones cruzadas.

Archivos relacionados:

- `sql/06_market_basket.sql`
- `notebooks/06_market_basket.ipynb`

Objetos generados:

- `dwh.product_affinity`
- `dwh.product_recommendations`

Resultado validado:

| Indicador | Valor |
|---|---:|
| Pares producto-producto | 1225 |
| Recomendaciones generadas | 235 |
| Reglas con `lift > 1` y minimo 10 tickets | 207 |
| Lift maximo | 1.3921 |

## Fase 10 - Validaciones reproducibles

Objetivo: comprobar que el DWH, las metricas y los marts finales son consistentes.

Archivo relacionado:

- `sql/04_validaciones_dwh.sql`

Controles:

- cargas contra tablas originales
- claves dimensionales nulas
- metricas para todos los clientes
- churn score informado
- clusters para todos los clientes
- `customer_360` completo
- reglas de Market Basket
- recomendaciones producto-producto
- coste imputado trazado

Resultado:

```text
14 controles OK / 0 controles REVISAR
```

## Fase 11 - Notebooks y documentacion final

Objetivo: dejar el proyecto defendible y reproducible.

Notebooks finales:

| Notebook | Funcion |
|---|---|
| `00_test_conexion.ipynb` | Test de conexion. |
| `01_inventario_esquema.ipynb` | Inventario del origen. |
| `02_relaciones_implicitas.ipynb` | Relaciones implicitas y calidad. |
| `03_eda_negocio.ipynb` | EDA de negocio. |
| `04_cltv_churn_customer360.ipynb` | CLTV, RFM, churn y customer 360. |
| `05_pca_clustering.ipynb` | PCA y clustering. |
| `06_market_basket.ipynb` | Afinidad de productos y recomendaciones. |
| `analisis_clientes.ipynb` | Resumen ejecutivo final. |

Documentos finales:

- `README.md`
- `docs/analisis_base_original.md`
- `docs/conclusiones_ejecutivas.md`
- `docs/diccionario_datos.md`
- `docs/memoria_proyecto.md`

## Siguiente fase

El dashboard queda como ultima capa visual del proyecto. La base tecnica ya esta preparada: `dwh.customer_360`, `notebooks/customer_analytics.csv` y `notebooks/customer_clusters.csv` contienen la informacion necesaria.
