from django.urls import path
from .views import MainView
from .models import Menu

urlpatterns = [path("", MainView.as_view(), name="")]

for i in Menu.objects.all():
    urlpatterns += [path(i.url.replace("/", ""), MainView.as_view())]

