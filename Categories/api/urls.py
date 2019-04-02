from django.conf.urls import url, include
from .views import PopularBrandsView,TopCategoriesList,CategoryListView

urlpatterns = [
    url(r'popularbrands/',PopularBrandsView.as_view()),
    url(r'topcategories/$',TopCategoriesList.as_view()),
    url(r'getcategories/$',CategoryListView.as_view()),
]