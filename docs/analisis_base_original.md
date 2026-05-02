# Fase 2 - Analisis de la base original

## Objetivo

El objetivo de esta fase es entender la base de datos operacional restaurada desde el backup `saleshealthBackupGD.sql`. Esta base representa la actividad de una empresa que vende productos de salud y bienestar.

La base restaurada en PostgreSQL se llama:

```text
saleshealth
```

## Resumen de datos

La base contiene 17 tablas principales.

| Tabla | Filas | Significado |
|---|---:|---|
| `brand` | 29 | Marcas de productos del catalogo central. |
| `category` | 6 | Categorias de productos del catalogo central. |
| `central_inventory` | 49 | Stock de productos en el almacen central. |
| `central_product` | 49 | Catalogo central de productos con coste, precio, marca y categoria. |
| `city_zone` | 42 | Zonas geograficas por codigo postal en Madrid. |
| `customer` | 5750 | Clientes. |
| `inventory` | 1000 | Stock de productos por tienda. |
| `offer` | 1 | Ofertas/promociones. |
| `product` | 50 | Productos vendidos en tiendas. |
| `product_offer` | 6 | Relacion entre productos y ofertas. |
| `return_item` | 2330 | Devoluciones de lineas de venta. |
| `return_reason` | 6 | Motivos de devolucion. |
| `sale` | 20000 | Cabecera de ventas. |
| `sale_item` | 42555 | Lineas de venta, es decir, productos incluidos en cada venta. |
| `store` | 20 | Tiendas. |
| `warehouse` | 1 | Almacen central. |
| `warehouse_location` | 40 | Ubicaciones internas del almacen. |

## Periodo y volumen de ventas

La tabla `sale` contiene ventas entre:

```text
Primera venta: 2020-01-01
Ultima venta: 2025-12-30
```

Metricas generales:

| Metrica | Valor |
|---|---:|
| Ventas | 20000 |
| Lineas de venta | 42555 |
| Ingresos totales | 9678681.67 |
| Ticket medio | 483.93 |

La tabla `return_item` contiene devoluciones entre:

```text
Primera devolucion: 2020-01-09
Ultima devolucion: 2026-02-07
```

Total de unidades devueltas:

```text
2330
```

## Tablas principales para el proyecto

### `customer`

Contiene los clientes. Sera una tabla clave para calcular metricas como CLTV, frecuencia de compra, ticket medio y segmentacion.

Columnas importantes:

- `customer_id`
- `first_name`
- `last_name`
- `email`
- `phone`
- `created_at`

### `sale`

Representa cada venta realizada. Es una cabecera de venta: indica que cliente compro, en que tienda, cuando y por cuanto total.

Columnas importantes:

- `sale_id`
- `customer_id`
- `store_id`
- `sale_date`
- `total`

### `sale_item`

Representa el detalle de cada venta. Una venta puede tener varios productos, por eso existe esta tabla.

Columnas importantes:

- `sale_item_id`
- `sale_id`
- `product_id`
- `quantity`
- `unit_price`
- `offer_id`
- `subtotal`

Esta tabla sera fundamental para analizar productos, cantidades, precios, descuentos y margenes.

### `product`

Contiene los productos vendidos en las tiendas.

Columnas importantes:

- `product_id`
- `name`
- `category`
- `manufacturer`
- `price`
- `created_at`

### `central_product`

Contiene una version mas completa del catalogo, incluyendo coste unitario y precio unitario. Es importante para calcular margen de beneficio.

Columnas importantes:

- `product_id`
- `name`
- `category_id`
- `brand_id`
- `sku`
- `barcode`
- `unit_cost`
- `unit_price`

### `store`

Contiene las tiendas donde se realizan ventas.

Columnas importantes:

- `store_id`
- `name`
- `address`
- `city`
- `postal_code`
- `latitude`
- `longitude`
- `opened_date`

### `return_item`

Contiene las devoluciones asociadas a lineas de venta.

Columnas importantes:

- `return_id`
- `sale_item_id`
- `return_date`
- `quantity`
- `reason_id`

### `return_reason`

Contiene los motivos de devolucion.

Columnas importantes:

- `reason_id`
- `reason`
- `active`

## Relaciones principales

Las relaciones mas importantes son:

