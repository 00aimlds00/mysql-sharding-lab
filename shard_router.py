import os
import time
import pymysql
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class ShardingRouter:
    def __init__(self, num_shards=5):
        self.num_shards = num_shards
        self.connections = {}

        self.db_user = "root"
        self.db_password = os.getenv("MYSQL_ROOT_PASSWORD")
        self.db_name = os.getenv("MYSQL_DATABASE")

        self.shard_config = {
            0: {"host": "localhost", "port": 3310, "user": self.db_user, "password": self.db_password, "database": self.db_name},
            1: {"host": "localhost", "port": 3311, "user": self.db_user, "password": self.db_password, "database": self.db_name},
            2: {"host": "localhost", "port": 3307, "user": self.db_user, "password": self.db_password, "database": self.db_name},
            3: {"host": "localhost", "port": 3308, "user": self.db_user, "password": self.db_password, "database": self.db_name},
            4: {"host": "localhost", "port": 3309, "user": self.db_user, "password": self.db_password, "database": self.db_name},
        }

    def get_shard_id(self, user_id):
        return user_id % self.num_shards

    def get_connection(self, shard_id):
        try:
            if shard_id not in self.connections or not self.connections[shard_id].open:
                config = self.shard_config[shard_id]
                conn = pymysql.connect(
                    host=config["host"],
                    port=config["port"],
                    user=config["user"],
                    password=config["password"],
                    database=config["database"],
                    autocommit=True
                )
                self.connections[shard_id] = conn
                print(f"✓ Connected to Shard {shard_id} (Port {config['port']})")
            return self.connections[shard_id]
        except pymysql.MySQLError as e:
            print(f"✗ Failed to connect to Shard {shard_id}: {e}")
            return None

    def insert_user(self, user_id, name, email, country):
        shard_id = self.get_shard_id(user_id)
        conn = self.get_connection(shard_id)
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO users (user_id, name, email, country)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, name, email, country))
            cursor.close()
            print(f"✓ Inserted User {user_id} into Shard {shard_id}")
            return True
        except pymysql.MySQLError as e:
            print(f"✗ Insert Error for User {user_id}: {e}")
            return False

    def find_user(self, user_id):
        shard_id = self.get_shard_id(user_id)
        conn = self.get_connection(shard_id)
        if not conn:
            return None
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except pymysql.MySQLError as e:
            print(f"✗ Search Error: {e}")
            return None

    def get_shard_stats(self):
        stats = {}
        for shard_id in range(self.num_shards):
            conn = self.get_connection(shard_id)
            if not conn:
                continue
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                stats[f"Shard {shard_id}"] = count
                cursor.close()
            except pymysql.MySQLError as e:
                print(f"✗ Stats Error on Shard {shard_id}: {e}")
        return stats

    def close_all(self):
        for conn in self.connections.values():
            if conn.open:
                conn.close()
        print("✓ All connections closed")


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE SHARDING DEMO")
    print("=" * 60)

    router = ShardingRouter()

    print("\nWaiting for databases...")
    time.sleep(5)

    print("\nTesting shard connections...")
    for i in range(5):
        router.get_connection(i)

    print("\nInserting sample users...\n")
    sample_users = [
        (1, "Alice Johnson", "alice@example.com", "USA"),
        (6, "Bob Smith", "bob@example.com", "UK"),
        (11, "Charlie Brown", "charlie@example.com", "Canada"),
        (2001, "Diana Prince", "diana@example.com", "USA"),
        (7812, "Eve Wilson", "eve@example.com", "Australia"),
    ]
    for user in sample_users:
        router.insert_user(*user)

    print("\nFinding users...\n")
    for user_id in [1, 6, 11, 2001, 7812]:
        shard_id = router.get_shard_id(user_id)
        result = router.find_user(user_id)
        if result:
            print(f"User {user_id} found in Shard {shard_id}")
            print(result)

    print("\nShard Distribution:\n")
    stats = router.get_shard_stats()
    for shard, count in stats.items():
        print(f"{shard}: {count} users")

    router.close_all()
