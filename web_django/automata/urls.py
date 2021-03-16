from django.urls import path

from . import views

urlpatterns = [
    path('input/', views.input, name='input'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('result/', views.computed_result, name="result"),
    path('savedAutomats/', views.saved_automatas, name="saved_automats"),
    path('playground/<int:automat_id>/', views.playground, name="playground"),
    path('playground/<int:automat_id>/result/', views.result, name="rasult"),
]
