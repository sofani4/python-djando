from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [

    path('costs/', CostsList.as_view(), name='costs'),
    path('costs_add/', costs_add, name='costs_add'),
    path('costs_search_form/', costs_search_form, name='costs_search_form'),
    path('costs_search_results/', costs_search_results, name='costs_search_results'),

    path('income/', IncomeList.as_view(), name='income'),
    path('income_add/', income_add, name='income_add'),
    path('income_search_form/', income_search_form, name='income_search_form'),
    path('income_search_results/', income_search_results, name='income_search_results'),

    path('analysis/', analysis, name='analysis'),
    path('analysis_form/', analysis_form, name='analysis_form'),
    path('analysis_results/', analysis_results, name='analysis_results'),

    path('main_str/', main_str, name='main_str'),
    path('accounts/profile/', profile, name='profile'),
    path('register/', register, name='register'),

    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
    path('o_p/', o_p, name='o_p'),
    path('', index, name='index'),
]