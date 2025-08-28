import pytest

class TestBooksCollector:

    @pytest.mark.parametrize('book_name, expected', [
        ('', False),
        ('A', True),
        ('A' * 40, True),
        ('A' * 41, False),
    ])
    def test_add_new_book_name_length_boundary(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == expected

    @pytest.mark.parametrize('genre', [
        'Фантастика',
        'Ужасы',
        'Детективы',
        'Мультфильмы',
        'Комедии'
    ])
    def test_set_book_genre_different_genres(self, genre):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', genre)
        assert collector.get_book_genre('Тестовая книга') == genre

    @pytest.mark.parametrize('genre, is_for_children', [
        ('Фантастика', True),
        ('Ужасы', False),
        ('Детективы', False),
        ('Мультфильмы', True),
        ('Комедии', True),
        ('', True)
    ])
    def test_books_for_children_age_rating(self, genre, is_for_children):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        if genre:
            collector.set_book_genre('Тестовая книга', genre)
        children_books = collector.get_books_for_children()
        assert ('Тестовая книга' in children_books) == is_for_children

    @pytest.mark.parametrize('book_in_collection, expected', [
        (True, True),
        (False, False)
    ])
    def test_add_to_favorites_depending_on_collection(self, book_in_collection, expected):
        collector = BooksCollector()
        if book_in_collection:
            collector.add_new_book('Тестовая книга')
        collector.add_book_in_favorites('Тестовая книга')
        assert ('Тестовая книга' in collector.favorites) == expected

    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.books_genre) == 1

    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Анна Каренина')
        collector.set_book_genre('Анна Каренина', 'Несуществующий жанр')
        assert collector.get_book_genre('Анна Каренина') == ''

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Ужасы')
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert fantasy_books == ['Книга 1']

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        assert 'Книга для удаления' not in collector.favorites