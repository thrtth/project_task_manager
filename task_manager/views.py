from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    text = _('Hello!')
    return render(request, 'index.html', {'text': text})
