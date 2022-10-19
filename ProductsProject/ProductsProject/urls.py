from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

# Setting the view for swagger
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Post API",
        default_version='1.0.0',
        description="API documentation for the App",
    ),
    public=True,
)

# Setting main paths for the project and connecting one to the app urls 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ProductsAPI.urls')),
    path('auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]
