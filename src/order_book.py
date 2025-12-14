"""
High-Performance Order Book Implementation
"""

from collections import defaultdict, deque
from typing import Dict, Deque, List, Optional, Tuple

from .order import Order
from .trade import Trade
from .matching_engine import MatchingEngine


class OrderBook:
    """
    Limit order book with price-time priority.
    
    Maintains separate bid and ask sides with FIFO queues at each price level.
    Supports adding orders, cancelling orders, and automatic order matching.
    """
    
    def __init__(self):
        """Initialize an empty order book"""
        # Price level -> Queue of orders at that price
        self.bids: Dict[float, Deque[Order]] = defaultdict(deque)
        self.asks: Dict[float, Deque[Order]] = defaultdict(deque)
        
        # Order ID -> (price, is_buy) for O(1) lookup during cancellation
        self.order_map: Dict[int, Tuple[float, bool]] = {}
        
        self.matcher = MatchingEngine()
        # Statistics
        self.total_orders = 0
        self.total_trades = 0
        self.total_volume = 0
        
    def add_order(self, order: Order) -> List[Trade]:
        """
        Add an order to the book and attempt to match.
        
        Args:
            order: Order to add to the book
            
        Returns:
            List of trades generated (empty if no matches)
        """
        if order.is_buy:
            trades = self.matcher.match_order(order, self.asks, self.order_map)
        else:
            trades = self.matcher.match_order(order, self.bids, self.order_map)
        
        # Update statistics
        for trade in trades:
            self.total_trades += 1
            self.total_volume += trade.quantity
        
        # If order has remaining quantity, add to book
        if order.quantity > 0:
            if order.is_buy:
                self.bids[order.price].append(order)
            else:
                self.asks[order.price].append(order)
            
            self.order_map[order.id] = (order.price, order.is_buy)
            self.total_orders += 1
        
        return trades
        
    def cancel_order(self, order_id: int) -> bool:
        """
        Cancel an order by ID.
        
        Args:
            order_id: Unique identifier of the order to cancel
            
        Returns:
            True if order was found and cancelled, False otherwise
        """
        # TODO: Implement proper cancellation on Day 3
        if order_id not in self.order_map:
            return False
            
        # Remove from map (lazy deletion from queues)
        del self.order_map[order_id]
        return True
        
    def get_best_bid(self) -> Optional[float]:
        """
        Get the best bid price (highest buy price).
        
        Returns:
            Best bid price or None if no bids exist
        """
        if not self.bids:
            return None
        return max(self.bids.keys())
        
    def get_best_ask(self) -> Optional[float]:
        """
        Get the best ask price (lowest sell price).
        
        Returns:
            Best ask price or None if no asks exist
        """
        if not self.asks:
            return None
        return min(self.asks.keys())
        
    def get_spread(self) -> Optional[float]:
        """
        Get the bid-ask spread.
        
        Returns:
            Spread (ask - bid) or None if market is one-sided
        """
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid is None or best_ask is None:
            return None
            
        return best_ask - best_bid
        
    def get_mid_price(self) -> Optional[float]:
        """
        Get the mid price (average of best bid and ask).
        
        Returns:
            Mid price or None if market is one-sided
        """
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid is None or best_ask is None:
            return None
            
        return (best_bid + best_ask) / 2.0
        
    def get_depth(self, levels: int = 5) -> Dict:
        """
        Get order book depth (top N price levels on each side).
        
        Args:
            levels: Number of price levels to return
            
        Returns:
            Dict with 'bids' and 'asks', each containing list of (price, quantity)
        """
        # TODO: Implement on Day 4
        pass
        
    def __repr__(self) -> str:
        """String representation of order book state"""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        spread = self.get_spread()
        
        bid_str = f"${best_bid:.2f}" if best_bid else "None"
        ask_str = f"${best_ask:.2f}" if best_ask else "None"
        spread_str = f"${spread:.2f}" if spread else "N/A"
        
        return (f"OrderBook(Bid: {bid_str}, Ask: {ask_str}, "
                f"Spread: {spread_str}, Orders: {self.total_orders}, "
                f"Trades: {self.total_trades}, Volume: {self.total_volume})")