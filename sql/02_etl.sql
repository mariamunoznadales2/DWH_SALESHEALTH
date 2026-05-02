-- Fase 5 - ETL del Data Warehouse saleshealth
-- Ejecutar despues de sql/01_crear_dwh.sql.

begin;

-- =========================
-- Dimensiones
-- =========================

insert into dwh.dim_date (
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    day,
    day_of_week,
    day_name,
    week_of_year,
    is_weekend
)
select
    to_char(d::date, 'YYYYMMDD')::integer as date_key,
    d::date as full_date,
    extract(year from d)::integer as year,
    extract(quarter from d)::integer as quarter,
    extract(month from d)::integer as month,
    trim(to_char(d, 'TMMonth')) as month_name,
    extract(day from d)::integer as day,
    extract(isodow from d)::integer as day_of_week,
    trim(to_char(d, 'TMDay')) as day_name,
    extract(week from d)::integer as week_of_year,
    extract(isodow from d)::integer in (6, 7) as is_weekend
from generate_series(
    (
        select min(fecha)::date
        from (
            select min(sale_date)::date as fecha from sale
            union all select min(return_date)::date from return_item
            union all select min(last_update)::date from inventory
            union all select min(last_update)::date from central_inventory
        ) fechas
    ),
    (
        select max(fecha)::date
        from (
            select max(sale_date)::date as fecha from sale
            union all select max(return_date)::date from return_item
            union all select max(last_update)::date from inventory
            union all select max(last_update)::date from central_inventory
        ) fechas
    ),
    interval '1 day'
) d;

insert into dwh.dim_customer (
    customer_id,
    first_name,
    last_name,
    last_name2,
    full_name,
    email,
    phone,
    created_at
)
select
    customer_id,
    first_name,
    last_name,
    last_name2,
    nullif(trim(concat_ws(' ', first_name, last_name, last_name2)), '') as full_name,
    email,
    phone,
    created_at
from customer;

insert into dwh.dim_product (
    product_id,
    product_name,
    product_category,
    manufacturer,
    sale_price,
    central_category_id,
    central_category_name,
    brand_id,
    brand_name,
    brand_country,
    sku,
    barcode,
    unit_cost,
    analytic_unit_cost,
    cost_source,
    is_cost_imputed,
    central_unit_price,
    created_at
)
select
    p.product_id,
    p.name as product_name,
    p.category as product_category,
    p.manufacturer,
    p.price as sale_price,
    cp.category_id as central_category_id,
    c.name as central_category_name,
    cp.brand_id,
    b.name as brand_name,
    b.country as brand_country,
    cp.sku,
    cp.barcode,
    cp.unit_cost,
    coalesce(cp.unit_cost, round((p.price * 0.60)::numeric, 2)) as analytic_unit_cost,
    case
        when cp.unit_cost is null then 'IMPUTED_60_PCT_PRICE'
        else 'CENTRAL_PRODUCT'
    end as cost_source,
    (cp.unit_cost is null) as is_cost_imputed,
    cp.unit_price as central_unit_price,
    p.created_at
from product p
left join central_product cp on cp.product_id = p.product_id
left join category c on c.category_id = cp.category_id
left join brand b on b.brand_id = cp.brand_id;

insert into dwh.dim_store (
    store_id,
    store_name,
    address,
    city,
    postal_code,
    district,
    area_type,
    zone_orientation,
    latitude,
    longitude,
    opened_date
)
select
    s.store_id,
    s.name,
    s.address,
    s.city,
    s.postal_code,
    cz.district,
    cz.area_type,
    cz.zone_orientation,
    s.latitude,
    s.longitude,
    s.opened_date
from store s
left join city_zone cz on cz.postal_code = left(s.postal_code, 5);

insert into dwh.dim_offer (
    offer_id,
    offer_name,
    description,
    discount_percent,
    start_date,
    end_date,
    is_no_offer
)
values (0, 'Sin oferta', 'Venta sin promocion asociada', 0, null, null, true);

insert into dwh.dim_offer (
    offer_id,
    offer_name,
    description,
    discount_percent,
    start_date,
    end_date,
    is_no_offer
)
select
    offer_id,
    name,
    description,
    discount_percent,
    start_date,
    end_date,
    false
from offer;

insert into dwh.dim_return_reason (
    reason_id,
    reason,
    active,
    is_unknown
)
values (0, 'Sin motivo informado', true, true);

insert into dwh.dim_return_reason (
    reason_id,
    reason,
    active,
    is_unknown
)
select
    reason_id,
    reason,
    active,
    false
from return_reason;

insert into dwh.dim_warehouse (
    warehouse_id,
    warehouse_name,
    address,
    city,
    postal_code,
    latitude,
    longitude
)
select
    warehouse_id,
    name,
    address,
    city,
    postal_code,
    latitude,
    longitude
from warehouse;

insert into dwh.dim_warehouse_location (
    location_id,
    warehouse_key,
    zone,
    aisle,
    shelf,
    bin_code
)
select
    wl.location_id,
    dw.warehouse_key,
    wl.zone,
    wl.aisle,
    wl.shelf,
    wl.bin_code
from warehouse_location wl
join dwh.dim_warehouse dw on dw.warehouse_id = wl.warehouse_id;

-- =========================
-- Hechos
-- =========================

