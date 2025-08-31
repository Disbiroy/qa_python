import pytest

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def collector_with_book(collector):
    collector.add_new_book('Тестовая книга')
    return collector

@pytest.fixture
def collector_with_books(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.set_book_genre('Книга 1', 'Фантастика')
    collector.set_book_genre('Книга 2', 'Ужасы')
    return collector

@pytest.fixture
def collector_with_favorites(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.add_book_in_favorites('Книга 1')
    collector.add_book_in_favorites('Книга 2')
    return collector

class TestBooksCollector:

    @pytest.mark.parametrize('book_name, expected', [
        ('', False),
        ('A', True),
        ('A' * 40, True),
        ('A' * 41, False),
    ])
    def test_add_new_book_name_length_boundary(self, collector, book_name, expected):
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == expected

    @pytest.mark.parametrize('genre', [
        'Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'
    ])
    def test_set_book_genre_different_genres(self, collector_with_book, genre):
        collector_with_book.set_book_genre('Тестовая книга', genre)
        assert collector_with_book.get_book_genre('Тестовая книга') == genre

    @pytest.mark.parametrize('genre', ['Фантастика', 'Мультфильмы', 'Комедии'])
    def test_books_for_children_valid_genres(self, collector_with_book, genre):
        collector_with_book.set_book_genre('Тестовая книга', genre)
        children_books = collector_with_book.get_books_for_children()
        assert 'Тестовая книга' in children_books

    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_books_for_children_invalid_genres(self, collector_with_book, genre):
        collector_with_book.set_book_genre('Тестовая книга', genre)
        children_books = collector_with_book.get_books_for_children()
        assert 'Тестовая книга' not in children_books

    def test_books_for_children_no_genre(self, collector_with_book):
        children_books = collector_with_book.get_books_for_children()
        assert 'Тестовая книга' not in children_books

    def test_add_to_favorites_book_in_collection(self, collector_with_book):
        collector_with_book.add_book_in_favorites('Тестовая книга')
        assert 'Тестовая книга' in collector_with_book.favorites

    def test_add_to_favorites_book_not_in_collection(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.favorites

    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.books_genre) == 1

    def test_set_book_genre_invalid_genre(self, collector_with_book):
        collector_with_book.set_book_genre('Тестовая книга', 'Несуществующий жанр')
        assert collector_with_book.get_book_genre('Тестовая книга') == ''

    def test_get_books_with_specific_genre(self, collector_with_books):
        fantasy_books = collector_with_books.get_books_with_specific_genre('Фантастика')
        assert fantasy_books == ['Книга 1']

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        assert 'Книга для удаления' not in collector.favorites

    def test_get_book_genre_existing_book(self, collector_with_book):
        collector_with_book.set_book_genre('Тестовая книга', 'Фантастика')
        genre = collector_with_book.get_book_genre('Тестовая книга')
        assert genre == 'Фантастика'

    def test_get_book_genre_nonexistent_book(self, collector):
        genre = collector.get_book_genre('Несуществующая книга')
        assert genre == ''

    def test_get_books_genre(self, collector_with_books):
        books_genre = collector_with_books.get_books_genre()
        expected = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Ужасы'
        }
        assert books_genre == expected

    def test_get_list_of_favorites_books(self, collector_with_favorites):
        favorites = collector_with_favorites.get_list_of_favorites_books()
        assert favorites == ['Книга 1', 'Книга 2']
        assert len(favorites) == 2

    def test_get_list_of_favorites_empty(self, collector):
        favorites = collector.get_list_of_favorites_books()
        assert favorites == []