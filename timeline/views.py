from django.views import generic

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'timeline/index.html'

index = IndexView.as_view()
