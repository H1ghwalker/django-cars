
from django.contrib import admin
from django.urls import path, include
from cars.views import pageNotFound
from django.conf.urls.static import static
from testsite import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('cars.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    
handler404 = pageNotFound
