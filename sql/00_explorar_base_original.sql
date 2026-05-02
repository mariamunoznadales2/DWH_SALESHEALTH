-- Fase 2 - Consultas para explorar la base original saleshealth

-- 1. Ver todas las tablas del esquema public
select schemaname, tablename
from pg_tables
where schemaname = 'public'
order by tablename;

-- 2. Ver columnas, tipos de datos y nulabilidad
select
    table_name,
    column_name,
    data_type,
    is_nullable
from information_schema.columns
where table_schema = 'public'
order by table_name, ordinal_position;

-- 3. Ver claves foraneas entre tablas
select
    tc.table_name,
    kcu.column_name,
    ccu.table_name as foreign_table_name,
    ccu.column_name as foreign_column_name
from information_schema.table_constraints tc
join information_schema.key_column_usage kcu
    on tc.constraint_name = kcu.constraint_name
   and tc.table_schema = kcu.table_schema
join information_schema.constraint_column_usage ccu
    on ccu.constraint_name = tc.constraint_name
   and ccu.table_schema = tc.table_schema
where tc.constraint_type = 'FOREIGN KEY'
  and tc.table_schema = 'public'
order by tc.table_name, kcu.column_name;

-- 4. Recuento de filas por tabla
select 'brand' tabla, count(*) filas from brand
union all select 'category', count(*) from category
union all select 'central_inventory', count(*) from central_inventory
union all select 'central_product', count(*) from central_product
union all select 'city_zone', count(*) from city_zone
union all select 'customer', count(*) from customer
union all select 'inventory', count(*) from inventory
union all select 'offer', count(*) from offer
union all select 'product', count(*) from product
union all select 'product_offer', count(*) from product_offer
union all select 'return_item', count(*) from return_item
union all select 'return_reason', count(*) from return_reason
union all select 'sale', count(*) from sale
union all select 'sale_item', count(*) from sale_item
union all select 'store', count(*) from store
union all select 'warehouse', count(*) from warehouse
union all select 'warehouse_location', count(*) from warehouse_location
order by tabla;

-- 5. Resumen general de ventas
select
    min(sale_date) as primera_venta,
    max(sale_date) as ultima_venta,
    count(*) as numero_ventas,
    sum(total) as ingresos_totales,
    avg(total) as ticket_medio
from sale;

-- 6. Resumen general de devoluciones
select
    min(return_date) as primera_devolucion,
    max(return_date) as ultima_devolucion,
    count(*) as numero_devoluciones,
    sum(quantity) as unidades_devueltas
from return_item;

-- 7. Relacion basica cliente-venta-linea-producto
select
    s.sale_id,
    s.sale_date,
    c.customer_id,
    c.email,
    st.name as tienda,
    p.name as producto,
    si.quantity,
    si.unit_price,
    si.subtotal
from sale s
join customer c on c.customer_id = s.customer_id
join store st on st.store_id = s.store_id
join sale_item si on si.sale_id = s.sale_id
join product p on p.product_id = si.product_id
limit 20;