```text
customer.customer_id -> sale.customer_id
store.store_id -> sale.store_id
sale.sale_id -> sale_item.sale_id
product.product_id -> sale_item.product_id
offer.offer_id -> sale_item.offer_id
sale_item.sale_item_id -> return_item.sale_item_id
```

Tambien hay relaciones de inventario y catalogo central:

```text
product.product_id -> inventory.product_id
store.store_id -> inventory.store_id
central_product.product_id -> central_inventory.product_id
brand.brand_id -> central_product.brand_id
category.category_id -> central_product.category_id
warehouse.warehouse_id -> warehouse_location.warehouse_id
warehouse_location.location_id -> central_inventory.location_id
```

## Relaciones implicitas y decisiones de modelado

Ademas de las claves principales, se detectaron relaciones y reglas utiles para el Data Warehouse:

| Area | Hallazgo | Decision en el DWH |
|---|---|---|
| Tiendas | `store.postal_code` se puede cruzar con `city_zone.postal_code` usando los cinco primeros caracteres. | Enriquecer `dim_store` con distrito, area y orientacion de zona. |
| Ofertas | Hay lineas de venta sin `offer_id`. | Crear registro tecnico `Sin oferta` en `dim_offer`. |
| Devoluciones | Puede faltar motivo informado. | Crear registro tecnico `Sin motivo informado` en `dim_return_reason`. |
| Catalogo | `product_id = 29` aparece vendido pero sin coste en `central_product`. | Mantener coste original nulo e imputar `analytic_unit_cost = sale_price * 0.60` con trazabilidad. |

Impacto del producto 29:

| Indicador | Valor |
|---|---:|
| Lineas de venta afectadas | 711 |
| Unidades vendidas afectadas | 1426 |
| Ingresos afectados | 28505.74 |
| Margen estimado recuperado por imputacion | 11408.00 |

## Lectura del modelo operacional

La base original esta pensada para registrar operaciones del negocio:

- Clientes que compran.
- Ventas realizadas.
- Productos incluidos en cada venta.
- Tiendas donde se vende.
- Promociones aplicadas.
- Devoluciones de productos.
- Inventario en tiendas y almacen central.

No esta optimizada para analisis directamente. Por eso el proyecto pide crear un Data Warehouse.

## Tablas que alimentaran el Data Warehouse

Para el modelo dimensional se usaran principalmente estas tablas fuente:

| Area | Tablas fuente |
|---|---|
| Clientes | `customer` |
| Ventas | `sale`, `sale_item` |
| Productos | `product`, `central_product`, `category`, `brand` |
| Tiendas | `store`, `city_zone` |
| Ofertas | `offer`, `product_offer` |
| Devoluciones | `return_item`, `return_reason` |
| Inventario | `inventory`, `central_inventory`, `warehouse`, `warehouse_location` |

La combinacion `sale` + `sale_item` tambien alimenta la ampliacion de Market Basket Analysis, ya que cada `sale_id` se interpreta como una cesta de compra y permite detectar productos comprados juntos.

## Primer diseno conceptual para el modelo ER

El nucleo del modelo es:

```text
customer -> sale -> sale_item -> product
              |
            store

sale_item -> return_item -> return_reason
sale_item -> offer
```

Este nucleo sera el mas importante para calcular CLTV, ya que el CLTV depende de ventas historicas, frecuencia de compra, ingresos y margen.

El mismo nucleo permite construir reglas de afinidad producto-producto, usando los productos que comparten un mismo `sale_id`.

## Conclusion de la fase

La base original contiene informacion suficiente para construir un entorno analitico. Las tablas clave para el proyecto son `customer`, `sale`, `sale_item`, `product`, `central_product`, `store`, `return_item` y `return_reason`.

El siguiente paso es crear el Modelo Entidad-Relacion y el Data Warehouse dimensional, incorporando desde el inicio las reglas anteriores para que la calidad de datos quede documentada y medible.

## Notebooks relacionados

La exploracion del origen queda documentada tambien en:

- `notebooks/00_test_conexion.ipynb`
- `notebooks/01_inventario_esquema.ipynb`
- `notebooks/02_relaciones_implicitas.ipynb`
- `notebooks/03_eda_negocio.ipynb`
- `notebooks/06_market_basket.ipynb`
