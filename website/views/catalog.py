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
    'zobani': {
        'name': 'Zobání',
        'template': 'nibbles.html',
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
