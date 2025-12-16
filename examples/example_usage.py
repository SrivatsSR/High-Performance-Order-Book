"""
Basic usage example for the order book.
"""

import sys
from pathlib import Path
import time
from src import Order, OrderBook

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    print("=" * 70)
    print(" " * 20 + "ORDER BOOK WITH MATCHING")
    print("=" * 70)
    
    book = OrderBook()
    order_id = 1

    print("\n SCENARIO 1: Building the book (no matches expected)")
    print("-" * 70)

    orders = [
        Order(order_id, 99.0, 10, True, time.time()),   # Buy 10 @ $99
        Order(order_id+1, 100.0, 15, True, time.time()), # Buy 15 @ $100
        Order(order_id+2, 101.0, 20, True, time.time()), # Buy 20 @ $101
        Order(order_id+3, 103.0, 25, False, time.time()),# Sell 25 @ $103
        Order(order_id+4, 104.0, 30, False, time.time()),# Sell 30 @ $104
    ]

    order_id += 5
    
    for order in orders:
        trades = book.add_order(order)
        print(f"  Added {order} → {len(trades)} trades")

    print(f"\n  {book}")
    print(f"  Spread: ${book.get_spread():.2f}")

    print("\n SCENARIO 2: Aggressive buy order crosses the spread")
    print("-" * 70)
    
    aggressive_buy = Order(order_id, 103.5, 30, True, time.time())
    order_id += 1
    print(f"  Incoming: {aggressive_buy}")
    
    trades = book.add_order(aggressive_buy)
    
    print(f"\n  Generated {len(trades)} trade(s):")
    for i, trade in enumerate(trades, 1):
        print(f"     Trade {i}: {trade}")
    
    print(f"\n  {book}")
    print(f"  New spread: ${book.get_spread():.2f}")

    print("\n SCENARIO 3: Large sell order hits multiple bid levels")
    print("-" * 70)
    
    aggressive_sell = Order(order_id, 98.0, 50, False, time.time())
    order_id += 1
    print(f"  Incoming: {aggressive_sell}")
    
    trades = book.add_order(aggressive_sell)
    
    print(f"\n  Generated {len(trades)} trade(s):")
    total_traded = 0
    for i, trade in enumerate(trades, 1):
        print(f"     Trade {i}: {trade}")
        total_traded += trade.quantity
    
    print(f"\n  Total quantity traded: {total_traded}")
    print(f"  Remaining from sell order: {aggressive_sell.quantity}")
    
    print(f"\n  {book}")

    print("\n SCENARIO 4: Partial fill scenario")
    print("-" * 70)
    
    # Add some liquidity
    book.add_order(Order(order_id, 102.0, 5, False, time.time()))
    order_id += 1
    
    partial_buy = Order(order_id, 102.0, 10, True, time.time())
    order_id += 1
    print(f"  Incoming: {partial_buy} (but only 5 available)")
    
    trades = book.add_order(partial_buy)
    
    print(f"\n  Generated {len(trades)} trade(s):")
    for trade in trades:
        print(f"     {trade}")
    
    print(f"\n  Order partially filled: {10 - partial_buy.quantity}/10 filled")
    print(f"  Remaining {partial_buy.quantity} added to book")
    
    print(f"\n Final State: {book}")
    
    # Summary
    print("\n" + "=" * 70)
    print(" " * 25 + "SUMMARY")
    print("=" * 70)
    print(f"  Total Orders Added: {order_id}")
    print(f"  Total Trades: {book.total_trades}")
    print(f"  Total Volume: {book.total_volume}")
    
    print("\n" + "="*70)
    print(" " * 25 + "FINAL ORDER BOOK DEPTH")
    print("="*70)
    
    book.print_depth(levels=10)

if __name__ == "__main__":
    main()