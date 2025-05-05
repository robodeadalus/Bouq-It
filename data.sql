-- Insert customers
INSERT INTO customers (username, email, password, last_name, first_name, middle_name, contact, address, barangay, city, zipcode)
VALUES
('johndoe', 'johndoe@example.com', 'password123', 'Doe', 'John', 'A.', '09123456789', '123 Street', 'Barangay 1', 'Manila', '1000'),
('janedoe', 'janedoe@example.com', 'password123', 'Doe', 'Jane', 'B.', '09234567890', '456 Avenue', 'Barangay 2', 'Quezon City', '1101'),
('mike88', 'mike88@example.com', 'securepass', 'Smith', 'Michael', NULL, '09345678901', '789 Road', 'Barangay 3', 'Pasig', '1600'),
('ann77', 'ann77@example.com', 'annpass', 'Johnson', 'Ann', 'C.', '09456789012', '321 Blvd', 'Barangay 4', 'Makati', '1200'),
('peterpan', 'peterpan@example.com', 'flyaway', 'Parker', 'Peter', NULL, '09567890123', '999 Circle', 'Barangay 5', 'Cebu', '6000'),
('clarkkent', 'clark@example.com', 'superman123', 'Kent', 'Clark', NULL, '09678901234', '888 Plaza', 'Barangay 6', 'Davao', '8000');

-- Insert shops
INSERT INTO shops (name, address, barangay, city, zipcode, contact, sales, image_link)
VALUES
('Rose Haven', '100 Rose St.', 'Brgy. A', 'Manila', '1000', '09981234567', 1500,'assets/bouqetShops/roseHaven.png'),
('Lily Garden', '200 Lily Ave.', 'Brgy. B', 'Quezon City', '1101', '09876543210', 2100,'assets/bouqetShops/lilyGarden.png'),
('Daisy Blooms', '300 Daisy Rd.', 'Brgy. C', 'Pasig', '1600', '09765432109', 1200,'assets/bouqetShops/daisyBlooms.png'),
('Tulip Wonderland', '400 Tulip Blvd.', 'Brgy. D', 'Makati', '1200', '09654321098', 1800,'assets/bouqetShops/tulipWonderland.png'),
('Sunflower Paradise', '500 Sunflower Circle', 'Brgy. E', 'Cebu', '6000', '09543210987', 900,'assets/bouqetShops/sunflowerParadise.jpg'),
('Orchid Emporium', '600 Orchid Plaza', 'Brgy. F', 'Davao', '8000', '09432109876', 1300,'assets/bouqetShops/orchidEmporium.png');

-- Insert flowers
INSERT INTO flowers (name, description, short_desc, image_link, origin, meaning, price)
VALUES
('Rose', 'A classic red rose symbolizing love.', 'Symbol of love.', 'assets/flowers/rose.jpg', 'France', 'Love, Passion', 150.00),
('Lily', 'A white lily that represents purity.', 'Represents purity.', 'assets/flowers/lily.jpg', 'Netherlands', 'Purity, Rebirth', 180.00),
('Daisy', 'A cheerful daisy flower.', 'Symbol of innocence.', 'assets/flowers/daisy.jpg', 'USA', 'Innocence, Joy', 120.00),
('Tulip', 'A bright and colorful tulip.', 'Symbol of perfect love.', 'assets/flowers/tulip.jpg', 'Turkey', 'Perfect Love', 200.00),
('Sunflower', 'A large sunflower symbolizing warmth.', 'Represents adoration.', 'assets/flowers/sunflower.jpg', 'Mexico', 'Adoration, Loyalty', 170.00),
('Orchid', 'A rare and exotic orchid.', 'Symbol of luxury.', 'assets/flowers/orchid.jpg', 'Philippines', 'Luxury, Beauty', 250.00);

