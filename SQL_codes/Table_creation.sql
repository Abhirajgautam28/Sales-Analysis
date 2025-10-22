-- Sales Orders
CREATE TABLE SalesOrders (
    OrderNumber VARCHAR(20) PRIMARY KEY,
    OrderDate DATETIME,
    CustomerIndex INT,
    Channel VARCHAR(50),
    CurrencyCode VARCHAR(10),
    WarehouseCode VARCHAR(20),
    DeliveryRegionIndex INT,
    ProductDescriptionIndex INT,
    OrderQuantity INT,
    UnitPrice DECIMAL(12,2),
    LineTotal DECIMAL(15,2),
    TotalUnitCost DECIMAL(12,2)
);

-- Customers
CREATE TABLE Customers (
    CustomerIndex INT PRIMARY KEY,
    CustomerName VARCHAR(255)
);

-- Regions
CREATE TABLE Regions (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    county VARCHAR(255),
    state_code VARCHAR(10),
    state VARCHAR(100),
    type VARCHAR(50),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    area_code INT,
    population INT,
    households INT,
    median_income INT,
    land_area BIGINT,
    water_area BIGINT,
    time_zone VARCHAR(50)
);

-- State Regions
CREATE TABLE StateRegions (
    StateCode VARCHAR(10) PRIMARY KEY,
    State VARCHAR(100),
    Region VARCHAR(50)
);

-- Products
CREATE TABLE Products (
    ProductIndex INT PRIMARY KEY,
    ProductName VARCHAR(255)
);

-- 2024 Budgets
CREATE TABLE Budgets (
    ProductName VARCHAR(255) PRIMARY KEY,
    Budget2024 DECIMAL(15,2)
);
