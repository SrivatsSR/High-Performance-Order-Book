from src.order import Order
from src.order_book import OrderBook
from src.utils import print_book

ob = OrderBook()
ob.addOrder(Order(id=1, side="BUY", price=100, quantity=10))
ob.addOrder(Order(id=2, side="BUY", price=100, quantity=5))
ob.addOrder(Order(id=3, side="SELL", price=110, quantity=8))
ob.addOrder(Order(id=4, side="SELL", price=115, quantity=12))

print(ob)

# Execute market orders
print("\nExecuting BUY market order for 12 shares...")
print(ob.executeMarketOrder("BUY", 12))
print(ob)

print("\nExecuting SELL market order for 8 shares...")
print(ob.executeMarketOrder("SELL", 8))
print(ob)

# Add orders
ob.addOrder(Order(1, "BUY", 100, 10))
ob.addOrder(Order(2, "BUY", 101, 5))
ob.addOrder(Order(3, "SELL", 103, 8))
ob.addOrder(Order(4, "SELL", 104, 12))

print_book(ob.bids, ob.asks)

# Modify order
ob.modify_order(1, new_quantity=15)
ob.cancel_order(4)

print_book(ob.bids, ob.asks)
