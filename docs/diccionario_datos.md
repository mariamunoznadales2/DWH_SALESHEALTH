# Diccionario de datos del Data Warehouse

Este documento resume el esquema `dwh` creado para el proyecto. El modelo esta organizado como una constelacion de hechos: varias tablas de hechos comparten dimensiones comunes para analizar ventas, devoluciones e inventario.

## Dimensiones

### `dwh.dim_date`

Dimension calendario. Permite agrupar hechos por dia, mes, trimestre, ano, semana y fin de semana.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `date_key` | PK | Clave entera en formato `YYYYMMDD`. |
| `full_date` | Fecha | Fecha real. |
| `year` | Numero | Ano. |
| `quarter` | Numero | Trimestre. |
| `month` | Numero | Mes. |
| `month_name` | Texto | Nombre del mes. |
| `day` | Numero | Dia del mes. |
| `day_of_week` | Numero | Dia ISO de la semana. |
| `day_name` | Texto | Nombre del dia. |
| `week_of_year` | Numero | Semana del ano. |
| `is_weekend` | Booleano | Indica si es sabado o domingo. |

### `dwh.dim_customer`

Dimension de clientes. Es la base para CLTV, RFM y clustering.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `customer_key` | PK | Clave surrogate del DWH. |
| `customer_id` | Natural key | Identificador del cliente en la base original. |
| `first_name`, `last_name`, `last_name2` | Texto | Nombre y apellidos. |
| `full_name` | Texto | Nombre completo unificado. |
| `email` | Texto | Correo del cliente. |
| `phone` | Texto | Telefono. |
| `created_at` | Fecha/hora | Fecha de alta. |

### `dwh.dim_product`

Dimension de producto. Une el producto comercial con informacion del catalogo central cuando existe.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `product_key` | PK | Clave surrogate del DWH. |
| `product_id` | Natural key | Identificador del producto original. |
| `product_name` | Texto | Nombre del producto. |
| `product_category` | Texto | Categoria comercial original. |
| `manufacturer` | Texto | Fabricante. |
| `sale_price` | Importe | Precio de venta original. |
| `central_category_id`, `central_category_name` | Categoria | Categoria en catalogo central. |
| `brand_id`, `brand_name`, `brand_country` | Marca | Informacion de marca. |
| `sku`, `barcode` | Texto | Codigos de catalogo central. |
| `unit_cost` | Importe | Coste unitario original del catalogo central. Puede ser nulo si falta informacion. |
| `analytic_unit_cost` | Importe | Coste unitario usado para margen. Si falta coste original, se imputa como 60% del precio de venta. |
| `cost_source` | Texto | Origen del coste: `CENTRAL_PRODUCT` o `IMPUTED_60_PCT_PRICE`. |
| `is_cost_imputed` | Booleano | Indica si el coste fue imputado por una regla analitica. |
| `central_unit_price` | Importe | Precio de catalogo central. |
| `created_at` | Fecha/hora | Fecha de creacion del producto. |

### `dwh.dim_store`

Dimension de tienda. Permite analizar ventas e inventario por ubicacion.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `store_key` | PK | Clave surrogate del DWH. |
| `store_id` | Natural key | Identificador de tienda original. |
| `store_name` | Texto | Nombre de la tienda. |
| `address`, `city`, `postal_code` | Texto | Localizacion. |
| `district`, `area_type`, `zone_orientation` | Texto | Enriquecimiento territorial desde `city_zone`. |
| `latitude`, `longitude` | Coordenadas | Geolocalizacion. |
| `opened_date` | Fecha | Fecha de apertura. |

### `dwh.dim_offer`

Dimension de ofertas. Incluye un registro tecnico `Sin oferta` para ventas sin promocion.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `offer_key` | PK | Clave surrogate del DWH. |
| `offer_id` | Natural key | Identificador de oferta original. |
| `offer_name` | Texto | Nombre de la oferta. |
| `description` | Texto | Descripcion. |
| `discount_percent` | Porcentaje | Descuento aplicado. |
| `start_date`, `end_date` | Fecha | Vigencia. |
| `is_no_offer` | Booleano | Marca el registro tecnico sin oferta. |

### `dwh.dim_return_reason`

Dimension de motivos de devolucion. Incluye un registro tecnico para motivo no informado.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `return_reason_key` | PK | Clave surrogate del DWH. |
| `reason_id` | Natural key | Identificador original. |
| `reason` | Texto | Motivo de devolucion. |
| `active` | Booleano | Indica si el motivo esta activo. |
| `is_unknown` | Booleano | Marca el registro tecnico desconocido. |

### `dwh.dim_warehouse`

