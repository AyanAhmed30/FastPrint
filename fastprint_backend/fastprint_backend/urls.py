from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    
    path('api/pricing/', include('pricing.urls')),
    path('api/calculator/', include('printbookcalculator.urls')),
    path('api/comicbook/', include('comicbook.urls')),


    path('api/photobook/', include('photobook.urls')),
    path('api/magazine/', include('magazine.urls')),
    path('api/yearbook/', include('yearbook.urls')),
    path('api/calender/', include('calender.urls')),  # ✅ Add this line
    path('api/', include('shipping.urls')),  # ✅ Add this line
        path('api/books/', include('book.urls')),





]
