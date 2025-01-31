from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from recipes.views import RecipeViewSet

def home_view(request):
    return HttpResponse("Добро пожаловать на главную страницу!")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("s/<int:pk>", RecipeViewSet.as_view({"get": "retrieve"})),
    path("", home_view, name="home"),

]
