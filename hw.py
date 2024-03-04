import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)

def find_by_tag(tag: str) -> list[str | None]:
    # Check if the result is already cached
    cached_result = cache.get(tag)
    if cached_result:
        print(f'Result found in cache for tag: {tag}')
        return cached_result

    print(f'Find by tag: {tag}')
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]

    # Store result in cache
    cache.set(tag, result)

    return result

def find_by_author(author: str) -> list[str | None]:
    # Check if the result is already cached
    cached_result = cache.get(author)
    if cached_result:
        print(f'Result found in cache for author: {author}')
        return cached_result

    print(f'Find by author: {author}')
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.extend([q.quote for q in quotes])

    # Store result in cache
    cache.set(author, result)

    return result

if __name__ == '__main__':
    print(find_by_tag('li'))
    print(find_by_tag('li'))  # Should retrieve from cache

    print(find_by_author('in'))
    print(find_by_author('in'))  # Should retrieve from cache
