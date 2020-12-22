from django.views.decorators.http import require_http_methods
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
    'kava': {
        'name': 'Káva',
        'template': 'coffee.html',
    }
}

@require_http_methods(['GET'])
def catalog(req):
    return render(req, 'catalog.html', {
        'catalog': mapping.items()
    })

@require_http_methods(['GET'])
def catalog_category(req, category):
    item = mapping[category]
    if item:
        return render(req, 'catalog/%s' % item.template)
    raise NotFound
