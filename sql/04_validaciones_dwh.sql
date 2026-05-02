-- Fase extra - Validaciones de calidad del Data Warehouse
-- Ejecutar despues de:
--   1) sql/01_crear_dwh.sql
--   2) sql/02_etl.sql
--   3) sql/03_metricas_cltv.sql
--   4) sql/05_load_customer_clusters.sql
--   5) sql/06_market_basket.sql
--
-- Objetivo: comprobar que el DWH esta cargado, que las claves principales
-- no tienen nulos, que las metricas cuadran y que las incidencias conocidas
-- quedan documentadas con impacto medible.

-- =========================
-- 1. Resumen de controles
-- =========================

with controles as (
    select
        'CARGA_DWH' as bloque,
        'dim_customer = customer original' as control,
        (select count(*) from dwh.dim_customer)::numeric as valor_obtenido,
        (select count(*) from customer)::numeric as valor_esperado,
        case
            when (select count(*) from dwh.dim_customer) = (select count(*) from customer)
            then 'OK' else 'REVISAR'
        end as estado
    union all
    select
        'CARGA_DWH',
        'fact_sales = sale_item original',
        (select count(*) from dwh.fact_sales)::numeric,
        (select count(*) from sale_item)::numeric,
        case
            when (select count(*) from dwh.fact_sales) = (select count(*) from sale_item)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'CARGA_DWH',
        'fact_returns = return_item original',
        (select count(*) from dwh.fact_returns)::numeric,
        (select count(*) from return_item)::numeric,
        case
            when (select count(*) from dwh.fact_returns) = (select count(*) from return_item)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'CARGA_DWH',
        'fact_store_inventory = inventory original',
        (select count(*) from dwh.fact_store_inventory)::numeric,
        (select count(*) from inventory)::numeric,
        case
            when (select count(*) from dwh.fact_store_inventory) = (select count(*) from inventory)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'CARGA_DWH',
        'fact_central_inventory = central_inventory original',
        (select count(*) from dwh.fact_central_inventory)::numeric,
        (select count(*) from central_inventory)::numeric,
        case
            when (select count(*) from dwh.fact_central_inventory) = (select count(*) from central_inventory)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'INTEGRIDAD',
        'fact_sales sin claves dimensionales nulas',
        (
            select count(*)
            from dwh.fact_sales
            where date_key is null
               or customer_key is null
               or product_key is null
               or store_key is null
               or offer_key is null
        )::numeric,
        0,
        case
            when (
                select count(*)
                from dwh.fact_sales
                where date_key is null
                   or customer_key is null
                   or product_key is null
                   or store_key is null
                   or offer_key is null
            ) = 0
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'INTEGRIDAD',
        'fact_returns sin claves dimensionales nulas',
        (
            select count(*)
            from dwh.fact_returns
            where date_key is null
               or customer_key is null
               or product_key is null
               or store_key is null
               or return_reason_key is null
        )::numeric,
        0,
        case
            when (
                select count(*)
                from dwh.fact_returns
                where date_key is null
                   or customer_key is null
                   or product_key is null
                   or store_key is null
                   or return_reason_key is null
            ) = 0
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'METRICAS',
        'clientes con metricas = clientes DWH',
        (select count(*) from dwh.customer_metrics)::numeric,
        (select count(*) from dwh.dim_customer)::numeric,
        case
            when (select count(*) from dwh.customer_metrics) = (select count(*) from dwh.dim_customer)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'METRICAS',
        'clientes con churn score informado',
        (select count(*) from dwh.customer_metrics where churn_risk_score is not null)::numeric,
        (select count(*) from dwh.dim_customer)::numeric,
        case
            when (select count(*) from dwh.customer_metrics where churn_risk_score is not null) = (select count(*) from dwh.dim_customer)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'MARTS',
        'customer_360 = clientes DWH',
        (select count(*) from dwh.customer_360)::numeric,
        (select count(*) from dwh.dim_customer)::numeric,
        case
            when (select count(*) from dwh.customer_360) = (select count(*) from dwh.dim_customer)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'MARTS',
        'customer_clusters = clientes DWH',
        (select count(*) from dwh.customer_clusters)::numeric,
        (select count(*) from dwh.dim_customer)::numeric,
        case
            when (select count(*) from dwh.customer_clusters) = (select count(*) from dwh.dim_customer)
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'MARTS',
        'product_affinity con reglas validas',
        (select count(*) from dwh.product_affinity where lift > 1 and baskets_together >= 10)::numeric,
        1,
        case
            when (select count(*) from dwh.product_affinity where lift > 1 and baskets_together >= 10) >= 1
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'MARTS',
        'product_recommendations con recomendaciones',
        (select count(*) from dwh.product_recommendations)::numeric,
        1,
        case
            when (select count(*) from dwh.product_recommendations) >= 1
            then 'OK' else 'REVISAR'
        end
    union all
    select
        'CALIDAD_DATOS',
        'lineas de venta con coste imputado trazado',
        (select count(*) from dwh.fact_sales where is_cost_imputed)::numeric,
        (
            select count(*)
            from sale_item si
            join product p on p.product_id = si.product_id
            left join central_product cp on cp.product_id = p.product_id
            where cp.unit_cost is null
        )::numeric,
        case
            when (select count(*) from dwh.fact_sales where is_cost_imputed) = (
                select count(*)
                from sale_item si
                join product p on p.product_id = si.product_id
                left join central_product cp on cp.product_id = p.product_id
                where cp.unit_cost is null
            )
            then 'OK' else 'REVISAR'
        end
)
select
    bloque,
    control,
    valor_obtenido,
    valor_esperado,
    estado
