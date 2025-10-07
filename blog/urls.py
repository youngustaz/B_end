from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.post_list, name='post_list'),   
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.project_create, name='project_create'),  
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path("testimonials/", views.testimonials, name="testimonials"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
