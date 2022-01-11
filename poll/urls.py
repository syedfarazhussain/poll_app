from django.urls import path
from poll import views as poll_views
from . import views

urlpatterns = [
    path('', poll_views.home, name='home'),
    path('create/', poll_views.create, name='create'),
    path('delete/<poll_id>', views.delete, name='delete'),
    path('update_view/<poll_id>', views.update_view, name='update_view'),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('results/<poll_id>/', poll_views.results, name='results'),

]