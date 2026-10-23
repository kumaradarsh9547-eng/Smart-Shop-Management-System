from django.contrib import admin
from django.urls import path, include
from inventory.views import dashboard, seed_demo, index
from pathlib import Path
from django.http import FileResponse, Http404
urlpatterns = [path('admin/', admin.site.urls), path('api/dashboard/', dashboard), path('api/', include('inventory.urls')), path('api/demo-data/', seed_demo), path('', index)]
urlpatterns += [
    path("images/<str:filename>", lambda request, filename: (
        FileResponse(open(Path(__file__).resolve().parents[2] / "frontend" / "images" / filename, "rb"))
        if (Path(__file__).resolve().parents[2] / "frontend" / "images" / filename).is_file()
        else (_ for _ in ()).throw(Http404("Image not found"))
    )),
]