-- Insert bouquets
INSERT INTO bouquets (name, description, short_desc, image_link, origin, meaning, price)
VALUES
('Romantic Red', 'A bouquet full of red roses.', 'Passionate love.', 'bouqets/RomanticRed.jpg', 'France', 'Love, Romance', 800.00),
('Pure Elegance', 'A mix of white lilies and orchids.', 'Elegant and pure.', 'bouqets/PureElegeance.jpg', 'Netherlands', 'Purity, Grace', 950.00),
('Sunshine Bliss', 'Sunflowers and daisies combined.', 'A cheerful bouquet.', 'bouqets/SunshineBliss.jpg', 'Mexico', 'Happiness, Warmth', 750.00),
('Tulip Dream', 'A bouquet full of colorful tulips.', 'Perfect love bouquet.', 'bouqets/TulipDream.jpg', 'Turkey', 'Love, Perfection', 870.00),
('Orchid Beauty', 'A luxurious orchid bouquet.', 'Exotic beauty.', 'bouqets/OrchidBeauty.jpg', 'Philippines', 'Luxury, Beauty', 1200.00),
('Daisy Delight', 'A fresh and joyful daisy bouquet.', 'Symbol of happiness.', 'bouqets/DaisyDelight.jpg', 'USA', 'Joy, Innocence', 650.00);

-- Insert bouquet_flowers
INSERT INTO bouquet_flowers (bouquet_name, flower_name, quantity)
VALUES
('Romantic Red', 'Rose', 12),
('Pure Elegance', 'Lily', 6),
('Pure Elegance', 'Orchid', 3),
('Sunshine Bliss', 'Sunflower', 5),
('Sunshine Bliss', 'Daisy', 7),
('Tulip Dream', 'Tulip', 10);

-- Insert orders
INSERT INTO orders (payment, address, barangay, city, zipcode, ordered_by)
VALUES
('G-Cash', '123 St.', 'Brgy. X', 'Manila', '1001', 1),
('Maya', '456 Ave.', 'Brgy. Y', 'Quezon City', '1102', 2),
('Cash on Delivery', '789 Rd.', 'Brgy. Z', 'Pasig', '1603', 3),
('Credit/Debit Card', '101 Blvd.', 'Brgy. W', 'Makati', '1204', 4),
('G-Cash', '222 Plaza', 'Brgy. V', 'Cebu', '6005', 5),
('Maya', '333 Lane', 'Brgy. U', 'Davao', '8006', 6);

-- Insert order_flowers
INSERT INTO order_flowers (order_id, flower_name, quantity)
VALUES
(1, 'Rose', 6),
(2, 'Lily', 3),
(3, 'Daisy', 10),
(4, 'Tulip', 4),
(5, 'Sunflower', 5),
(6, 'Orchid', 2);

-- Insert order_bouquets
INSERT INTO order_bouquets (order_id, bouquet_name, quantity, design)
VALUES
(1, 'Romantic Red', 1, 'Heart Shaped'),
(2, 'Pure Elegance', 1, 'Classic Wrap'),
(3, 'Sunshine Bliss', 2, 'Bright and Happy'),
(4, 'Tulip Dream', 1, 'Colorful Theme'),
(5, 'Orchid Beauty', 1, 'Luxury Pack'),
(6, 'Daisy Delight', 2, 'Simple and Sweet');

-- Insert shop_flowers
INSERT INTO shop_flowers (shop_id, flower_name, quantity)
VALUES
(1, 'Rose', 100),
(2, 'Lily', 50),
(3, 'Daisy', 80),
(4, 'Tulip', 40),
(5, 'Sunflower', 60),
(6, 'Orchid', 30);

-- Insert shop_bouquets
INSERT INTO shop_bouquets (shop_id, bouquet_name, quantity)
VALUES
(1, 'Romantic Red', 20),
(2, 'Pure Elegance', 15),
(3, 'Sunshine Bliss', 10),
(4, 'Tulip Dream', 12),
(5, 'Orchid Beauty', 8),
(6, 'Daisy Delight', 25);
