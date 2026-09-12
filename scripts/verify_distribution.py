import sys
sys.path.append('..')
from shard_router import ShardingRouter

def verify_distribution():
    """Verify data is evenly distributed across shards"""
    router = ShardingRouter(num_shards=5)
    
    print("🔍 Verifying data distribution across shards...\n")
    
    # Connect to all shards
    for i in range(5):
        router.get_connection(i)
    
    # Get statistics
    stats = router.get_shard_stats()
    total = sum(stats.values())
    
    print("Distribution Summary:")
    print("-" * 60)
    for shard, count in sorted(stats.items()):
        expected_percentage = 20.0  # 100% / 5 shards
        actual_percentage = (count / total * 100) if total > 0 else 0
        deviation = abs(actual_percentage - expected_percentage)
        
        status = "✓" if deviation < 2 else "⚠"
        print(f"{status} {shard}: {count:6,} users ({actual_percentage:5.1f}%) [Expected: {expected_percentage}%]")
    
    print("-" * 60)
    print(f"Total users: {total:,}")
    
    # Sample user locations
    print("\n📍 Sample user-to-shard mapping:")
    sample_ids = [1, 100, 500, 1000, 5000, 10000]
    for user_id in sample_ids:
        shard_id = router.get_shard_id(user_id)
        user = router.find_user(user_id)
        if user:
            print(f"  User {user_id:5} → Shard {shard_id}: {user['name']}")
    
    router.close_all()

if __name__ == "__main__":
    verify_distribution()