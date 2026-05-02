-- Fase 4 - Creacion del Data Warehouse para saleshealth
-- Modelo dimensional orientado a analisis de ventas, devoluciones, inventario y CLTV.

drop schema if exists dwh cascade;
create schema dwh;

-- =========================
-- Dimensiones
-- =========================

create table dwh.dim_date (
    date_key integer primary key,
    full_date date not null unique,
    year integer not null,
    quarter integer not null,
    month integer not null,
    month_name varchar(20) not null,
    day integer not null,
    day_of_week integer not null,
    day_name varchar(20) not null,
    week_of_year integer not null,
    is_weekend boolean not null
);

create table dwh.dim_customer (
    customer_key integer generated always as identity primary key,
    customer_id integer not null unique,
    first_name varchar(100),
    last_name varchar(100),
    last_name2 varchar(100),
    full_name varchar(320),
    email varchar(150),
    phone varchar(20),
    created_at timestamp without time zone
);

create table dwh.dim_product (
    product_key integer generated always as identity primary key,
    product_id integer not null unique,
    product_name varchar(200) not null,
    product_category varchar(100),
    manufacturer varchar(150),
    sale_price numeric(10,2),
    central_category_id integer,
    central_category_name varchar(100),
    brand_id integer,
    brand_name varchar(150),
    brand_country varchar(100),
    sku varchar(50),
    barcode varchar(50),
    unit_cost numeric(10,2),
    analytic_unit_cost numeric(10,2),
    cost_source varchar(30) not null,
    is_cost_imputed boolean not null,
    central_unit_price numeric(10,2),
    created_at timestamp without time zone
);

create table dwh.dim_store (
    store_key integer generated always as identity primary key,
    store_id integer not null unique,
    store_name varchar(100) not null,
    address varchar(200),
    city varchar(100),
    postal_code varchar(10),
    district varchar(100),
    area_type varchar(20),
    zone_orientation varchar(20),
    latitude numeric(9,6),
    longitude numeric(9,6),
    opened_date date
);

create table dwh.dim_offer (
    offer_key integer generated always as identity primary key,
    offer_id integer not null unique,
    offer_name varchar(150),
    description text,
    discount_percent numeric(5,2),
    start_date date,
    end_date date,
    is_no_offer boolean not null default false
);

create table dwh.dim_return_reason (
    return_reason_key integer generated always as identity primary key,
    reason_id integer not null unique,
    reason text,
    active boolean,
    is_unknown boolean not null default false
);

create table dwh.dim_warehouse (
    warehouse_key integer generated always as identity primary key,
    warehouse_id integer not null unique,
    warehouse_name varchar(150) not null,
    address varchar(200),
    city varchar(100),
    postal_code varchar(10),
    latitude numeric(9,6),
    longitude numeric(9,6)
);

create table dwh.dim_warehouse_location (
    warehouse_location_key integer generated always as identity primary key,
    location_id integer not null unique,
    warehouse_key integer not null references dwh.dim_warehouse(warehouse_key),
    zone varchar(50),
    aisle varchar(10),
    shelf varchar(10),
    bin_code varchar(10)
);

-- =========================
-- Hechos
-- =========================

create table dwh.fact_sales (
    sales_key bigint generated always as identity primary key,
    sale_item_id integer not null unique,
    sale_id integer not null,
    date_key integer not null references dwh.dim_date(date_key),
    customer_key integer not null references dwh.dim_customer(customer_key),
    product_key integer not null references dwh.dim_product(product_key),
    store_key integer not null references dwh.dim_store(store_key),
    offer_key integer not null references dwh.dim_offer(offer_key),
    quantity integer not null,
    unit_price numeric(10,2) not null,
    subtotal numeric(10,2) not null,
    sale_total numeric(10,2),
    estimated_unit_cost numeric(10,2),
    cost_source varchar(30) not null,
    is_cost_imputed boolean not null,
    estimated_total_cost numeric(12,2),
    gross_margin_amount numeric(12,2),
    gross_margin_percent numeric(8,4)
);

