from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', include('ml_app.urls')),
    path('scrapping/', include('scrapping_app.urls')), # hay que revisarlo cuando los scripts este hechos
    path('', views.index, name='index'),
    path('houses/',include('house_app.urls'))
    
]+static(settings.STATIC_URL,
document_root=settings.STATICFILES_DIRS)+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)

