from redis import Redis

cache = Redis(host="redis", port=6379)
cache.set("example", 5)
value = cache.get("example")
print(int(value) ** 2)