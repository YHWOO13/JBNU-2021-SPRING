select ordernumber, sum(extendedprice) as best_selling
from order_item oi
where ordernumber in
(select ordernumber 
from retail_order
where orderyear =2020)
group by ordernumber;