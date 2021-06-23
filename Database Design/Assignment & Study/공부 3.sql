select sku_description, max(Price) as Price
from sku_data, retail_order, order_item
where sku_data.sku = order_item.sku and order_item.ordernumber = retail_order.ordernumber
Order bY Price desc;