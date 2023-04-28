import pytest
from http import HTTPStatus
from django.shortcuts import resolve_url
from devpro.core.models import Author, Book

# refatorado

pytestmark = pytest.mark.django_db

list_author_url = resolve_url('core:list-authors')

# teste de integração


@pytest.fixture
def book(db):
    author = Author.objects.create(name='Luciano Ramalho')
    book = Book.objects.create(
        name='Python Fluente',
        edition=2,
        publication_year=2023,
    )
    book.authors.add(author)  # mesmo que book.authors.set([author])
    return book


def test_list_all_authors(client):
    # author = Author.objects.create(name='J.K Rowling')

    authors = Author.objects.bulk_create(Author(name=f'Author {i}') for i in range(10))
    response = client.get(list_author_url, data={'page': 2, 'page_size': 5})

    assert response.status_code == HTTPStatus.OK
    assert 5 == len(response.json()['data'])
    assert [a['name'] for a in response.json()['data']] == [a.name for a in authors[5:]]
    assert response.json()['num_pages'] == 2
    # assert response.json()['data'] == [{'id': author.id, 'name': 'J.K Rowling'}]


def test_search_author_by_name(client):
    author1 = Author.objects.create(name='J.K Rowling')

    # response = client.get(resolve_url('core:list-authors'), data={'name': 'rowling'})

    response = client.get(list_author_url, data={'name': 'rowling'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == [{'id': author1.id, 'name': 'J.K Rowling'}]


def test_search_author_by_name_without_match(client):
    Author.objects.create(name='J.K Rowling')

    response = client.get(list_author_url, data={'name': 'no match'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == []


def test_create_book(client):
    author = Author.objects.create(name='Luciano Ramalho')

    data = {
        "name": 'Python fluente',
        "edition": 1,
        "publication_year": 2002,
        "authors": [author.id]
    }
    # import ipdb;ipdb.set_trace()
    response = client.post('/api/books/', data=data, content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED
    book = Book.objects.first()
    assert book is not None
    assert response['Location'] == f'/api/books/{book.id}/'

    response_data = response.json()

    assert response_data['name'] == data['name']
    assert response_data['edition'] == data['edition']
    assert response_data['publication_year'] == data['publication_year']
    assert response_data['authors'] == [author.id]
    assert response_data['id'] == book.id
    assert 'id' in response_data


def test_read_book(client, book):
    response = client.get(f'/api/books/{book.id}/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == book.to_dict()


def test_read_unexist_book(client):
    response = client.get(f'/api/books/1/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updade_book(client, book):

    data = {
        "id": book.id,
        "name": 'Python fluente',
        "edition": 3,
        "publication_year": 2024,
        "authors": [a.id for a in book.authors.all()]
    }

    response = client.put(f'/api/books/{book.id}/', data=data, content_type='application/json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == data


def test_update_unexist_book(client):

    response = client.put(f'/api/books/1/', data={}, content_type='application/json')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_book(client, book):
    response = client.delete(f'/api/books/{book.id}/')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Book.objects.filter(pk=book.id).exists()


def test_delete_unexist_book(client):

    response = client.delete(f'/api/books/1/', data={}, content_type='application/json')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_books(client, book):
    response = client.get('/api/books/')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == [book.to_dict()]

