from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.core.serializers import serialize

from wagtail.models import Page
from wagtail.search.models import Query

from recipe.models import RecipePage

def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 9)
    search_results_number = len(search_results)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "search_results_number": search_results_number
        },
    )

#def autocomplete_search(request):
#    search_query = request.GET.get("query", None)
#    if search_query:
#        search_results = RecipePage.objects.live().autocomplete(search_query)
#    else: 
#        return JsonResponse({"search_results": []})
#    print(search_query)
#    data = serialize("json", search_results)
#    print(data)
#    return JsonResponse({"search_results": data})
