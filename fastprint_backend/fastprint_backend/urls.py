from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    # ✅ Correctly include your app routes
    path('api/pricing/', include('pricing.urls')),
    path('api/calculator/', include('printbookcalculator.urls')),
    path('api/comicbook/', include('comicbook.urls')),

    path('api/books/', include('books.urls')),

]
