import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.core.paginator import Paginator
from devpro.core.models import Author, Book
from http import HTTPStatus
from django.shortcuts import resolve_url, get_object_or_404

DEFAULT_PAGE_SIZE = 25


def authors(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

    name = request.GET.get('name')

    queryset = Author.objects.all()

    if name:
        queryset = queryset.filter(name__icontains=name)

    paginator = Paginator(queryset, per_page=page_size)

    page = paginator.get_page(page_number)

    authors = [
        a.to_dict() for a in page.object_list
    ]
    # return HttpResponse(json.dumps(authors), content_type='application/json')

    return JsonResponse({
        'data': authors,
        'count': paginator.count,
        'current_page': page_number,
        'num_pages': paginator.num_pages
    })


def book_list_create(request):
    # payload = json.load(request) # tbm daria certo
    if request.method == 'POST':
        payload = json.loads(request.body)

        authors = payload.pop('authors')

        book = Book.objects.create(**payload)

        book.authors.set(authors)

        response = JsonResponse(book.to_dict(), status=HTTPStatus.CREATED)
        response['Location'] = resolve_url(book)  # book.get_absolute_url()  ou f'/api/books/{book.id}'
        return response
    else:

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

        queryset = Book.objects.all()

        paginator = Paginator(queryset, per_page=page_size)

        page = paginator.get_page(page_number)


        # return HttpResponse(json.dumps(authors), content_type='application/json')

        return JsonResponse({
            'data': [a.to_dict() for a in page.object_list],
            'count': paginator.count,
            'current_page': page_number,
            'num_pages': paginator.num_pages
        })

    # return JsonResponse(data, safe=False)


# def book_read_update_delete(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     # read
#     if request.method == 'GET':
#         return JsonResponse(book.to_dict())
#     # update
#     elif request.method == 'PUT':
#         payload = json.load(request)
#         book.name = payload['name']
#         book.edition = payload['edition']
#         book.publication_year = payload['publication_year']
#         book.authors.set(payload['authors'])
#         book.save()
#
#         return JsonResponse(book.to_dict())
#     # delete
#     else:
#         book.delete()
#         return HttpResponse(status=HTTPStatus.NO_CONTENT)


# a view  virou um dispacth(roteador) para dividir a responsabilidade de cada ação
def book_read_update_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    handlers = {
        'GET': _book_read,
        'PUT': _book_update,
        'DELETE': _book_delete
    }

    try:
        handler = handlers[request.method]
    except KeyError:
        return HttpResponseNotAllowed

    return handler(request, book)


def _book_read(request, book):
    return JsonResponse(book.to_dict())


def _book_update(request, book):
    payload = json.load(request)
    book.name = payload['name']
    book.edition = payload['edition']
    book.publication_year = payload['publication_year']
    book.authors.set(payload['authors'])
    book.save()

    return JsonResponse(book.to_dict())


def _book_delete(request, book):
    book.delete()

    return HttpResponse(status=HTTPStatus.NO_CONTENT)