insert into dwh.fact_sales (
    sale_item_id,
    sale_id,
    date_key,
    customer_key,
    product_key,
    store_key,
    offer_key,
    quantity,
    unit_price,
    subtotal,
    sale_total,
    estimated_unit_cost,
    cost_source,
    is_cost_imputed,
    estimated_total_cost,
    gross_margin_amount,
    gross_margin_percent
)
select
    si.sale_item_id,
    s.sale_id,
    dd.date_key,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    dof.offer_key,
    si.quantity,
    si.unit_price,
    si.subtotal,
    s.total as sale_total,
    dp.analytic_unit_cost as estimated_unit_cost,
    dp.cost_source,
    dp.is_cost_imputed,
    round((dp.analytic_unit_cost * si.quantity)::numeric, 2) as estimated_total_cost,
    round((si.subtotal - (dp.analytic_unit_cost * si.quantity))::numeric, 2) as gross_margin_amount,
    case
        when si.subtotal = 0 then null
        else round(((si.subtotal - (dp.analytic_unit_cost * si.quantity)) / si.subtotal)::numeric, 4)
    end as gross_margin_percent
from sale_item si
join sale s on s.sale_id = si.sale_id
join dwh.dim_date dd on dd.full_date = s.sale_date::date
join dwh.dim_customer dc on dc.customer_id = s.customer_id
join dwh.dim_product dp on dp.product_id = si.product_id
join dwh.dim_store ds on ds.store_id = s.store_id
join dwh.dim_offer dof on dof.offer_id = coalesce(si.offer_id, 0);

insert into dwh.fact_returns (
    return_id,
    sale_item_id,
    sale_id,
    date_key,
    customer_key,
    product_key,
    store_key,
    return_reason_key,
    quantity_returned,
    returned_amount,
    cost_source,
    is_cost_imputed,
    estimated_return_cost,
    estimated_margin_lost
)
select
    ri.return_id,
    si.sale_item_id,
    s.sale_id,
    dd.date_key,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    drr.return_reason_key,
    ri.quantity,
    round((ri.quantity * si.unit_price)::numeric, 2) as returned_amount,
    dp.cost_source,
    dp.is_cost_imputed,
    round((ri.quantity * dp.analytic_unit_cost)::numeric, 2) as estimated_return_cost,
    round((ri.quantity * (si.unit_price - dp.analytic_unit_cost))::numeric, 2) as estimated_margin_lost
from return_item ri
join sale_item si on si.sale_item_id = ri.sale_item_id
join sale s on s.sale_id = si.sale_id
join dwh.dim_date dd on dd.full_date = ri.return_date::date
join dwh.dim_customer dc on dc.customer_id = s.customer_id
join dwh.dim_product dp on dp.product_id = si.product_id
join dwh.dim_store ds on ds.store_id = s.store_id
join dwh.dim_return_reason drr on drr.reason_id = coalesce(ri.reason_id, 0);

insert into dwh.fact_store_inventory (
    inventory_id,
    date_key,
    store_key,
    product_key,
    stock,
    cost_source,
    is_cost_imputed,
    estimated_stock_cost,
    estimated_stock_value
)
select
    i.inventory_id,
    dd.date_key,
    ds.store_key,
    dp.product_key,
    i.stock,
    dp.cost_source,
    dp.is_cost_imputed,
    round((i.stock * dp.analytic_unit_cost)::numeric, 2) as estimated_stock_cost,
    round((i.stock * coalesce(dp.central_unit_price, dp.sale_price))::numeric, 2) as estimated_stock_value
from inventory i
join dwh.dim_date dd on dd.full_date = i.last_update::date
join dwh.dim_store ds on ds.store_id = i.store_id
join dwh.dim_product dp on dp.product_id = i.product_id;

insert into dwh.fact_central_inventory (
    inventory_id,
    date_key,
    warehouse_key,
    warehouse_location_key,
    product_key,
    quantity,
    min_stock,
    max_stock,
    cost_source,
    is_cost_imputed,
    estimated_stock_cost,
    estimated_stock_value
)
select
    ci.inventory_id,
    dd.date_key,
    dw.warehouse_key,
    dwl.warehouse_location_key,
    dp.product_key,
    ci.quantity,
    ci.min_stock,
    ci.max_stock,
    dp.cost_source,
    dp.is_cost_imputed,
    round((ci.quantity * dp.analytic_unit_cost)::numeric, 2) as estimated_stock_cost,
    round((ci.quantity * coalesce(dp.central_unit_price, dp.sale_price))::numeric, 2) as estimated_stock_value
from central_inventory ci
join dwh.dim_date dd on dd.full_date = ci.last_update::date
join dwh.dim_warehouse dw on dw.warehouse_id = ci.warehouse_id
left join dwh.dim_warehouse_location dwl on dwl.location_id = ci.location_id
join dwh.dim_product dp on dp.product_id = ci.product_id;

commit;

-- Comprobacion rapida de cargas.
select 'dim_date' tabla, count(*) filas from dwh.dim_date
union all select 'dim_customer', count(*) from dwh.dim_customer
union all select 'dim_product', count(*) from dwh.dim_product
union all select 'dim_store', count(*) from dwh.dim_store
union all select 'dim_offer', count(*) from dwh.dim_offer
union all select 'dim_return_reason', count(*) from dwh.dim_return_reason
union all select 'dim_warehouse', count(*) from dwh.dim_warehouse
union all select 'dim_warehouse_location', count(*) from dwh.dim_warehouse_location
union all select 'fact_sales', count(*) from dwh.fact_sales
union all select 'fact_returns', count(*) from dwh.fact_returns
union all select 'fact_store_inventory', count(*) from dwh.fact_store_inventory
union all select 'fact_central_inventory', count(*) from dwh.fact_central_inventory
order by tabla;
