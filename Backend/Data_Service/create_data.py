import os
import random
import uuid
import psycopg2
import logging
import time
from dotenv import load_dotenv


class OpsDataGenerator:

    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )

        self.logger = logging.getLogger("OPS-DATA-GENERATOR")

        load_dotenv()

        db_password = os.getenv("DB_PASSWORD")

        self.conn = psycopg2.connect(
            f"postgresql://postgres.lmyqoumqhetgznztbnjg:{db_password}"
            "@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"
        )

        self.cursor = self.conn.cursor()

        self.logger.info("Connected to Supabase successfully")

        self._load_static_data()

    # -------------------------------------
    # Static data
    # -------------------------------------

    def _load_static_data(self):

        self.regions = ["West India", "North India", "South India", "East India"]

        self.cities_by_region = {
            "West India": ["Mumbai", "Pune", "Ahmedabad"],
            "North India": ["Delhi", "Jaipur"],
            "South India": ["Bangalore", "Chennai"],
            "East India": ["Kolkata", "Bhubaneswar"]
        }

        self.couriers = ["Delhivery", "BlueDart", "EcomExpress", "DTDC"]

        self.payment_methods = [
            "UPI", "Credit Card", "Debit Card", "Net Banking"
        ]

        self.devices = ["mobile", "desktop", "tablet"]

        self.order_events = [
            "order_created",
            "order_confirmed",
            "order_cancelled",
            "order_shipped",
            "order_delivered"
        ]

        self.shipment_events = [
            "shipment_created",
            "shipment_dispatched",
            "in_transit",
            "delivery_attempted",
            "delivered",
            "delivery_failed"
        ]

        self.inventory_events = [
            "stock_added",
            "stock_reserved",
            "stock_released",
            "stockout",
            "replenishment"
        ]

        self.payment_status = ["success", "failed", "timeout", "pending"]

        self.return_status = [
            "return_requested",
            "return_approved",
            "return_completed"
        ]

        self.user_events = [
            "product_view",
            "add_to_cart",
            "checkout_started",
            "checkout_abandoned"
        ]

    # -------------------------------------
    # Helpers
    # -------------------------------------

    def uid(self):
        return str(uuid.uuid4())

    def random_region_city(self):
        region = random.choice(self.regions)
        city = random.choice(self.cities_by_region[region])
        return region, city

    def random_delay(self):
        time.sleep(random.uniform(0.01, 0.1))

    # -------------------------------------
    # Order event
    # -------------------------------------

    def insert_order_event(self, order_id):

        region, city = self.random_region_city()

        quantity = random.randint(1, 5)

        order_value = round(random.uniform(200, 7000), 2)

        self.cursor.execute(
            """
            INSERT INTO raw_order_events
            (order_id, customer_id, sku_id, quantity, order_value, region, city, warehouse_id, event_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                order_id,
                self.uid(),
                self.uid(),
                quantity,
                order_value,
                region,
                city,
                self.uid(),
                random.choice(self.order_events)
            )
        )

    # -------------------------------------
    # Payment event
    # -------------------------------------

    def insert_payment_event(self, order_id):

        status = random.choices(
            self.payment_status,
            weights=[75, 10, 10, 5]
        )[0]

        failure_reason = None

        if status == "failed":
            failure_reason = random.choice([
                "gateway_error",
                "insufficient_balance",
                "bank_declined"
            ])

        self.cursor.execute(
            """
            INSERT INTO raw_payment_events
            (payment_id, order_id, payment_method, amount, payment_status, failure_reason)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                self.uid(),
                order_id,
                random.choice(self.payment_methods),
                round(random.uniform(200, 7000), 2),
                status,
                failure_reason
            )
        )

    # -------------------------------------
    # Shipment event
    # -------------------------------------

    def insert_shipment_event(self, order_id):

        region, city = self.random_region_city()

        self.cursor.execute(
            """
            INSERT INTO raw_shipment_events
            (shipment_id, order_id, courier_name, warehouse_id, region, city, event_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                self.uid(),
                order_id,
                random.choice(self.couriers),
                self.uid(),
                region,
                city,
                random.choice(self.shipment_events)
            )
        )

    # -------------------------------------
    # Inventory event
    # -------------------------------------

    def insert_inventory_event(self):

        self.cursor.execute(
            """
            INSERT INTO raw_inventory_events
            (sku_id, warehouse_id, event_type, quantity_change, stock_after_event)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                self.uid(),
                self.uid(),
                random.choice(self.inventory_events),
                random.randint(-25, 80),
                random.randint(0, 700)
            )
        )

    # -------------------------------------
    # Return event
    # -------------------------------------

    def insert_return_event(self, order_id):

        self.cursor.execute(
            """
            INSERT INTO raw_return_events
            (order_id, sku_id, return_reason, return_status)
            VALUES (%s,%s,%s,%s)
            """,
            (
                order_id,
                self.uid(),
                random.choice([
                    "damaged",
                    "wrong_item",
                    "not_needed",
                    "size_issue"
                ]),
                random.choice(self.return_status)
            )
        )

    # -------------------------------------
    # User event
    # -------------------------------------

    def insert_user_event(self):

        region, _ = self.random_region_city()

        self.cursor.execute(
            """
            INSERT INTO raw_user_events
            (user_id, sku_id, region, device_type, event_type)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                self.uid(),
                self.uid(),
                region,
                random.choice(self.devices),
                random.choice(self.user_events)
            )
        )

    # -------------------------------------
    # Batch generation
    # -------------------------------------

    def generate_batch(self):

        order_count = random.randint(40, 100)
        inventory_count = random.randint(10, 35)

        self.logger.info(f"Generating {order_count} order flows")

        for _ in range(order_count):

            order_id = self.uid()

            self.insert_order_event(order_id)
            self.insert_payment_event(order_id)
            self.insert_shipment_event(order_id)

            if random.random() < 0.15:
                self.insert_return_event(order_id)

            if random.random() < 0.7:
                self.insert_user_event()

            self.random_delay()

        self.logger.info(f"Generating {inventory_count} inventory updates")

        for _ in range(inventory_count):
            self.insert_inventory_event()

        self.conn.commit()

        self.logger.info("Batch committed successfully")

    # -------------------------------------
    # Close
    # -------------------------------------

    def close(self):

        self.cursor.close()
        self.conn.close()

        self.logger.info("Database connection closed")

# if __name__ == "__main__":

#     generator = OpsDataGenerator()

#     try:

#         start = time.time()

#         generator.generate_batch()

#         end = time.time()

#         generator.logger.info(
#             f"Batch completed in {round(end-start,2)} seconds"
#         )

#     except Exception as e:

#         generator.logger.error(f"Generator error: {e}")

#     finally:

#         generator.close()