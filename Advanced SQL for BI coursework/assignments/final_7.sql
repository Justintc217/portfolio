-- goal: how well each product cross sells from the other
-- data since dec 5th 2014
-- matrix row split by primary product col split by cross sell
-- step: need to find primary product id for cross sells

WITH primary_product_by_order AS (
-- get all primary items and their order_ids
SELECT
	order_id,
    order_item_id,
    is_primary_item,
    product_id AS primary_product
FROM order_items
WHERE is_primary_item=1
	AND created_at > "2014-12-05"
)
SELECT
    t2.primary_product,
    COUNT(DISTINCT t1.order_id) AS total_orders,
    COUNT(CASE WHEN t1.product_id=1 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END) AS x_sell_1,
    COUNT(CASE WHEN t1.product_id=2 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END) AS x_sell_2,
    COUNT(CASE WHEN t1.product_id=3 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END) AS x_sell_3,
    COUNT(CASE WHEN t1.product_id=4 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END) AS x_sell_4,
    COUNT(CASE WHEN t1.product_id=1 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END)
    /COUNT(DISTINCT t1.order_id) AS x_rate_1,
    COUNT(CASE WHEN t1.product_id=2 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END)
    /COUNT(DISTINCT t1.order_id) AS x_rate_2,
    COUNT(CASE WHEN t1.product_id=3 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END)
    /COUNT(DISTINCT t1.order_id) AS x_rate_3,
    COUNT(CASE WHEN t1.product_id=4 AND t1.order_item_id <> t2.order_item_id THEN t1.order_id ELSE NULL END)
    /COUNT(DISTINCT t1.order_id) AS x_rate_4
FROM order_items AS t1
	LEFT JOIN primary_product_by_order AS t2
		ON t1.order_id = t2.order_id
WHERE t1.created_at > "2014-12-05"
GROUP BY
	t2.primary_product
ORDER BY
	t2.primary_product