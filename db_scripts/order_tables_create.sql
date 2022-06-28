/* Orders */

drop table orders;

drop table products;

drop table museums;

CREATE TABLE orders
(order_id NUMBER GENERATED ALWAYS AS IDENTITY,
product_id NUMBER(6) NOT NULL,
quantity NUMBER(8),
total_price NUMBER(8,2)
);

CREATE UNIQUE INDEX order_pk ON orders (order_id);

ALTER TABLE orders ADD (CONSTRAINT order_pk PRIMARY KEY (order_id));


/* Product */

CREATE TABLE products
(product_id NUMBER GENERATED ALWAYS AS IDENTITY,
product_name VARCHAR2(50),
product_description VARCHAR2(2000),
product_status VARCHAR2(20),
product_price NUMBER(8,2)
);

CREATE UNIQUE INDEX products_pk on products (product_id) ;

ALTER TABLE products ADD ( CONSTRAINT product_pk PRIMARY KEY (product_id));


/* Stores */

create table museums (
museum_id NUMBER GENERATED ALWAYS AS IDENTITY,
museum_name varchar2(500),
museum_address varchar2(500),
museum_lat NUMBER(8,6),
museum_long NUMBER(9,6)
);

CREATE UNIQUE INDEX museum_pk on museum (museum_id) ;

ALTER TABLE museums ADD ( CONSTRAINT museum_pk PRIMARY KEY (museum_id));

commit;