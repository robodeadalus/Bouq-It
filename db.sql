CREATE DATABASE bouq_it;
\c bouq_it
CREATE TABLE customers (
    user_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    user_address VARCHAR(255) NOT NULL,
    user_barangay VARCHAR(255) NOT NULL,
    user_city VARCHAR(255) NOT NULL,
    user_zipcode VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
    payment VARCHAR(255),
    CHECK (payment IN ('G-Cash', 'Maya', 'Cash on Delivery', 'Credit/Debit Card')),
    order_address VARCHAR(255) NOT NULL,
    order_barangay VARCHAR(255) NOT NULL,
    order_city VARCHAR(255) NOT NULL,
    order_zipcode VARCHAR(255) NOT NULL,
    ordered_by INT NOT NULL,
    FOREIGN KEY (ordered_by) REFERENCES customers(user_id)
);

CREATE TABLE flowers (
    flower_name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price FLOAT (2) NOT NULL
);

CREATE TABLE bouquets (
    bouquet_name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    description TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_link TEXT NOT NULL,
    origin TEXT NOT NULL,
    meaning TEXT NOT NULL,
    price FLOAT (2) NOT NULL
);

CREATE TABLE order_flowers (
    order_id INT NOT NULL,
    flower_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 1),
    PRIMARY KEY (order_id, flower_name),
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (flower_name) REFERENCES flowers (flower_name)
);

CREATE TABLE order_bouquets (
    order_id INT NOT NULL,
    bouquet_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    design VARCHAR(255),
    CHECK (quantity >= 1),
    PRIMARY KEY (order_id, bouquet_name),
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (bouquet_name) REFERENCES bouquets (bouquet_name)
);

CREATE TABLE shops (
    shop_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
    shop_address VARCHAR(255) NOT NULL,
    shop_barangay VARCHAR(255) NOT NULL,
    shop_city VARCHAR(255) NOT NULL,
    shop_zipcode VARCHAR(255) NOT NULL,
    shop_contact VARCHAR(255) NOT NULL,
    shop_price FLOAT (2) NOT NULL
);

CREATE TABLE shop_flowers (
    shop_id INT NOT NULL,
    flower_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, flower_name),
    FOREIGN KEY (shop_id) REFERENCES shops (shop_id),
    FOREIGN KEY (flower_name) REFERENCES flowers (flower_name)
);

CREATE TABLE shop_bouquets (
    shop_id INT NOT NULL,
    bouquet_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    CHECK (quantity >= 0),
    PRIMARY KEY (shop_id, bouquet_name),
    FOREIGN KEY (shop_id) REFERENCES shops (shop_id),
    FOREIGN KEY (bouquet_name) REFERENCES bouquets (bouquet_name)
);