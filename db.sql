CREATE DATABASE bouq_it;
\c bouq_it
CREATE TABLE customers (
    id SERIAL NOT NULL UNIQUE PRIMARY KEY,
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
    id SERIAL NOT NULL UNIQUE PRIMARY KEY,
    payment VARCHAR(255) NOT NULL,
    CHECK (payment IN ('G-Cash', 'Maya', 'Cash on Delivery', 'Credit/Debit Card')),
    address VARCHAR(255) NOT NULL,
    barangay VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(255) NOT NULL,
    ordered_by INT NOT NULL,
    FOREIGN KEY (ordered_by) REFERENCES customers(id)
);

CREATE TABLE flowers (
    name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price FLOAT (2) NOT NULL
);

CREATE TABLE bouquets (
    name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price FLOAT (2) NOT NULL
);

CREATE TABLE bouquet_flowers (
    bouquet_name VARCHAR(255) NOT NULL,  
    flower_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 1),
    PRIMARY KEY (bouquet_name, flower_name),
    FOREIGN KEY (bouquet_name) REFERENCES bouquets (name),
    FOREIGN KEY (flower_name) REFERENCES flowers (name)
);

CREATE TABLE order_flowers (
    order_id INT NOT NULL,
    flower_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 1),
    PRIMARY KEY (order_id, flower_name),
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (flower_name) REFERENCES flowers (name)
);

CREATE TABLE order_bouquets (
    order_id INT NOT NULL,
    bouquet_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    design VARCHAR(255),
    CHECK (quantity >= 1),
    PRIMARY KEY (order_id, bouquet_name),
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (bouquet_name) REFERENCES bouquets (name)
);

CREATE TABLE shops (
    id SERIAL NOT NULL UNIQUE PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    barangay VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    sales INT NOT NULL
);

CREATE TABLE shop_flowers (
    shop_id INT NOT NULL,
    flower_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, flower_name),
    FOREIGN KEY (shop_id) REFERENCES shops (id),
    FOREIGN KEY (flower_name) REFERENCES flowers (name)
);

CREATE TABLE shop_bouquets (
    shop_id INT NOT NULL,
    bouquet_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, bouquet_name),
    FOREIGN KEY (shop_id) REFERENCES shops (id),
    FOREIGN KEY (bouquet_name) REFERENCES bouquets (name)
);