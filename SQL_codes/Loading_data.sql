-- Create Database
-- CREATE DATABASE IF NOT EXISTS RegionalSales;
-- USE RegionalSales;

-- Sales Orders Table
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

LOAD DATA LOCAL INFILE "D:\\Prep\\Projects\\Sales-Analysis\\Data_split\\Sales_Orders.csv"
INTO TABLE SalesOrders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Customers Table
CREATE TABLE Customers (
    CustomerIndex INT PRIMARY KEY,
    CustomerName VARCHAR(255)
);

LOAD DATA LOCAL INFILE 'C:/path/to/Customers.csv'
INTO TABLE Customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Regions Table
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

LOAD DATA LOCAL INFILE 'C:/path/to/Regions.csv'
INTO TABLE Regions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- State Regions Table
CREATE TABLE StateRegions (
    StateCode VARCHAR(10) PRIMARY KEY,
    State VARCHAR(100),
    Region VARCHAR(50)
);

LOAD DATA LOCAL INFILE 'C:/path/to/State_Regions.csv'
INTO TABLE StateRegions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Products Table
CREATE TABLE Products (
    ProductIndex INT PRIMARY KEY,
    ProductName VARCHAR(255)
);

LOAD DATA LOCAL INFILE 'C:/path/to/Products.csv'
INTO TABLE Products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Budgets Table
CREATE TABLE Budgets (
    ProductName VARCHAR(255) PRIMARY KEY,
    Budget2017 DECIMAL(15,2)
);

LOAD DATA LOCAL INFILE 'C:/path/to/2024_Budgets.csv'
INTO TABLE Budgets
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;