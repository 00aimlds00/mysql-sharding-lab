import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shard_router import ShardingRouter

#import sys
sys.path.append('..')
#from shard_router import ShardingRouter
import time
import random

def generate_user_data(user_id):
    """Generate realistic user data"""
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
    last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson"]
    countries = ["USA", "UK", "Canada", "Australia", "India", "Germany", "France", "Japan", "Brazil", "Mexico"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}{user_id}@example.com"
    country = random.choice(countries)
    
    return name, email, country

def seed_data(total_users=10000):
    """Insert users into sharded database"""
    router = ShardingRouter(num_shards=5)
    
    print(f"⏳ Waiting for database containers...")
    time.sleep(5)
    
    print(f"\n📡 Connecting to shards...")
    for i in range(5):
        router.get_connection(i)
    
    print(f"\n🌱 Seeding {total_users:,} users into sharded database...")
    print(f"This will take ~30-60 seconds...\n")
    
    start_time = time.time()
    successful = 0
    failed = 0
    
    for user_id in range(1, total_users + 1):
        name, email, country = generate_user_data(user_id)
        
        if router.insert_user(user_id, name, email, country):
            successful += 1
        else:
            failed += 1
        
        # Progress indicator
        if user_id % 1000 == 0:
            elapsed = time.time() - start_time
            rate = user_id / elapsed
            print(f"  {user_id:,} users inserted ({rate:.0f} users/sec) | Failures: {failed}")
    
    end_time = time.time()
    
    print(f"\n✅ Seeding complete!")
    print(f"  Total inserted: {successful:,}")
    print(f"  Total failed: {failed}")
    print(f"  Time taken: {end_time - start_time:.2f} seconds")
    
    # Show distribution
    print(f"\n📊 Distribution across shards:")
    stats = router.get_shard_stats()
    total = sum(stats.values())
    for shard, count in sorted(stats.items()):
        percentage = (count / total * 100) if total > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"  {shard}: {count:5,} users [{bar:<50}] {percentage:5.1f}%")
    
    router.close_all()

if __name__ == "__main__":
    seed_data(10000)