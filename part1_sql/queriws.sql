-- Part 1: monthly revenue by category
SELECT
	month,
	category,
	ROUND(SUM(quantity * unit_price), 2) AS revenue,
	COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;

-- Part 2: region-wise revenue and order count
SELECT
	r.region,
	ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
	COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY r.region;

-- Part 3: top resellers by total spend
SELECT
	o.reseller_id,
	r.reseller_name,
	ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Part 4a: resellers with no matching orders
SELECT
	r.reseller_id,
	r.reseller_name,
	r.city,
	r.region
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE o.order_id IS NULL
ORDER BY r.reseller_id;

-- Part 4b: COUNT(*) versus COUNT(order_id) for the unmatched reseller
SELECT
	r.reseller_id,
	COUNT(*) AS row_count,
	COUNT(o.order_id) AS order_id_count
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- Part 5: June delivered Average Order Value
SELECT
	ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';

-- Grand total revenue across all orders and months
SELECT
	ROUND(SUM(quantity * unit_price), 2) AS grand_total_revenue
FROM orders;
