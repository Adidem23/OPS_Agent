import os
import psycopg2
import logging
from statistics import mean
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger("OPS_ENGINE")

class Database:

    def __init__(self):

        load_dotenv()

        password = os.getenv("DB_PASSWORD")

        self.conn = psycopg2.connect(
            f"postgresql://postgres.lmyqoumqhetgznztbnjg:{password}"
            "@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"
        )

        self.conn.autocommit = False

        logger.info("Database connected")

    def query(self, sql, params=None):

        try:

            with self.conn.cursor() as cur:

                cur.execute(sql, params)

                rows = cur.fetchall()

            self.conn.commit()

            return rows

        except Exception as e:

            logger.error(f"Query failed: {e}")

            self.conn.rollback()

            return []



class SchemaInspector:

    def __init__(self, db):

        self.db = db

        self.cache = {}

    def get_columns(self, table):

        if table in self.cache:
            return self.cache[table]

        rows = self.db.query(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table}'
        """)

        cols = {r[0] for r in rows}

        self.cache[table] = cols

        return cols


class SignalDetector:

    @staticmethod
    def detect(data):

        if not data:
            return []

        values = list(data.values())

        if len(values) < 2:
            return []

        avg = mean(values)

        signals = []

        for k, v in data.items():

            if v > avg * 1.5 or v < avg * 0.5:

                signals.append({
                    "dimension": k,
                    "value": v,
                    "avg": avg,
                    "severity": round(abs(v - avg) / avg, 3)
                })

        return signals


class TableAnalyzer:

    def __init__(self, db, schema):

        self.db = db
        self.schema = schema

    def build_scope(self, table, scope):

        columns = self.schema.get_columns(table)

        filters = []

        params = []

        for k, v in scope.items():

            if k in columns:

                filters.append(f"{k}=%s")

                params.append(v)

        if not filters:
            return "", []

        return "WHERE " + " AND ".join(filters), params


    def row_count(self, table, where_sql, params):

        rows = self.db.query(
            f"SELECT COUNT(*) FROM {table} {where_sql}",
            params
        )

        return rows[0][0] if rows else 0


    def breakdown(self, table, column, where_sql, params):

        columns = self.schema.get_columns(table)

        if column not in columns:
            return {}

        rows = self.db.query(
            f"""
            SELECT {column}, COUNT(*)
            FROM {table}
            {where_sql}
            GROUP BY {column}
            """,
            params
        )

        result = {}

        for r in rows:

            key = str(r[0])

            result[key] = int(r[1])

        return result



class InvestigationEngine:

    TABLES = {
        "raw_order_events": ["region","city","sku_id","event_type"],
        "raw_payment_events": ["payment_status","payment_method"],
        "raw_shipment_events": ["courier_name","event_type","region"],
        "raw_inventory_events": ["event_type"],
        "raw_return_events": ["return_reason","return_status"],
        "raw_user_events": ["event_type","device_type","region"]
    }

    def __init__(self):

        self.db = Database()

        self.schema = SchemaInspector(self.db)

        self.analyzer = TableAnalyzer(self.db, self.schema)


    def analyze_table(self, table, dimensions, scope):

        where_sql, params = self.analyzer.build_scope(table, scope)

        result = {}

        result["kci"] = {
            "rows": self.analyzer.row_count(
                table,
                where_sql,
                params
            )
        }

        dims = {}

        signals = {}

        for col in dimensions:

            data = self.analyzer.breakdown(
                table,
                col,
                where_sql,
                params
            )

            dims[col] = data

            signals[col] = SignalDetector.detect(data)

        result["dimensions"] = dims

        result["signals"] = signals

        return result


    def run(self, scope):

        logger.info(f"Running investigation with scope: {scope}")

        report = {"scope": scope}

        for table, dims in self.TABLES.items():

            report[table] = self.analyze_table(
                table,
                dims,
                scope
            )

        return report


# if __name__ == "__main__":

#     engine = InvestigationEngine()

#     report = engine.run({
#         "region": "West India",
#         "courier_name": "Delhivery"
#     })

#     print(report)