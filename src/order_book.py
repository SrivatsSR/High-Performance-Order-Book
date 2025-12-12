from collections import defaultdict
from typing import List
from .order import Order
from .cancel_modify import CancelModifyMixin

class OrderBook(CancelModifyMixin):
    def __init__(self):
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)

    def addOrder(self, order: Order):
        if order.side == "BUY":
            self.bids[order.price].append(order)
        elif order.side == "SELL":
            self.asks[order.price].append(order)
        else:
            raise ValueError("Invalid Arguments Passed. Only BUY or SELL")

    def bestBid(self):
        if not self.bids:
            return None
        price = max(self.bids.keys())
        return price, self.bids[price]
    
    def bestAsk(self):
        if not self.asks: 
            return None
        price = min(self.asks.keys())
        return price, self.asks[price]

    def executeMarketOrder(self, side: str, quantity: int):
        filled = []

        if side == "BUY":
            book = self.asks
            price_ordering = sorted(book.keys())
        else:
            book = self.bids
            price_ordering = sorted(book.keys(), reverse=True)

        remaining = quantity

        for price in price_ordering:
            if remaining <= 0:
                break

            levelOrders = book[price]

            for order in levelOrders[:]:
                if remaining <= 0:
                    break

                tradedQty = min(remaining, order.quantity)
                filled.append((price, tradedQty))
                remaining -= tradedQty
                order.quantity -= tradedQty

                if order.quantity == 0:
                    levelOrders.remove(order)
                
            if len(levelOrders) == 0:
                del book[price]
        return filled
    
    def __repr__(self):
        bid_side = sorted(self.bids.items(), reverse=True)
        ask_side = sorted(self.asks.items())

        s = "\nORDER BOOK\n------------\nBIDS:\n"
        for p, orders in bid_side:
            s += f"{p}: {orders}\n"

        s += "\nASKS:\n"
        for p, orders in ask_side:
            s += f"{p}: {orders}\n"

        return s