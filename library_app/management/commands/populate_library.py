from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library_app.models import Author, Genre, Book, Reader
from datetime import date
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем заполнение базы данных...')

        # Создаем жанры
        genres_data = [
            'Фантастика', 'Детектив', 'Роман', 'Приключения',
            'Научная литература', 'История', 'Биография', 'Поэзия'
        ]

        genres = []
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                defaults={'description': f'Описание жанра {genre_name}'}
            )
            genres.append(genre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Создан жанр: {genre_name}'))

        # Создаем авторов
        authors_data = [
            {'first_name': 'Александр', 'last_name': 'Пушкин', 'birth_date': date(1799, 6, 6)},
            {'first_name': 'Лев', 'last_name': 'Толстой', 'birth_date': date(1828, 9, 9)},
            {'first_name': 'Федор', 'last_name': 'Достоевский', 'birth_date': date(1821, 11, 11)},
            {'first_name': 'Агата', 'last_name': 'Кристи', 'birth_date': date(1890, 9, 15)},
            {'first_name': 'Артур', 'last_name': 'Конан Дойл', 'birth_date': date(1859, 5, 22)},
            {'first_name': 'Джордж', 'last_name': 'Оруэлл', 'birth_date': date(1903, 6, 25)},
            {'first_name': 'Рэй', 'last_name': 'Брэдбери', 'birth_date': date(1920, 8, 22)},
            {'first_name': 'Джоан', 'last_name': 'Роулинг', 'birth_date': date(1965, 7, 31)},
        ]

        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                defaults={
                    'birth_date': author_data['birth_date'],
                    'biography': f'Великий русский поэт и писатель {author_data["first_name"]} {author_data["last_name"]}. Автор множества известных произведений.'
                }
            )
            authors.append(author)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан автор: {author_data["last_name"]} {author_data["first_name"]}'))

        # Создаем книги
        books_data = [
            {'title': 'Евгений Онегин', 'author_idx': 0, 'year': 1833, 'pages': 389, 'genre_idxs': [2], 'rating': 9.5},
            {'title': 'Война и мир', 'author_idx': 1, 'year': 1869, 'pages': 1225, 'genre_idxs': [2, 5], 'rating': 9.8},
            {'title': 'Преступление и наказание', 'author_idx': 2, 'year': 1866, 'pages': 671, 'genre_idxs': [2, 1],
             'rating': 9.6},
            {'title': 'Десять негритят', 'author_idx': 3, 'year': 1939, 'pages': 256, 'genre_idxs': [1], 'rating': 9.2},
            {'title': 'Шерлок Холмс', 'author_idx': 4, 'year': 1892, 'pages': 307, 'genre_idxs': [1, 3], 'rating': 9.4},
            {'title': '1984', 'author_idx': 5, 'year': 1949, 'pages': 328, 'genre_idxs': [0, 4], 'rating': 9.7},
            {'title': '451 градус по Фаренгейту', 'author_idx': 6, 'year': 1953, 'pages': 256, 'genre_idxs': [0],
             'rating': 9.3},
            {'title': 'Гарри Поттер и философский камень', 'author_idx': 7, 'year': 1997, 'pages': 332,
             'genre_idxs': [0, 3], 'rating': 9.1},
            {'title': 'Анна Каренина', 'author_idx': 1, 'year': 1877, 'pages': 864, 'genre_idxs': [2], 'rating': 9.7},
            {'title': 'Идиот', 'author_idx': 2, 'year': 1869, 'pages': 656, 'genre_idxs': [2], 'rating': 9.5},
            {'title': 'Мастер и Маргарита', 'author_idx': 2, 'year': 1967, 'pages': 480, 'genre_idxs': [2, 0],
             'rating': 9.9},
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': authors[book_data['author_idx']],
                    'publication_year': book_data['year'],
                    'pages': book_data['pages'],
                    'isbn': f'978-{random.randint(1000000000, 9999999999)}',
                    'description': f'Захватывающая книга "{book_data["title"]}" - классическое произведение мировой литературы.',
                    'available_copies': random.randint(1, 5),
                    'rating': book_data['rating']
                }
            )
            if created:
                for genre_idx in book_data['genre_idxs']:
                    book.genre.add(genres[genre_idx])
                self.stdout.write(self.style.SUCCESS(f'✓ Создана книга: {book_data["title"]}'))

        # Создаем тестовых пользователей
        test_users = [
            {'username': 'reader1', 'email': 'reader1@example.com', 'password': 'reader123', 'first_name': 'Иван',
             'last_name': 'Шакаева'},
            {'username': 'reader2', 'email': 'reader2@example.com', 'password': 'reader123', 'first_name': 'Петр',
             'last_name': 'Петров'},
            {'username': 'reader3', 'email': 'reader3@example.com', 'password': 'reader123', 'first_name': 'Мария',
             'last_name': 'Гагарин'},
        ]

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()

                # Создаем профиль читателя
                Reader.objects.create(
                    user=user,
                    phone=f'+7 (999) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                    address=f'г. Москва, ул. {random.choice(["Ленина", "Пушкина", "Гагарина", "Советская"])} д.{random.randint(1, 100)}',
                    date_of_birth=date(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28))
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан пользователь: {user_data["username"]} (пароль: reader123)'))

        self.stdout.write(self.style.SUCCESS('\n=== База данных успешно заполнена! ==='))
        self.stdout.write(self.style.SUCCESS('Тестовые пользователи:'))
        self.stdout.write(self.style.SUCCESS('  reader1 / reader123'))
        self.stdout.write(self.style.SUCCESS('  reader2 / reader123'))
        self.stdout.write(self.style.SUCCESS('  reader3 / reader123'))