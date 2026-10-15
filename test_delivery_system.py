"""Regression tests for order validation, revenue and safe persistence."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import delivery_system as delivery


class DeliveryTests(unittest.TestCase):
    """Exercise the business behavior and security fixes."""

    def setUp(self):
        delivery.orders.clear()
        delivery.menu.clear()
        delivery.menu.update(pizza=250, burger=150, fries=90, coke=40)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.backup = Path(self.temp.name) / "orders.json"

    def test_order_total_history_and_item_copy(self):
        items, history = ["pizza", "coke"], []
        order_id = delivery.create_order("Asha", items, history)
        items.append("fries")
        self.assertEqual(history, [order_id])
        self.assertEqual(delivery.orders[order_id]["total"], 290)
        self.assertEqual(delivery.orders[order_id]["items"], ["pizza", "coke"])

    def test_independent_orders_without_history(self):
        first = delivery.create_order("Asha", ["pizza"])
        second = delivery.create_order("Ravi", ["burger"])
        self.assertEqual((first, second), (1, 2))

    def test_unknown_item_rejected_without_mutation(self):
        with self.assertRaises(ValueError):
            delivery.create_order("Ravi", ["sushi"])
        self.assertEqual(delivery.orders, {})

    def test_empty_customer_and_items_rejected(self):
        for customer, items in (("", ["pizza"]), ("  ", ["pizza"]),
                                ("Asha", [])):
            with self.subTest(customer=customer, items=items):
                with self.assertRaises(ValueError):
                    delivery.create_order(customer, items)
        self.assertEqual(delivery.orders, {})

    def test_status_validation(self):
        order_id = delivery.create_order("Asha", ["pizza"])
        for status in delivery.VALID_STATUSES:
            delivery.update_order_status(order_id, status)
            self.assertEqual(delivery.orders[order_id]["status"], status)
        with self.assertRaises(ValueError):
            delivery.update_order_status(order_id, "teleported")
        self.assertEqual(delivery.orders[order_id]["status"], "delivered")
        with self.assertRaises(ValueError):
            delivery.update_order_status(42, "delivered")

    def test_revenue_counts_only_delivered_orders(self):
        first = delivery.create_order("Asha", ["pizza", "coke"])
        delivery.create_order("Ravi", ["burger"])
        self.assertEqual(delivery.daily_revenue(), 0)
        delivery.update_order_status(first, "delivered")
        self.assertEqual(delivery.daily_revenue(), 290)

    def test_menu_loading_and_fallback(self):
        config = Path(self.temp.name) / "menu.json"
        delivery.read_menu_config(config)
        self.assertEqual(delivery.menu["pizza"], 250)
        config.write_text('{"salad": 120}', encoding="utf-8")
        delivery.read_menu_config(config)
        self.assertEqual(delivery.menu, {"salad": 120})
        config.write_text("invalid json", encoding="utf-8")
        delivery.read_menu_config(config)
        self.assertEqual(delivery.menu["pizza"], 250)

    def test_json_round_trip_and_next_order_id(self):
        first = delivery.create_order("Asha", ["pizza", "coke"])
        delivery.update_order_status(first, "delivered")
        expected = {
            key: value.copy() for key, value in delivery.orders.items()
        }
        delivery.backup_orders(self.backup)
        self.assertIn("1", json.loads(self.backup.read_text(encoding="utf-8")))
        delivery.orders.clear()
        delivery.restore_orders(self.backup)
        self.assertEqual(delivery.orders, expected)
        second = delivery.create_order("Ravi", ["burger"])
        self.assertEqual(second, first + 1)
        self.assertEqual(delivery.daily_revenue(), 290)

    def test_invalid_backup_preserves_existing_queue(self):
        delivery.create_order("Asha", ["pizza"])
        expected = delivery.orders.copy()
        for content in ('[]', '{"0": {}}', '{"x": {}}', '{"1": {}}',
                        'not json'):
            with self.subTest(content=content):
                self.backup.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    delivery.restore_orders(self.backup)
                self.assertEqual(delivery.orders, expected)

    def test_invalid_record_values_rejected(self):
        delivery.create_order("Asha", ["pizza"])
        valid = delivery.orders[1].copy()
        for field, value in (("total", -1), ("total", True),
                             ("total", float("inf")), ("items", []),
                             ("customer", ""), ("status", "teleported")):
            with self.subTest(field=field, value=value):
                invalid = dict(valid, **{field: value})
                self.backup.write_text(json.dumps({"1": invalid}),
                                       encoding="utf-8")
                with self.assertRaises(ValueError):
                    delivery.restore_orders(self.backup)
                self.assertEqual(delivery.orders[1], valid)

    def test_duplicate_numeric_ids_rejected(self):
        delivery.create_order("Asha", ["pizza"])
        record = delivery.orders[1]
        self.backup.write_text(json.dumps({"1": record, "01": record}),
                               encoding="utf-8")
        with self.assertRaises(ValueError):
            delivery.restore_orders(self.backup)

    def test_queue_display(self):
        delivery.create_order("Asha", ["pizza"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            delivery.print_queue()
        self.assertIn("1 Asha placed 250", output.getvalue())


if __name__ == "__main__":
    unittest.main()
