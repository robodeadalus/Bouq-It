-- Use Manila time (GMT+8) for all timestamp with time zone columns
SET TIME ZONE 'Asia/Manila';

CREATE DATABASE bouq_it;
\c bouq_it

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    contact VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    barangay VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    payment VARCHAR(255) NOT NULL
        CHECK (payment IN ('G-Cash', 'Maya', 'Cash on Delivery', 'Credit/Debit Card')),
    address VARCHAR(255) NOT NULL,
    barangay VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(255) NOT NULL,
    ordered_by INT NOT NULL
        REFERENCES customers(id),
    order_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE flowers (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE bouquets (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE custom_bouquets (
    customer_id INT NOT NULL
        REFERENCES customers(id),
    bouquet_name VARCHAR(255) NOT NULL UNIQUE,
    design VARCHAR(255),
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (customer_id, bouquet_name)
);

CREATE TABLE bouquet_flowers (
    bouquet_name VARCHAR(255) NOT NULL
        REFERENCES bouquets(name),
    flower_name VARCHAR(255) NOT NULL
        REFERENCES flowers(name),
    quantity INT NOT NULL CHECK (quantity >= 1),
    PRIMARY KEY (bouquet_name, flower_name)
);

CREATE TABLE order_flowers (
    order_id INT NOT NULL
        REFERENCES orders(id),
    flower_name VARCHAR(255) NOT NULL
        REFERENCES flowers(name),
    quantity INT NOT NULL CHECK (quantity >= 1),
    PRIMARY KEY (order_id, flower_name)
);

CREATE TABLE order_bouquets (
    order_id INT NOT NULL
        REFERENCES orders(id),
    bouquet_name VARCHAR(255) NOT NULL
        REFERENCES bouquets(name),
    quantity INT NOT NULL CHECK (quantity >= 1),
    design VARCHAR(255),
    PRIMARY KEY (order_id, bouquet_name)
);

CREATE TABLE order_custom (
    order_id INT NOT NULL
        REFERENCES orders(id),
    custom_bouquet VARCHAR(255) NOT NULL UNIQUE,
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, custom_bouquet)
);

CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    barangay VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    sales INT NOT NULL,
    image_link TEXT NOT NULL
);

CREATE TABLE shop_flowers (
    shop_id INT NOT NULL
        REFERENCES shops(id),
    flower_name VARCHAR(255) NOT NULL
        REFERENCES flowers(name),
    quantity INT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, flower_name)
);

CREATE TABLE shop_bouquets (
    shop_id INT NOT NULL
        REFERENCES shops(id),
    bouquet_name VARCHAR(255) NOT NULL
        REFERENCES bouquets(name),
    quantity INT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, bouquet_name)
);

CREATE TABLE customer_flowers (
    customer_id INT NOT NULL
        REFERENCES customers(id),
    flower_name VARCHAR(255) NOT NULL
        REFERENCES flowers(name),
    quantity INT NOT NULL CHECK (quantity >= 1),
    PRIMARY KEY (customer_id, flower_name)
);

CREATE TABLE customer_bouquets (
    customer_id INT NOT NULL
        REFERENCES customers(id),
    bouquet_name VARCHAR(255) NOT NULL
        REFERENCES bouquets(name),
    quantity INT NOT NULL CHECK (quantity >= 1),
    design VARCHAR(255),
    PRIMARY KEY (customer_id, bouquet_name)
);
