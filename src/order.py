from dataclasses import dataclass

@dataclass
class Order:
    id: int
    side: str
    price: float
    quantity: int

    def __repr__(self):
        return f"Order(id={self.id}, side={self.side}, price={self.price}, qty={self.quantity})"