create table dwh.fact_returns (
    returns_key bigint generated always as identity primary key,
    return_id integer not null unique,
    sale_item_id integer not null,
    sale_id integer not null,
    date_key integer not null references dwh.dim_date(date_key),
    customer_key integer not null references dwh.dim_customer(customer_key),
    product_key integer not null references dwh.dim_product(product_key),
    store_key integer not null references dwh.dim_store(store_key),
    return_reason_key integer not null references dwh.dim_return_reason(return_reason_key),
    quantity_returned integer not null,
    returned_amount numeric(12,2),
    cost_source varchar(30) not null,
    is_cost_imputed boolean not null,
    estimated_return_cost numeric(12,2),
    estimated_margin_lost numeric(12,2)
);

create table dwh.fact_store_inventory (
    store_inventory_key bigint generated always as identity primary key,
    inventory_id integer not null unique,
    date_key integer not null references dwh.dim_date(date_key),
    store_key integer not null references dwh.dim_store(store_key),
    product_key integer not null references dwh.dim_product(product_key),
    stock integer,
    cost_source varchar(30) not null,
    is_cost_imputed boolean not null,
    estimated_stock_cost numeric(12,2),
    estimated_stock_value numeric(12,2)
);

create table dwh.fact_central_inventory (
    central_inventory_key bigint generated always as identity primary key,
    inventory_id integer not null unique,
    date_key integer not null references dwh.dim_date(date_key),
    warehouse_key integer not null references dwh.dim_warehouse(warehouse_key),
    warehouse_location_key integer references dwh.dim_warehouse_location(warehouse_location_key),
    product_key integer not null references dwh.dim_product(product_key),
    quantity integer not null,
    min_stock integer,
    max_stock integer,
    cost_source varchar(30) not null,
    is_cost_imputed boolean not null,
    estimated_stock_cost numeric(12,2),
    estimated_stock_value numeric(12,2)
);

create table dwh.customer_clusters (
    customer_id integer primary key references dwh.dim_customer(customer_id),
    cluster_id integer not null,
    cluster_name varchar(100) not null,
    pca_1 numeric(14,6),
    pca_2 numeric(14,6),
    cluster_distance numeric(14,6),
    loaded_at timestamp without time zone not null default now()
);

create table dwh.product_affinity (
    product_affinity_key bigint generated always as identity primary key,
    product_a_key integer not null references dwh.dim_product(product_key),
    product_b_key integer not null references dwh.dim_product(product_key),
    product_a_id integer not null,
    product_b_id integer not null,
    product_a_name varchar(200) not null,
    product_b_name varchar(200) not null,
    baskets_together integer not null,
    baskets_a integer not null,
    baskets_b integer not null,
    total_baskets integer not null,
    support numeric(12,6) not null,
    confidence_a_to_b numeric(12,6) not null,
    confidence_b_to_a numeric(12,6) not null,
    lift numeric(12,6) not null,
    avg_basket_revenue numeric(12,2),
    recommendation_rank integer,
    created_at timestamp without time zone not null default now(),
    unique (product_a_key, product_b_key),
    check (product_a_key < product_b_key)
);

create table dwh.product_recommendations (
    product_key integer not null references dwh.dim_product(product_key),
    recommended_product_key integer not null references dwh.dim_product(product_key),
    product_id integer not null,
    recommended_product_id integer not null,
    product_name varchar(200) not null,
    recommended_product_name varchar(200) not null,
    confidence numeric(12,6) not null,
    lift numeric(12,6) not null,
    support numeric(12,6) not null,
    baskets_together integer not null,
    recommendation_rank integer not null,
    created_at timestamp without time zone not null default now(),
    primary key (product_key, recommended_product_key)
);

-- Indices para acelerar consultas analiticas habituales.
create index idx_fact_sales_customer on dwh.fact_sales(customer_key);
create index idx_fact_sales_product on dwh.fact_sales(product_key);
create index idx_fact_sales_store on dwh.fact_sales(store_key);
create index idx_fact_sales_date on dwh.fact_sales(date_key);

create index idx_fact_returns_customer on dwh.fact_returns(customer_key);
create index idx_fact_returns_product on dwh.fact_returns(product_key);
create index idx_fact_returns_date on dwh.fact_returns(date_key);

create index idx_fact_store_inventory_product on dwh.fact_store_inventory(product_key);
create index idx_fact_central_inventory_product on dwh.fact_central_inventory(product_key);
create index idx_product_affinity_lift on dwh.product_affinity(lift desc);
create index idx_product_affinity_confidence on dwh.product_affinity(confidence_a_to_b desc, confidence_b_to_a desc);
create index idx_product_recommendations_product on dwh.product_recommendations(product_key, recommendation_rank);
