import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import Order, OrderBook

def generate_random_orders(n: int, base_price: float = 100.0) -> list:
    """Generate random orders around a base price"""
    orders = []
    order_id = 1
    
    for _ in range(n):
        is_buy = random.random() > 0.5
        
        # Price within +/- 5% of base
        price_offset = random.uniform(-5, 5)
        price = round(base_price * (1 + price_offset/100), 2)
        
        # Quantity between 1 and 100
        quantity = random.randint(1, 100)
        
        order = Order(order_id, price, quantity, is_buy, time.time())
        orders.append(order)
        order_id += 1
    
    return orders

def benchmark_add_orders(orders: list) -> tuple:
    """Benchmark adding orders, return (time, book)"""
    book = OrderBook()
    
    start = time.perf_counter()
    for order in orders:
        book.add_order(order)
    end = time.perf_counter()
    
    return end - start, book

def benchmark_cancel_orders(book: OrderBook, order_ids: list) -> float:
    """Benchmark cancelling orders"""
    start = time.perf_counter()
    for order_id in order_ids:
        book.cancel_order(order_id)
    end = time.perf_counter()
    
    return end - start


def main():
    """Run performance benchmarks"""
    print("="*70)
    print(" " * 20 + "ORDER BOOK PERFORMANCE BENCHMARK")
    print("="*70)
    
    # Test different order quantities
    test_sizes = [1_000, 5_000, 10_000, 50_000]
    
    results = []
    
    for n in test_sizes:
        print(f"\n📊 Testing with {n:,} orders...")
        
        # Generate orders
        orders = generate_random_orders(n)
        
        # Benchmark add
        add_time, book = benchmark_add_orders(orders)
        orders_per_sec = n / add_time
        
        print(f"  ✓ Add: {add_time:.3f}s ({orders_per_sec:,.0f} orders/sec)")
        print(f"    Trades generated: {book.total_trades:,}")
        print(f"    Volume traded: {book.total_volume:,}")
        print(f"    Orders in book: {book.total_orders:,}")
        
        # Benchmark cancel (random 10% of orders)
        remaining_ids = list(book.order_map.keys())
        if remaining_ids:
            num_to_cancel = min(len(remaining_ids), n // 10)
            cancel_ids = random.sample(remaining_ids, num_to_cancel)
            cancel_time = benchmark_cancel_orders(book, cancel_ids)
            
            cancels_per_sec = num_to_cancel / cancel_time if cancel_time > 0 else 0
            print(f"  ✓ Cancel: {cancel_time:.3f}s ({cancels_per_sec:,.0f} cancels/sec)")
        
        results.append({
            'n': n,
            'add_time': add_time,
            'orders_per_sec': orders_per_sec,
            'trades': book.total_trades,
            'volume': book.total_volume
        })
    
    # Summary
    print("\n" + "="*70)
    print(" " * 25 + "PERFORMANCE SUMMARY")
    print("="*70)
    print(f"{'Orders':>10} │ {'Time':>10} │ {'Orders/sec':>15} │ {'Trades':>10}")
    print("-"*70)
    for r in results:
        print(f"{r['n']:>10,} │ {r['add_time']:>9.3f}s │ {r['orders_per_sec']:>14,.0f} │ {r['trades']:>10,}")
    
    print("\n" + "="*70)
    print("\n📈 Performance Goals:")
    print("  • Current (Python):     ~10,000-50,000 orders/sec")
    print("  • Goal Month 3:         100,000+ orders/sec (optimized Python)")
    print("  • Goal Month 9:         1,000,000+ orders/sec (C++ rewrite)")
    print("\n" + "="*70)


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    main()