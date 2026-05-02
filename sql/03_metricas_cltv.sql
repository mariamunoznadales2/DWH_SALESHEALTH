-- Fase 6 y 7 - Metricas de cliente: CLTV, RFM y tasa de devolucion
-- Ejecutar despues de sql/01_crear_dwh.sql y sql/02_etl.sql.

drop view if exists dwh.customer_360 cascade;
drop view if exists dwh.v_customer_analytics cascade;
drop table if exists dwh.customer_rfm cascade;
drop table if exists dwh.customer_metrics cascade;

-- =========================
-- Tabla principal de metricas de cliente
-- =========================

create table dwh.customer_metrics as
with parametros as (
    select max(dd.full_date) as fecha_referencia
    from dwh.fact_sales fs
    join dwh.dim_date dd on dd.date_key = fs.date_key
),
ventas_cliente as (
    select
        dc.customer_key,
        dc.customer_id,
        dc.full_name,
        dc.email,
        min(dd.full_date) as primera_compra,
        max(dd.full_date) as ultima_compra,
        count(distinct fs.sale_id) as numero_compras,
        count(*) as lineas_compra,
        sum(fs.quantity) as unidades_compradas,
        sum(fs.subtotal) as ingresos_brutos,
        sum(coalesce(fs.gross_margin_amount, 0)) as margen_bruto_estimado,
        count(*) filter (where fs.is_cost_imputed) as lineas_coste_imputado,
        avg(fs.subtotal) as importe_medio_linea,
        avg(fs.sale_total) as ticket_medio_cabecera_repetido
    from dwh.fact_sales fs
    join dwh.dim_customer dc on dc.customer_key = fs.customer_key
    join dwh.dim_date dd on dd.date_key = fs.date_key
    group by
        dc.customer_key,
        dc.customer_id,
        dc.full_name,
        dc.email
),
ventas_agregadas as (
    select
        customer_key,
        sum(sale_total) as ingresos_por_ticket
    from (
        select distinct
            customer_key,
            sale_id,
            sale_total
        from dwh.fact_sales
    ) ventas_unicas
    group by customer_key
),
devoluciones_cliente as (
    select
        fr.customer_key,
        count(distinct fr.return_id) as numero_devoluciones,
        sum(fr.quantity_returned) as unidades_devueltas,
        sum(fr.returned_amount) as importe_devuelto,
        sum(coalesce(fr.estimated_margin_lost, 0)) as margen_perdido_estimado
    from dwh.fact_returns fr
    group by fr.customer_key
)
select
    vc.customer_key,
    vc.customer_id,
    vc.full_name,
    vc.email,
    vc.primera_compra,
    vc.ultima_compra,
    p.fecha_referencia,
    vc.numero_compras,
    vc.lineas_compra,
    vc.unidades_compradas,
    coalesce(dc.numero_devoluciones, 0) as numero_devoluciones,
    coalesce(dc.unidades_devueltas, 0) as unidades_devueltas,
    round(vc.ingresos_brutos::numeric, 2) as ingresos_brutos,
    round(coalesce(dc.importe_devuelto, 0)::numeric, 2) as importe_devuelto,
    round((vc.ingresos_brutos - coalesce(dc.importe_devuelto, 0))::numeric, 2) as ingresos_netos,
    round(vc.margen_bruto_estimado::numeric, 2) as margen_bruto_estimado,
    round(coalesce(dc.margen_perdido_estimado, 0)::numeric, 2) as margen_perdido_estimado,
    round((vc.margen_bruto_estimado - coalesce(dc.margen_perdido_estimado, 0))::numeric, 2) as margen_neto_estimado,
    vc.lineas_coste_imputado,
    round((va.ingresos_por_ticket / nullif(vc.numero_compras, 0))::numeric, 2) as ticket_medio,
    round((vc.ingresos_brutos / nullif(vc.lineas_compra, 0))::numeric, 2) as importe_medio_linea,
    (p.fecha_referencia - vc.primera_compra) as antiguedad_dias,
    (p.fecha_referencia - vc.ultima_compra) as recencia_dias,
    greatest((p.fecha_referencia - vc.primera_compra) / 30.4375, 1) as antiguedad_meses,
    round((vc.numero_compras / greatest((p.fecha_referencia - vc.primera_compra) / 30.4375, 1))::numeric, 4) as frecuencia_mensual,
    round((vc.numero_compras / greatest((p.fecha_referencia - vc.primera_compra) / 365.25, 1))::numeric, 4) as frecuencia_anual,
    round((coalesce(dc.importe_devuelto, 0) / nullif(vc.ingresos_brutos, 0))::numeric, 4) as tasa_devolucion_importe,
    round((coalesce(dc.unidades_devueltas, 0)::numeric / nullif(vc.unidades_compradas, 0))::numeric, 4) as tasa_devolucion_unidades,
    round(((vc.margen_bruto_estimado - coalesce(dc.margen_perdido_estimado, 0)) / nullif((vc.ingresos_brutos - coalesce(dc.importe_devuelto, 0)), 0))::numeric, 4) as margen_neto_pct,
    -- CLTV historico: valor neto observado hasta la fecha de referencia.
    round((vc.ingresos_brutos - coalesce(dc.importe_devuelto, 0))::numeric, 2) as cltv_historico_ingresos,
    round((vc.margen_bruto_estimado - coalesce(dc.margen_perdido_estimado, 0))::numeric, 2) as cltv_historico_margen,
    -- CLTV estimado a 12 meses: frecuencia mensual historica * ticket medio * 12.
    round((
        (vc.numero_compras / greatest((p.fecha_referencia - vc.primera_compra) / 30.4375, 1))
        * (va.ingresos_por_ticket / nullif(vc.numero_compras, 0))
        * 12
    )::numeric, 2) as cltv_estimado_12m_ingresos,
    round((
        (vc.numero_compras / greatest((p.fecha_referencia - vc.primera_compra) / 30.4375, 1))
        * ((vc.margen_bruto_estimado - coalesce(dc.margen_perdido_estimado, 0)) / nullif(vc.numero_compras, 0))
        * 12
    )::numeric, 2) as cltv_estimado_12m_margen