Dimension de almacenes centrales.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `warehouse_key` | PK | Clave surrogate del DWH. |
| `warehouse_id` | Natural key | Identificador original del almacen. |
| `warehouse_name` | Texto | Nombre del almacen. |
| `address`, `city`, `postal_code` | Texto | Localizacion. |
| `latitude`, `longitude` | Coordenadas | Geolocalizacion. |

### `dwh.dim_warehouse_location`

Dimension de ubicaciones internas de almacen.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `warehouse_location_key` | PK | Clave surrogate del DWH. |
| `location_id` | Natural key | Identificador original de ubicacion. |
| `warehouse_key` | FK | Relacion con `dwh.dim_warehouse`. |
| `zone`, `aisle`, `shelf`, `bin_code` | Texto | Posicion fisica dentro del almacen. |

## Tablas de hechos

### `dwh.fact_sales`

Hecho principal de ventas, a nivel de linea de ticket.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `sales_key` | PK | Clave surrogate del hecho. |
| `sale_item_id` | Natural key | Linea de venta original. |
| `sale_id` | Degenerate dimension | Ticket de venta. |
| `date_key` | FK | Fecha de venta. |
| `customer_key` | FK | Cliente comprador. |
| `product_key` | FK | Producto vendido. |
| `store_key` | FK | Tienda. |
| `offer_key` | FK | Oferta aplicada o sin oferta. |
| `quantity` | Medida | Unidades vendidas. |
| `unit_price` | Medida | Precio unitario. |
| `subtotal` | Medida | Importe de la linea. |
| `sale_total` | Medida | Total del ticket original. |
| `estimated_unit_cost` | Medida | Coste unitario estimado. |
| `cost_source` | Texto | Origen del coste utilizado. |
| `is_cost_imputed` | Booleano | Marca lineas con coste imputado. |
| `estimated_total_cost` | Medida | Coste total estimado. |
| `gross_margin_amount` | Medida | Margen bruto estimado. |
| `gross_margin_percent` | Medida | Porcentaje de margen bruto. |

### `dwh.fact_returns`

Hecho de devoluciones, conectado con la venta original.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `returns_key` | PK | Clave surrogate del hecho. |
| `return_id` | Natural key | Devolucion original. |
| `sale_item_id`, `sale_id` | Referencia operacional | Venta y linea devuelta. |
| `date_key` | FK | Fecha de devolucion. |
| `customer_key` | FK | Cliente asociado. |
| `product_key` | FK | Producto devuelto. |
| `store_key` | FK | Tienda de la venta. |
| `return_reason_key` | FK | Motivo de devolucion. |
| `quantity_returned` | Medida | Unidades devueltas. |
| `returned_amount` | Medida | Importe devuelto estimado. |
| `cost_source` | Texto | Origen del coste utilizado. |
| `is_cost_imputed` | Booleano | Marca devoluciones con coste imputado. |
| `estimated_return_cost` | Medida | Coste estimado de la devolucion. |
| `estimated_margin_lost` | Medida | Margen perdido estimado. |

### `dwh.fact_store_inventory`

Hecho de inventario en tienda.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `store_inventory_key` | PK | Clave surrogate del hecho. |
| `inventory_id` | Natural key | Registro original de inventario. |
| `date_key` | FK | Fecha de actualizacion. |
| `store_key` | FK | Tienda. |
| `product_key` | FK | Producto. |
| `stock` | Medida | Unidades disponibles. |
| `cost_source` | Texto | Origen del coste utilizado. |
| `is_cost_imputed` | Booleano | Marca stock valorado con coste imputado. |
| `estimated_stock_cost` | Medida | Coste estimado del stock. |
| `estimated_stock_value` | Medida | Valor estimado del stock. |

### `dwh.fact_central_inventory`

Hecho de inventario en almacen central.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `central_inventory_key` | PK | Clave surrogate del hecho. |
| `inventory_id` | Natural key | Registro original de inventario central. |
| `date_key` | FK | Fecha de actualizacion. |
| `warehouse_key` | FK | Almacen. |
| `warehouse_location_key` | FK | Ubicacion dentro del almacen. |
| `product_key` | FK | Producto. |
| `quantity` | Medida | Unidades disponibles. |
| `min_stock`, `max_stock` | Medida | Umbrales de stock. |
| `cost_source` | Texto | Origen del coste utilizado. |
| `is_cost_imputed` | Booleano | Marca stock central valorado con coste imputado. |
| `estimated_stock_cost` | Medida | Coste estimado del stock. |
| `estimated_stock_value` | Medida | Valor estimado del stock. |

## Tablas analiticas derivadas

### `dwh.customer_metrics`

Tabla agregada por cliente. Contiene ingresos, margen, frecuencia, recencia, devoluciones, CLTV y scoring de churn.

