from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'home.html'


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)