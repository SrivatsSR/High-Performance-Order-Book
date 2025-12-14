from typing import List,Deque
from collections import deque
import time

from .order import Order
from .trade import Trade

class MatchingEngine:
    def match_order(
        self,
        new_order: Order,
        opposite_side: dict,
        order_map: dict
    ) -> List[Trade]:
        
        trades = []
        remaining_qty = new_order.quantity

        if new_order.is_buy:
            price_levels = sorted(opposite_side.keys())
        else:
            price_levels = sorted(opposite_side.keys(), reverse=True)
        
        for price in price_levels:
            if new_order.is_buy and price > new_order.price:
                break
            
            if not new_order.is_buy and price < new_order.price:
                break

            order_queue = opposite_side[price]

            while order_queue and remaining_qty > 0:
                resting_order = order_queue[0]

                if resting_order.id not in order_map:
                    order_queue.popleft()
                    continue

                trade_qty = min(remaining_qty, resting_order.quantity)

                trade = Trade(
                    buy_order_id=new_order.id if new_order.is_buy else resting_order.id,
                    sell_order_id=resting_order.id if new_order.is_buy else new_order.id,
                    price=resting_order.price,  # Resting order price
                    quantity=trade_qty,
                    timestamp=time.time()
                )
                trades.append(trade)

                remaining_qty-= trade_qty

                resting_order.quantity-= trade_qty
                if resting_order.quantity == 0:
                    order_queue.popleft()
                    del order_map[resting_order.id]
                
            if not order_queue:
                del opposite_side[price]
            
            if remaining_qty == 0:
                break

        new_order.quantity = remaining_qty
        
        return trades