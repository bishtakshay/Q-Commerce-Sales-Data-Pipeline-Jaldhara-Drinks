USE jaldhara_db;

ALTER TABLE dim_platform
    ADD CONSTRAINT dim_platform_PK PRIMARY KEY (platform_id);

ALTER TABLE fact_sales
    ADD CONSTRAINT fact_sales_FK FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id);

ALTER TABLE dim_sku
    ADD CONSTRAINT dim_sku_PK PRIMARY KEY (internal_sku_id);  
    
ALTER TABLE dim_platform_sku_map
    ADD CONSTRAINT dim_platform_sku_map_FK1 FOREIGN KEY (internal_sku_id)
        REFERENCES dim_sku(internal_sku_id);


-- Basic QUERIES

-- Total units sold and total revenue per platform for the full date range
SELECT internal_sku_id AS SKU_ID, internal_name AS SKU_Name ,SUM(qty_sold) AS quantity_sold, SUM(mrp) AS revenue
	FROM fact_sales 
    GROUP BY internal_sku_id, internal_name
    ORDER BY quantity_sold DESC;

-- Top 10 SKUs by total quantity sold across all platforms
SELECT internal_sku_id AS SKU_ID, internal_name AS SKU_Name ,SUM(qty_sold) AS quantity_sold
	FROM fact_sales 
    GROUP BY internal_sku_id, internal_name
    ORDER BY quantity_sold DESC
    LIMIT 10;

-- Monthly revenue trend — total MRP per month across all platforms
WITH cte AS(
	SELECT platform_id, platform_sku_id, city_id, city_name, state, region, internal_sku_id,
		   status, category, internal_name, qty_sold, mrp ,DATE_FORMAT(sale_date,"%M") AS month_of_sale, MONTH(sale_date) AS month_no
		FROM fact_sales)
	SELECT month_no, month_of_sale ,SUM(mrp) AS revenue FROM cte 
		GROUP BY month_no, month_of_sale
		ORDER BY revenue DESC;
            
            
-- Total units sold per category (Lemonade, Iced Mix, Sherbet etc.)
SELECT category, SUM(qty_sold) AS qty_sold FROM fact_sales
	GROUP BY category
    ORDER BY qty_sold DESC;

-- Number of cities each SKU was sold in
SELECT internal_sku_id, internal_name, COUNT(city_id) AS no_of_city FROM fact_sales
	GROUP BY internal_sku_id, internal_name
    ORDER BY no_of_city DESC;


-- Basic QUERIES