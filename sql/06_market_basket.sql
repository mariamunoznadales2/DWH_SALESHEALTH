-- Fase 9 - Market Basket Analysis
-- Detecta productos comprados juntos para recomendaciones, packs y promociones cruzadas.

truncate table dwh.product_recommendations;
truncate table dwh.product_affinity;

insert into dwh.product_affinity (
    product_a_key,
    product_b_key,
    product_a_id,
    product_b_id,
    product_a_name,
    product_b_name,
    baskets_together,
    baskets_a,
    baskets_b,
    total_baskets,
    support,
    confidence_a_to_b,
    confidence_b_to_a,
    lift,
    avg_basket_revenue,
    recommendation_rank
)
with baskets as (
    select
        sale_id,
        sum(subtotal) as basket_revenue
    from dwh.fact_sales
    group by sale_id
),
basket_products as (
    select distinct
        fs.sale_id,
        fs.product_key
    from dwh.fact_sales fs
),
total as (
    select count(*) as total_baskets
    from baskets
),
product_counts as (
    select
        product_key,
        count(*) as baskets_product
    from basket_products
    group by product_key
),
pairs as (
    select
        least(bp1.product_key, bp2.product_key) as product_a_key,
        greatest(bp1.product_key, bp2.product_key) as product_b_key,
        count(*) as baskets_together,
        round(avg(b.basket_revenue)::numeric, 2) as avg_basket_revenue
    from basket_products bp1
    join basket_products bp2
      on bp1.sale_id = bp2.sale_id
     and bp1.product_key < bp2.product_key
    join baskets b on b.sale_id = bp1.sale_id
    group by
        least(bp1.product_key, bp2.product_key),
        greatest(bp1.product_key, bp2.product_key)
),
scored as (
    select
        p.product_a_key,
        p.product_b_key,
        dpa.product_id as product_a_id,
        dpb.product_id as product_b_id,
        dpa.product_name as product_a_name,
        dpb.product_name as product_b_name,
        p.baskets_together,
        pca.baskets_product as baskets_a,
        pcb.baskets_product as baskets_b,
        t.total_baskets,
        round((p.baskets_together::numeric / nullif(t.total_baskets, 0))::numeric, 6) as support,
        round((p.baskets_together::numeric / nullif(pca.baskets_product, 0))::numeric, 6) as confidence_a_to_b,
        round((p.baskets_together::numeric / nullif(pcb.baskets_product, 0))::numeric, 6) as confidence_b_to_a,
        round((
            (p.baskets_together::numeric / nullif(t.total_baskets, 0))
            / nullif(
                (pca.baskets_product::numeric / nullif(t.total_baskets, 0))
                * (pcb.baskets_product::numeric / nullif(t.total_baskets, 0)),
                0
            )
        )::numeric, 6) as lift,
        p.avg_basket_revenue
    from pairs p
    join product_counts pca on pca.product_key = p.product_a_key
    join product_counts pcb on pcb.product_key = p.product_b_key
    join dwh.dim_product dpa on dpa.product_key = p.product_a_key
    join dwh.dim_product dpb on dpb.product_key = p.product_b_key
    cross join total t
    where p.baskets_together >= 10
)
select
    product_a_key,
    product_b_key,
    product_a_id,
    product_b_id,
    product_a_name,
    product_b_name,
    baskets_together,
    baskets_a,
    baskets_b,
    total_baskets,
    support,
    confidence_a_to_b,
    confidence_b_to_a,
    lift,
    avg_basket_revenue,
    row_number() over (
        partition by product_a_key
        order by lift desc, confidence_a_to_b desc, baskets_together desc
    ) as recommendation_rank
from scored;

insert into dwh.product_recommendations (
    product_key,
    recommended_product_key,
    product_id,
    recommended_product_id,
    product_name,
    recommended_product_name,
    confidence,
    lift,
    support,
    baskets_together,
    recommendation_rank
)
with directional as (
    select
        product_a_key as product_key,
        product_b_key as recommended_product_key,
        product_a_id as product_id,
        product_b_id as recommended_product_id,
        product_a_name as product_name,
        product_b_name as recommended_product_name,
        confidence_a_to_b as confidence,
        lift,
        support,
        baskets_together
    from dwh.product_affinity
    union all
    select
        product_b_key,
        product_a_key,
        product_b_id,
        product_a_id,
        product_b_name,
        product_a_name,
        confidence_b_to_a,
        lift,
        support,
        baskets_together
    from dwh.product_affinity
),
ranked as (
    select
        *,
        row_number() over (
            partition by product_key
            order by lift desc, confidence desc, baskets_together desc
        ) as recommendation_rank
    from directional
    where lift > 1
)
select
    product_key,
    recommended_product_key,
    product_id,
    recommended_product_id,
    product_name,
    recommended_product_name,
    confidence,
    lift,
    support,
    baskets_together,
    recommendation_rank
from ranked
where recommendation_rank <= 5;

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
limit 15;
