from .order import Order
from dataclasses import dataclass

class OrderNotFound(Exception):
    pass

class CancelModifyMixin:
    def cancel_order(self, order_id: int):
        for price,order in self.bids.items():
            for o in order:
                if o.id == order_id:
                    order.remove(o)
                    return True
        
        for price,order in self.asks.items():
            for o in order:
                if o.id == order_id:
                    order.remove(o)
                    return True
                
        raise OrderNotFound(f"Order {order_id} not found")
    
    def modify_order(self, order_id: int, new_price=None, new_quantity=None):
        for books in (self.asks, self.bids):
            for price, orders in books.items():
                for o in orders:
                    if(o.id == order_id):
                        if new_price is not None:
                            o.price = new_price
                        if new_quantity is not None:
                            o.quantity = new_quantity
                        return o
                    
        raise OrderNotFound(f"Order {order_id} not found")