select sku, orderyear
from order_item, retail_order
where order_item.ordernumber = retail_order.ordernumber and orderyear=2020;


/*
select sku
from order_item
where sku in
(select sku
 from retail_order
 where ordernumber = 2000)
*/