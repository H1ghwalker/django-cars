from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', CarsHome.as_view(), name='home'), # http://127.0.0.1:8000/cars/
    path('about/', about, name='about'),
    path('addpost/', AddPost.as_view(), name='add_post'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', CarsCategories.as_view(), name='category')
]