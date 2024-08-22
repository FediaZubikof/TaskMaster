from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutProjectView(TemplateView):
    template_name = 'about/project.html'