from ventas_cliente vc
join ventas_agregadas va on va.customer_key = vc.customer_key
cross join parametros p
left join devoluciones_cliente dc on dc.customer_key = vc.customer_key;

alter table dwh.customer_metrics
    add column churn_risk_score integer,
    add column churn_risk_level varchar(20),
    add column recommended_action varchar(120);

with umbrales as (
    select
        percentile_cont(0.75) within group (order by cltv_historico_margen) as p75_cltv_margen,
        percentile_cont(0.50) within group (order by cltv_historico_margen) as p50_cltv_margen
    from dwh.customer_metrics
),
scoring as (
    select
        cm.customer_key,
        least(100, greatest(0,
            (case
                when cm.recencia_dias >= 365 then 40
                when cm.recencia_dias >= 180 then 30
                when cm.recencia_dias >= 90 then 18
                else 5
            end)
            + (case
                when cm.frecuencia_mensual < 0.05 then 20
                when cm.frecuencia_mensual < 0.15 then 12
                else 3
            end)
            + (case
                when cm.tasa_devolucion_importe >= 0.40 then 20
                when cm.tasa_devolucion_importe >= 0.20 then 12
                else 0
            end)
            + (case
                when cm.cltv_historico_margen >= u.p75_cltv_margen then 15
                when cm.cltv_historico_margen >= u.p50_cltv_margen then 8
                else 0
            end)
        ))::integer as churn_risk_score
    from dwh.customer_metrics cm
    cross join umbrales u
)
update dwh.customer_metrics cm
set
    churn_risk_score = s.churn_risk_score,
    churn_risk_level = case
        when s.churn_risk_score >= 75 then 'Critico'
        when s.churn_risk_score >= 55 then 'Alto'
        when s.churn_risk_score >= 35 then 'Medio'
        else 'Bajo'
    end,
    recommended_action = case
        when s.churn_risk_score >= 75 and cm.cltv_historico_margen >= u.p75_cltv_margen then 'Recuperacion prioritaria de alto valor'
        when s.churn_risk_score >= 55 and cm.cltv_historico_margen >= u.p50_cltv_margen then 'Campana de reactivacion personalizada'
        when cm.tasa_devolucion_importe >= 0.40 then 'Revisar experiencia y causas de devolucion'
        when cm.frecuencia_mensual >= 0.25 and cm.recencia_dias < 90 then 'Fidelizacion y venta cruzada'
        else 'Mantener seguimiento comercial'
    end
from scoring s
cross join umbrales u
where cm.customer_key = s.customer_key;

alter table dwh.customer_metrics
    add primary key (customer_key);

create index idx_customer_metrics_customer_id on dwh.customer_metrics(customer_id);
create index idx_customer_metrics_cltv on dwh.customer_metrics(cltv_historico_margen desc);
create index idx_customer_metrics_churn on dwh.customer_metrics(churn_risk_score desc);

