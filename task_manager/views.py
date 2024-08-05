from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        text = _('Hello!')
        return render(request, 'index.html', {'text': text})
