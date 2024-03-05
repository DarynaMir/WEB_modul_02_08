from models import Author, Quote


def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def find_by_author(author: str) -> list[str | None]:
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.extend([q.quote for q in quotes])
    return result


def find_by_tags(tags: str) -> list[str | None]:
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    result = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    while True:
        command = input('Введіть команду (name/author/tag/tags/exit): ').strip().lower()

        if command == 'exit':
            print('Завершення роботи програми.')
            break

        if command == 'name':
            author_name = input('Введіть ім\'я автора: ').strip()
            quotes = find_by_author(author_name)
            print(quotes)

        elif command == 'tag':
            tag = input('Введіть тег: ').strip()
            quotes = find_by_tag(tag)
            print(quotes)

        elif command == 'tags':
            tags = input('Введіть набір тегів через кому (без пробілів): ').strip()
            quotes = find_by_tags(tags)
            print(quotes)

        else:
            print('Неправильна команда. Будь ласка, спробуйте ще раз.')
