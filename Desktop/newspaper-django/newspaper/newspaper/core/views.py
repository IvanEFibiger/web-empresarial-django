from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def index(request):
    # Obtener todos los artículos ordenados por fecha de publicación más reciente
    articles = Article.objects.filter(is_important=True).order_by('-published_date')

    # Paginador: 4 artículos por página
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Artículo destacado
    featured_article = Article.objects.filter(is_featured=True).order_by('-published_date').first()

    # Filtrar artículos por categoría (4 artículos por cada una)
    categories = ['Mundo', 'Nacionales', 'Deportes', 'Policiales', 'Varias']
    articles_by_category = {}
    for category_name in categories:
        category = Category.objects.get(name=category_name)
        articles_by_category[category_name] = Article.objects.filter(category=category).order_by('-published_date')[:3]

    return render(request, 'index.html', {
        'page': page,  # Página actual para los artículos paginados
        'featured_article': featured_article,  # Artículo destacado
        'articles_by_category': articles_by_category,  # Artículos por categoría
    })


def category_detail(request, category_name):
    # Obtener la categoría específica
    category = get_object_or_404(Category, name=category_name)
    articles = Article.objects.filter(category=category).order_by('-published_date')

    # Paginador: 4 artículos por página
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'secciones.html', {
        'category': category,
        'page': page,
    })



def article_detail(request, id):
    # Obtener el artículo correspondiente usando el ID
    article_detail = get_object_or_404(Article, id=id)
    return render(request, 'articulo.html', {'article_detail': article_detail})

