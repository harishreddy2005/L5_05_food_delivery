"""Manage a food delivery order queue and its daily revenue."""

import json
import pickle
from datetime import datetime

orders = {}
menu = {}
VALID_STATUSES = ("placed", "cooking", "out_for_delivery", "delivered")

def create_order(customer, items, order_history=None):
    """Create a valid order and optionally append its ID to a history."""
    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name must not be empty")
    items = list(items)
    if not items:
        raise ValueError("An order must contain at least one item")
    unknown_items = [item for item in items if item not in menu]
    if unknown_items:
        raise ValueError(f"Unknown menu items: {', '.join(unknown_items)}")
    order_id = max(orders, default=0) + 1
    total = sum(menu[item] for item in items)
    orders[order_id] = {"customer": customer, "items": items, "total": total, "status": "placed"}
    if order_history is not None:
        order_history.append(order_id)
    return order_id

def update_order_status(order_id, status):
    """Update a known order to a supported delivery status."""
    if order_id not in orders:
        raise ValueError(f"Unknown order ID: {order_id}")
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid order status: {status}")
    orders[order_id]["status"] = status

def read_menu_config(file="menu.json"):
    """Load a menu, falling back when the file is missing or unreadable."""
    try:
        with open(file, encoding="utf-8") as menu_file:
            loaded_menu = json.load(menu_file)
    except (OSError, json.JSONDecodeError):
        loaded_menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
    menu.clear()
    menu.update(loaded_menu)

def daily_revenue():
    """Return the total value of delivered orders only."""
    return sum(order["total"] for order in orders.values()
               if order["status"] == "delivered")

def backup_orders(file="orders.pkl"):
    """Save the current order queue to disk."""
    with open(file, "wb") as backup_file:
        pickle.dump(orders, backup_file)

def restore_orders(file="orders.pkl"):
    """Restore the order queue from disk."""
    with open(file, "rb") as backup_file:
        restored_orders = pickle.load(backup_file)
    orders.clear()
    orders.update(restored_orders)

def print_queue():
    """Display each order and its current delivery status."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"], order["total"])

def main():
    """Demonstrate valid orders, rejected input, revenue and backups."""
    read_menu_config()
    asha_order = create_order("Asha", ["pizza", "coke"])
    ravi_order = create_order("Ravi", ["burger"])
    for customer, items in (("Ravi", ["burger", "sushi"]), ("", [])):
        try:
            create_order(customer, items)
        except ValueError as error:
            print(f"Order rejected: {error}")
    update_order_status(asha_order, "delivered")
    for order_id, status in ((ravi_order, "teleported"), (42, "delivered")):
        try:
            update_order_status(order_id, status)
        except ValueError as error:
            print(f"Status update rejected: {error}")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()

if __name__ == "__main__":
    main()
