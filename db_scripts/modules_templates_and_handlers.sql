
-- Generated by ORDS REST Data Services 21.4.3.r1300919
-- Schema: ADMIN  Date: Wed May 25 10:07:33 2022 

BEGIN
    
  ORDS.DEFINE_MODULE(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_base_path      => '/products/',
      p_items_per_page => 25,
      p_status         => 'PUBLISHED',
      p_comments       => NULL);

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'createorder/',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'createorder/',
      p_method         => 'POST',
      p_source_type    => 'plsql/block',
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'insert into ORDERS (PRODUCT_ID, PRODUCT_PRICE)
values (:PRODUCT_ID, :QUANTITY, :PRODUCT_PRICE)');

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'getorders/',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'getorders/',
      p_method         => 'GET',
      p_source_type    => 'json/collection',
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'SELECT o.ORDER_ID, p.PRODUCT_NAME, p.PRODUCT_DESCRIPTION, o.QUANTITY, TO_CHAR(o.PRODUCT_PRICE,''L99G999D99MI'',''NLS_NUMERIC_CHARACTERS = ''''.,''''NLS_CURRENCY = "$'') PRODUCT_PRICE
from orders o, products p
where o.product_id = p.product_id
order by o.order_id');

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'getprice/:product_id',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'com.oracle.flaskords.lab',
      p_pattern        => 'getprice/:product_id',
      p_method         => 'GET',
      p_source_type    => 'json/collection',
      p_items_per_page => 25,
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'select product_price from PRODUCTS
where product_id = :product_id');

COMMIT;

END;