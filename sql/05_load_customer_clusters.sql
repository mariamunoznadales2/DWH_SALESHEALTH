-- Fase 8 - Carga de clusters y Customer 360 final
-- Ejecutar despues de generar notebooks/customer_clusters.csv con:
--   python scripts/build_customer_clusters.py

truncate table dwh.customer_clusters;

\copy dwh.customer_clusters (customer_id, cluster_id, cluster_name, pca_1, pca_2, cluster_distance) from 'notebooks/customer_clusters.csv' with (format csv, header true, encoding 'UTF8');

create or replace view dwh.customer_360 as
select
    v.*,
    cc.cluster_id,
    cc.cluster_name,
    cc.pca_1,
    cc.pca_2,
    cc.cluster_distance
from dwh.v_customer_analytics v
left join dwh.customer_clusters cc on cc.customer_id = v.customer_id;

select
    cluster_id,
    cluster_name,
    count(*) as clientes,
    round(avg(ingresos_netos)::numeric, 2) as ingresos_netos_medios,
    round(avg(margen_neto_estimado)::numeric, 2) as margen_neto_medio,
    round(avg(recencia_dias)::numeric, 2) as recencia_media,
    round(avg(tasa_devolucion_importe)::numeric, 4) as tasa_devolucion_media,
    round(avg(churn_risk_score)::numeric, 2) as churn_risk_medio
from dwh.customer_360
group by cluster_id, cluster_name
order by cluster_id;
