# Conclusiones ejecutivas

## Lectura general

El proyecto convierte la base operacional `saleshealth` en un sistema analitico capaz de responder preguntas de negocio sobre clientes, ventas, margen, devoluciones e inventario. La parte mas importante no es solo la carga del Data Warehouse, sino que el modelo permite pasar de registros transaccionales a decisiones accionables.

## Principales resultados

| Indicador | Resultado |
|---|---:|
| Clientes analizados | 5750 |
| Ventas originales | 20000 |
| Lineas de venta | 42555 |
| Devoluciones | 2330 |
| Ingresos netos | 9402367.86 |
| Margen neto estimado | 3761148.12 |
| Clientes estrella | 1218 |
| Clientes dormidos | 1057 |
| Clientes valiosos en riesgo | 726 |
| Clientes con churn score | 5750 |
| Clientes con cluster asignado | 5750 |
| Pares producto-producto analizados | 1225 |
| Recomendaciones producto-producto | 235 |
| Validaciones finales | 14/14 OK |

## Segmentos por clustering

| Cluster | Interpretacion | Clientes | Lectura de negocio |
|---:|---|---:|---|
| 0 | Clientes recientes con potencial | 1469 | Baja recencia y churn medio bajo; buenos candidatos para venta cruzada. |
| 1 | Clientes de alto valor | 746 | Principal fuente de margen; prioridad de fidelizacion. |
| 2 | Clientes inactivos o en riesgo | 3134 | Recencia media alta; requieren reactivacion selectiva. |
| 3 | Clientes con mas devoluciones | 401 | Tasa de devolucion muy alta; revisar experiencia, producto y motivos. |

## Market Basket Analysis

La ampliacion de Market Basket analiza productos comprados juntos en el mismo ticket. Sirve para recomendaciones, packs comerciales y promociones cruzadas.

| Indicador | Valor |
|---|---:|
| Pares de productos | 1225 |
| Recomendaciones generadas | 235 |
| Reglas con `lift > 1` | 207 |
| Lift maximo | 1.3921 |

## Acciones recomendadas

### 1. Proteger los clientes de mayor valor

Los `Clientes estrella` y el cluster de alto valor deben priorizarse en acciones de fidelizacion. Son clientes con mayor contribucion historica y mejor potencial de recurrencia.

Acciones propuestas:

- Ofertas personalizadas.
- Comunicaciones prioritarias.
- Programas de fidelizacion.
- Seguimiento de satisfaccion tras compra.

### 2. Reactivar clientes valiosos en riesgo

Los `Valiosos en riesgo` han generado valor, pero presentan peor recencia. Son especialmente interesantes porque ya han demostrado capacidad de compra.

Acciones propuestas:

- Campanas de recuperacion con incentivo limitado.
- Analisis de ultima categoria comprada.
- Recomendaciones de productos relacionados.
- Control de devoluciones previas para evitar repetir una mala experiencia.

### 3. Separar clientes dormidos de clientes no rentables

No todos los clientes inactivos tienen la misma prioridad. El proyecto permite distinguir clientes dormidos con bajo valor de clientes inactivos con buen margen historico.

Acciones propuestas:

- Reactivar solo los que tengan margen o CLTV suficiente.
- Evitar gastar presupuesto comercial en segmentos de bajo retorno.
- Usar RFM como primera regla de priorizacion.

### 4. Vigilar devoluciones

El analisis incorpora tasa de devolucion por importe y por unidades. Esto permite detectar clientes o productos con comportamiento anomalo de devolucion.

Acciones propuestas:

- Revisar productos con devoluciones recurrentes.
- Cruzar devoluciones con motivos (`dim_return_reason`).
- Separar problemas de calidad de problemas de expectativas.
- Ajustar fichas de producto o politicas comerciales si procede.

### 5. Mejorar calidad de datos del catalogo central

Se ha detectado una incidencia relevante: el producto `product_id = 29`, `Sensor temperatura inteligente`, aparece en ventas pero no existe en `central_product`. Para no perder trazabilidad, el DWH conserva el coste original nulo y anade un coste analitico imputado como el 60% del precio de venta.

Impacto:

- Los ingresos siguen siendo correctos.
- 711 lineas y 1426 unidades quedan marcadas con `is_cost_imputed = true`.
- El coste analitico imputado es 17097.74.
- El margen estimado recuperado es 11408.00.
- El CLTV por margen queda completo, pero trazado como estimacion en los clientes afectados.

Accion propuesta:

- Completar el producto en `central_product` con coste unitario, marca, categoria central, SKU y precio central.
- Reejecutar `scripts/run_pipeline.sh` para recalcular margen, CLTV, churn, clusters y validaciones.

## Valor diferencial del proyecto

El proyecto no se limita a crear tablas. Aporta una cadena analitica completa:

- Modelo Entidad-Relacion de la base original.
- Modelo dimensional del DWH.
- ETL reproducible.
- Metricas CLTV y RFM.
- Scoring de churn y accion recomendada por cliente.
- Control de devoluciones y margen.
- PCA y clustering integrado en `dwh.customer_clusters`.
- Market Basket Analysis integrado en `dwh.product_affinity` y `dwh.product_recommendations`.
- Mart final `dwh.customer_360`.
- Notebooks por fases para defender el proceso completo.
- Validaciones de calidad de datos con 14 controles OK.
- Diccionario de datos.
- Conclusiones orientadas a negocio.

## Notebooks de soporte

| Notebook | Aporta |
|---|---|
| `00_test_conexion.ipynb` | Evidencia de conexion y entorno. |
| `01_inventario_esquema.ipynb` | Inventario reproducible del origen. |
| `02_relaciones_implicitas.ipynb` | Justificacion de decisiones de modelado. |
| `03_eda_negocio.ipynb` | Lectura inicial de negocio. |
| `04_cltv_churn_customer360.ipynb` | Analisis de valor, RFM y churn. |
| `05_pca_clustering.ipynb` | Segmentacion con PCA y K-Means. |
| `06_market_basket.ipynb` | Afinidad de productos, support, confidence y lift. |
| `analisis_clientes.ipynb` | Resumen ejecutivo final. |

## Conclusion final

La solucion permite tomar decisiones sobre clientes con una base tecnica solida. El negocio puede identificar a quien fidelizar, a quien recuperar, donde se pierde margen y que problemas de datos deben corregirse para mejorar la fiabilidad del analisis.
