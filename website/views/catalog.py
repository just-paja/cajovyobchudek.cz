from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render


mapping = {
    'caj': {
        'name': 'Čaj',
        'template': 'tea.html'
    },
    'kava': {
        'name': 'Káva',
        'template': 'coffee.html',
    },
    'orechy': {
        'name': 'Ořechy',
        'template': 'nuts.html',
    },
    'susene-ovoce': {
        'name': 'Sušené ovoce',
        'template': 'dried-fruit.html',
    },
    'vazene-bonbony': {
        'name': 'Vážené bonbony',
        'template': 'weighted-candy.html',
    },
    'bylinne-kapky': {
        'name': 'Bylinné kapky',
        'template': 'herbal-drops.html',
    },
    'bylinne-sirupy': {
        'name': 'Bylinné sirupy',
        'template': 'herbal-syrups.html',
    },
    'ovocne-sirupy': {
        'name': 'Ovocné sirupy',
        'template': 'fruit-syrups.html',
    },
    'med': {
        'name': 'Med',
        'template': 'honey.html',
    },
    'alkoholicke-napoje': {
        'name': 'Alkoholické nápoje',
        'template': 'alcoholic-beverages.html',
    },
    'kosmetika': {
        'name': 'Kosmetika',
        'template': 'cosmetics.html',
    },
    'oleje-a-octy': {
        'name': 'Oleje a octy',
        'template': 'oils.html',
    },
    'porcelain': {
        'name': 'Porcelán',
        'template': 'porcelain.html',
    },
    'accessories': {
        'name': 'Příslušenství',
        'template': 'accessories.html',
    },
}


@require_http_methods(['GET'])
def home(req):
    return render(req, 'catalog.html', {
        'catalog': mapping.items()
    })


@require_http_methods(['GET'])
def category(req, category_id):
    item = mapping[category_id]
    if item:
        return render(req, 'catalog/%s' % item['template'])
    raise Http404