Campos destacados:

- `churn_risk_score`: puntuacion de 0 a 100.
- `churn_risk_level`: nivel `Bajo`, `Medio`, `Alto` o `Critico`.
- `recommended_action`: accion comercial sugerida.

### `dwh.customer_rfm`

Tabla de segmentacion RFM. Clasifica clientes por recencia, frecuencia y valor monetario.

### `dwh.v_customer_analytics`

Vista final usada por el notebook. Une `customer_metrics` y `customer_rfm` para exportar un dataset plano de clientes.

### `dwh.customer_clusters`

Tabla con la asignacion de clustering generada por `scripts/build_customer_clusters.py`.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `customer_id` | PK/FK | Cliente asignado al cluster. |
| `cluster_id` | Numero | Identificador del cluster K-Means. |
| `cluster_name` | Texto | Interpretacion de negocio del cluster. |
| `pca_1`, `pca_2` | Numero | Coordenadas de visualizacion PCA. |
| `cluster_distance` | Numero | Distancia al centroide asignado. |
| `loaded_at` | Fecha/hora | Fecha de carga en el DWH. |

### `dwh.customer_360`

Vista mart final con una fila por cliente. Integra metricas CLTV/RFM, churn risk, recomendacion comercial y cluster.

Campos funcionales principales:

- identificacion del cliente
- primera y ultima compra
- ingresos y margen
- devoluciones
- CLTV historico y estimado
- RFM
- churn risk
- cluster K-Means
- coordenadas PCA
- accion recomendada

### `dwh.product_affinity`

Tabla de afinidad producto-producto generada por `sql/06_market_basket.sql`.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `product_affinity_key` | PK | Clave surrogate de la regla. |
| `product_a_key`, `product_b_key` | FK | Productos del par. |
| `product_a_id`, `product_b_id` | Natural key | Identificadores origen de los productos. |
| `product_a_name`, `product_b_name` | Texto | Nombres de productos. |
| `baskets_together` | Medida | Numero de tickets donde aparecen juntos. |
| `baskets_a`, `baskets_b` | Medida | Tickets donde aparece cada producto. |
| `total_baskets` | Medida | Total de tickets analizados. |
| `support` | Ratio | Proporcion de tickets con el par. |
| `confidence_a_to_b`, `confidence_b_to_a` | Ratio | Probabilidad direccional de recomendacion. |
| `lift` | Ratio | Fuerza de asociacion frente a independencia. |
| `avg_basket_revenue` | Importe | Ingreso medio de tickets donde aparece el par. |
| `recommendation_rank` | Numero | Ranking inicial por producto A. |

### `dwh.product_recommendations`

Tabla direccional de recomendaciones producto-producto. Incluye las mejores recomendaciones por producto con `lift > 1`.

| Campo | Tipo logico | Descripcion |
|---|---|---|
| `product_key` | FK | Producto base. |
| `recommended_product_key` | FK | Producto recomendado. |
| `product_id`, `recommended_product_id` | Natural key | Identificadores origen. |
| `product_name`, `recommended_product_name` | Texto | Nombres de producto. |
| `confidence` | Ratio | Probabilidad de recomendar el producto destino. |
| `lift` | Ratio | Fuerza de asociacion. |
| `support` | Ratio | Soporte del par. |
| `baskets_together` | Medida | Tickets donde aparecen juntos. |
| `recommendation_rank` | Numero | Ranking de recomendacion por producto. |

## Artefactos analiticos exportados

| Archivo | Descripcion |
|---|---|
| `notebooks/customer_analytics.csv` | Export de `dwh.v_customer_analytics`. Sirve como dataset plano de cliente. |
| `notebooks/customer_clusters.csv` | Asignacion de cluster, nombre de cluster, coordenadas PCA y distancia al centroide. |
| `reports/figures/clientes_pca_clusters.png` | Figura de clientes proyectados en PCA y coloreados por cluster. |

## Notebooks relacionados

| Notebook | Uso |
|---|---|
| `00_test_conexion.ipynb` | Comprueba conexion a PostgreSQL. |
| `01_inventario_esquema.ipynb` | Documenta tablas y columnas origen. |
| `02_relaciones_implicitas.ipynb` | Valida relaciones implicitas y calidad. |
| `03_eda_negocio.ipynb` | EDA de ventas, devoluciones y productos. |
| `04_cltv_churn_customer360.ipynb` | Analisis de metricas de cliente y churn. |
| `05_pca_clustering.ipynb` | PCA y clustering desde CSVs. |
| `06_market_basket.ipynb` | Afinidad producto-producto y recomendaciones. |
| `analisis_clientes.ipynb` | Resumen ejecutivo final. |
