from django.conf.urls import url, include
from .views import ProductDetailsView,SearchSuggestionsView,ProductsForCategoryView,CreateReviewView

urlpatterns = [
    url(r'details/$',ProductDetailsView.as_view()),
    url(r'suggestions/$',SearchSuggestionsView.as_view()),
    url(r'getproducts/$',ProductsForCategoryView.as_view()),
    url(r'review/create/$',CreateReviewView.as_view())
]