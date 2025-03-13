-- Insert sample customers
INSERT INTO customers (username, email, password, last_name, first_name, middle_name, contact, address, barangay, city, zipcode)
VALUES
('jdoe', 'jdoe@example.com', 'hashedpassword123', 'Doe', 'John', 'A.', '09123456789', '123 Main St', 'Barangay 1', 'Manila', '1000'),
('asmith', 'asmith@example.com', 'hashedpassword456', 'Smith', 'Alice', 'B.', '09129876543', '456 Elm St', 'Barangay 2', 'Quezon City', '1100');

INSERT INTO flowers (name, description, short_desc, image_link, origin, meaning, price) VALUES
('Rose', 'A beautiful red flower symbolizing love and passion.', 'Symbol of love.', 'https://example.com/rose.jpg', 'Europe', 'Love and Passion', 150.00),
('Tulip', 'A vibrant spring flower available in many colors.', 'Bright and cheerful.', 'https://example.com/tulip.jpg', 'Netherlands', 'Perfect Love', 120.00),
('Sunflower', 'A tall, bright yellow flower that follows the sun.', 'Represents warmth and happiness.', 'https://example.com/sunflower.jpg', 'North America', 'Loyalty and Adoration', 100.00),
('Lily', 'An elegant flower with a strong fragrance.', 'Represents purity and devotion.', 'https://example.com/lily.jpg', 'Asia', 'Purity and Renewal', 180.00),
('Orchid', 'A unique and exotic flower with many varieties.', 'Symbolizes luxury and strength.', 'https://example.com/orchid.jpg', 'Tropics', 'Beauty and Strength', 250.00),
('Daisy', 'A small white flower with a yellow center.', 'Represents innocence and purity.', 'https://example.com/daisy.jpg', 'Europe', 'Innocence and Cheerfulness', 90.00),
('Peony', 'A large, fragrant flower popular in weddings.', 'Symbolizes romance and prosperity.', 'https://example.com/peony.jpg', 'China', 'Romance and Wealth', 200.00),
('Cherry Blossom', 'A delicate pink flower that blooms in spring.', 'Represents the beauty of life.', 'https://example.com/cherryblossom.jpg', 'Japan', 'Renewal and Transience', 170.00),
('Carnation', 'A ruffled flower available in many colors.', 'Represents admiration and affection.', 'https://example.com/carnation.jpg', 'Mediterranean', 'Love and Admiration', 110.00),
('Hydrangea', 'A lush, globe-like flower with many petals.', 'Symbolizes gratitude and understanding.', 'https://example.com/hydrangea.jpg', 'Japan', 'Gratitude and Understanding', 140.00);


-- Insert sample bouquets
INSERT INTO bouquets (name, description, short_desc, image_link, origin, meaning, price)
VALUES
('Romantic Red', 'A bouquet of red roses', 'Perfect for Valentine''s', 'https://example.com/romantic_red.jpg', 'Mixed', 'Love and romance', 500.00),
('Spring Delight', 'A mix of colorful tulips', 'Brightens any day', 'https://example.com/spring_delight.jpg', 'Mixed', 'Joy and freshness', 450.00);

-- Insert bouquet flowers
INSERT INTO bouquet_flowers (bouquet_name, flower_name, quantity)
VALUES
('Romantic Red', 'Rose', 12),
('Spring Delight', 'Tulip', 10);

-- Insert sample orders
INSERT INTO orders (payment, address, barangay, city, zipcode, ordered_by)
VALUES
('G-Cash', '789 Maple St', 'Barangay 3', 'Pasig', '1600', 1),
('Cash on Delivery', '567 Oak St', 'Barangay 4', 'Makati', '1200', 2);

-- Insert order flowers
INSERT INTO order_flowers (order_id, flower_name, quantity)
VALUES
(1, 'Rose', 5),
(2, 'Tulip', 7);

-- Insert order bouquets
INSERT INTO order_bouquets (order_id, bouquet_name, quantity, design)
VALUES
(1, 'Romantic Red', 1, 'Classic'),
(2, 'Spring Delight', 2, 'Minimalist');

-- Insert sample shops
INSERT INTO shops (name, address, barangay, city, zipcode, contact, price)
VALUES
('Flower Haven', '101 Garden St', 'Barangay 5', 'Taguig', '1630', '09987654321', 300.00),
('Bloom Boutique', '202 Blossom Ave', 'Barangay 6', 'Mandaluyong', '1550', '09876543210', 280.00);

-- Insert shop flowers
INSERT INTO shop_flowers (shop_id, flower_name, quantity)
VALUES
(1, 'Rose', 50),
(2, 'Tulip', 30);

-- Insert shop bouquets
INSERT INTO shop_bouquets (shop_id, bouquet_name, quantity)
VALUES
(1, 'Romantic Red', 5),
(2, 'Spring Delight', 3);