-- =========================
-- RFM: Recency, Frequency, Monetary
-- =========================

create table dwh.customer_rfm as
with puntuaciones as (
    select
        cm.*,
        ntile(5) over (order by cm.recencia_dias desc) as r_score,
        ntile(5) over (order by cm.numero_compras asc) as f_score,
        ntile(5) over (order by cm.ingresos_netos asc) as m_score
    from dwh.customer_metrics cm
)
select
    customer_key,
    customer_id,
    full_name,
    email,
    recencia_dias,
    numero_compras,
    ingresos_netos,
    margen_neto_estimado,
    tasa_devolucion_importe,
    churn_risk_score,
    churn_risk_level,
    recommended_action,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) as rfm_score,
    concat(r_score::text, f_score::text, m_score::text) as rfm_code,
    case
        when r_score >= 4 and f_score >= 4 and m_score >= 4 then 'Clientes estrella'
        when r_score >= 4 and f_score >= 3 then 'Clientes fieles recientes'
        when r_score <= 2 and f_score >= 4 and m_score >= 4 then 'Valiosos en riesgo'
        when r_score <= 2 and f_score <= 2 then 'Clientes dormidos'
        when m_score >= 4 then 'Alto valor'
        when f_score >= 4 then 'Compradores frecuentes'
        else 'Clientes medios'
    end as segmento_rfm
from puntuaciones;

alter table dwh.customer_rfm
    add primary key (customer_key);

create index idx_customer_rfm_segmento on dwh.customer_rfm(segmento_rfm);
create index idx_customer_rfm_score on dwh.customer_rfm(rfm_score desc);

-- =========================
-- Vista final para analisis y notebook
-- =========================

create or replace view dwh.v_customer_analytics as
select
    cm.customer_key,
    cm.customer_id,
    cm.full_name,
    cm.email,
    cm.primera_compra,
    cm.ultima_compra,
    cm.fecha_referencia,
    cm.numero_compras,
    cm.unidades_compradas,
    cm.unidades_devueltas,
    cm.ingresos_brutos,
    cm.importe_devuelto,
    cm.ingresos_netos,
    cm.margen_neto_estimado,
    cm.ticket_medio,
    cm.antiguedad_dias,
    cm.recencia_dias,
    cm.frecuencia_mensual,
    cm.frecuencia_anual,
    cm.tasa_devolucion_importe,
    cm.tasa_devolucion_unidades,
    cm.margen_neto_pct,
    cm.cltv_historico_ingresos,
    cm.cltv_historico_margen,
    cm.cltv_estimado_12m_ingresos,
    cm.cltv_estimado_12m_margen,
    cm.lineas_coste_imputado,
    cm.churn_risk_score,
    cm.churn_risk_level,
    cm.recommended_action,
    rfm.r_score,
    rfm.f_score,
    rfm.m_score,
    rfm.rfm_score,
    rfm.rfm_code,
    rfm.segmento_rfm
from dwh.customer_metrics cm
join dwh.customer_rfm rfm on rfm.customer_key = cm.customer_key;

create or replace view dwh.customer_360 as
select
    v.*,
    null::integer as cluster_id,
    null::varchar(100) as cluster_name,
    null::numeric(14,6) as pca_1,
    null::numeric(14,6) as pca_2
from dwh.v_customer_analytics v;

-- =========================
-- Consultas de comprobacion
-- =========================

select
    count(*) as clientes_con_metricas,
    round(sum(ingresos_netos)::numeric, 2) as ingresos_netos,
    round(sum(margen_neto_estimado)::numeric, 2) as margen_neto_estimado,
    round(avg(cltv_historico_ingresos)::numeric, 2) as cltv_medio_ingresos,
    round(avg(cltv_historico_margen)::numeric, 2) as cltv_medio_margen
from dwh.customer_metrics;

select
    segmento_rfm,
    count(*) as clientes,
    round(avg(ingresos_netos)::numeric, 2) as ingresos_netos_medios,
    round(avg(cltv_historico_margen)::numeric, 2) as cltv_margen_medio
from dwh.v_customer_analytics
group by segmento_rfm
order by clientes desc;

select
    customer_id,
    full_name,
    numero_compras,
    ingresos_netos,
    margen_neto_estimado,
    cltv_historico_margen,
    cltv_estimado_12m_margen,
    segmento_rfm
from dwh.v_customer_analytics
order by cltv_historico_margen desc
limit 10;
