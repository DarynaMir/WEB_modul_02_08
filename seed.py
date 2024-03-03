import json
from models import Author, Quote
from mongoengine.errors import NotUniqueError

if __name__ == '__main__':
    # Load authors from JSON file
    with open('authors.json', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'),
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'),
                                description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Author exists: {el.get('fullname')}")

    # Load quotes from JSON file
    with open('quotes.json', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            author = Author.objects(fullname=el.get('author')).first()
            if author:
                quote = Quote(quote=el.get('quote'),
                              tags=el.get('tags'),
                              author=author)
                quote.save()

