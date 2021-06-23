select BUYER, sum(ExtendedPrice) as totalExtendedPrice
from sku_data, order_item
where sku_data.sku = order_item.sku
group by buyer
order by totalextendedprice desc;