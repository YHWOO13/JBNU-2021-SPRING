select sku_description, max(ExtendedPrice) as revenue, orderyear
from sku_data, retail_order, order_item
where sku_data.sku = order_item.sku and order_item.ordernumber = retail_order.ordernumber and orderyear = 2020
group by sku_description, ExtendedPrice
Order bY revenue desc;