from controles
order by
    case estado when 'REVISAR' then 1 else 2 end,
    bloque,
    control;

-- =========================
-- 2. Incidencias de calidad de datos
-- =========================

-- Productos vendidos que no tienen coste en catalogo central.
-- Se imputa coste analitico = 60% del precio de venta y se conserva trazabilidad.
select
    dp.product_id,
    dp.product_name,
    dp.unit_cost as coste_original,
    dp.analytic_unit_cost as coste_analitico,
    dp.cost_source,
    count(*) as lineas_venta_coste_imputado,
    sum(fs.quantity) as unidades_vendidas,
    round(sum(fs.subtotal)::numeric, 2) as ingresos_afectados,
    round(sum(fs.estimated_total_cost)::numeric, 2) as coste_imputado_total,
    round(sum(fs.gross_margin_amount)::numeric, 2) as margen_estimado_recuperado
from dwh.fact_sales fs
join dwh.dim_product dp on dp.product_key = fs.product_key
where fs.is_cost_imputed
group by
    dp.product_id,
    dp.product_name,
    dp.unit_cost,
    dp.analytic_unit_cost,
    dp.cost_source
order by lineas_venta_coste_imputado desc;

-- =========================
-- 3. Resumen ejecutivo de metricas
-- =========================

select
    count(*) as clientes,
    round(sum(ingresos_netos)::numeric, 2) as ingresos_netos,
    round(sum(margen_neto_estimado)::numeric, 2) as margen_neto_estimado,
    round(avg(cltv_historico_margen)::numeric, 2) as cltv_margen_medio,
    round(avg(tasa_devolucion_importe)::numeric, 4) as tasa_devolucion_media_importe,
    round(avg(churn_risk_score)::numeric, 2) as churn_risk_medio
from dwh.customer_metrics;

select
    segmento_rfm,
    count(*) as clientes,
    round(sum(ingresos_netos)::numeric, 2) as ingresos_netos,
    round(sum(margen_neto_estimado)::numeric, 2) as margen_neto_estimado,
    round(avg(cltv_historico_margen)::numeric, 2) as cltv_margen_medio,
    round(avg(tasa_devolucion_importe)::numeric, 4) as tasa_devolucion_media_importe,
    round(avg(churn_risk_score)::numeric, 2) as churn_risk_medio
from dwh.v_customer_analytics
group by segmento_rfm
order by margen_neto_estimado desc;

select
    cluster_id,
    cluster_name,
    count(*) as clientes,
    round(sum(ingresos_netos)::numeric, 2) as ingresos_netos,
    round(sum(margen_neto_estimado)::numeric, 2) as margen_neto_estimado,
    round(avg(recencia_dias)::numeric, 2) as recencia_media,
    round(avg(tasa_devolucion_importe)::numeric, 4) as tasa_devolucion_media_importe,
    round(avg(churn_risk_score)::numeric, 2) as churn_risk_medio
from dwh.customer_360
group by cluster_id, cluster_name
order by margen_neto_estimado desc;

select
    count(*) as pares_producto,
    round(avg(lift)::numeric, 4) as lift_medio,
    round(max(lift)::numeric, 4) as lift_maximo,
    round(avg(confidence_a_to_b)::numeric, 4) as confidence_media_a_b
from dwh.product_affinity;

select
    product_name,
    recommended_product_name,
    baskets_together,
    confidence,
    lift,
    support,
    recommendation_rank
from dwh.product_recommendations
order by lift desc, confidence desc
limit 10;

-- =========================
-- 4. Top riesgos y oportunidades
-- =========================

-- Clientes de alto margen historico.
select
    customer_id,
    full_name,
    numero_compras,
    ingresos_netos,
    margen_neto_estimado,
    cltv_historico_margen,
    churn_risk_score,
    churn_risk_level,
    segmento_rfm
from dwh.v_customer_analytics
order by cltv_historico_margen desc
limit 10;

-- Clientes valiosos con mayor riesgo de churn.
select
    customer_id,
    full_name,
    recencia_dias,
    numero_compras,
    ingresos_netos,
    margen_neto_estimado,
    churn_risk_score,
    churn_risk_level,
    segmento_rfm,
    recommended_action
from dwh.v_customer_analytics
where churn_risk_level in ('Critico', 'Alto')
order by churn_risk_score desc, margen_neto_estimado desc
limit 10;
