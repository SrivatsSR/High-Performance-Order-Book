def print_book(bids, asks, depth=5):
    print("\nORDER BOOK (top levels)")
    print("BIDS                ASKS")
    print("------------------------------")

    bid_prices = sorted(bids.keys(), reverse=True)[:depth]
    ask_prices = sorted(asks.keys())[:depth]

    for bp, ap in zip(bid_prices + [None]*len(ask_prices),
                      ask_prices + [None]*len(bid_prices)):
        bid_str = f"{bp}: {sum(o.quantity for o in bids[bp])}" if bp else ""
        ask_str = f"{ap}: {sum(o.quantity for o in asks[ap])}" if ap else ""

        print(f"{bid_str:<20}{ask_str}")
    print()
