-- goal: get monthly orders and refund rates for each bear products until oct 15
-- get product order quantity
-- get product refund quantity
-- refunds granular by order_item_id
-- order_items table granular by order_item_id
-- step 1: pivot grouping of order item product id 
-- step 2: pivot grouping of order item product id refund 
-- refund = does the linked order_item_id have a refund id?

SELECT
	YEAR(t1.created_at) AS yr,
    MONTH(t1.created_at) AS mo,
	SUM(t1.product_id = 1) AS p1_order_items,
	SUM(t1.product_id = 1 AND t2.order_item_refund_id IS NOT NULL)/SUM(t1.product_id = 1) AS p1_refund_rate,
	SUM(t1.product_id = 2) AS p2_order_items,
	SUM(t1.product_id = 2 AND t2.order_item_refund_id IS NOT NULL)/SUM(t1.product_id = 2) AS p2_refund_rate,
	SUM(t1.product_id = 3) AS p3_order_items,
	SUM(t1.product_id = 3 AND t2.order_item_refund_id IS NOT NULL)/SUM(t1.product_id = 3) AS p3_refund_rate,
	SUM(t1.product_id = 4) AS p4_order_items,
	SUM(t1.product_id = 4 AND t2.order_item_refund_id IS NOT NULL)/SUM(t1.product_id = 4) AS p4_refund_rate
FROM order_items AS t1
	LEFT JOIN order_item_refunds AS t2
		ON t1.order_item_id = t2.order_item_id
WHERE t1.created_at < "2014-10-15"
GROUP BY
	1,2
