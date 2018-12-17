from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='budget_dashboard'),

    path('budgets/', views.budgets, name='budget_budgets'),
    path('budgets/<int:id>/', views.budget_details, name='budget_budget_details'),
    path('budgets/add/', views.budget_create, name='budget_add_budget'),
    path('budgets/update/<int:id>/', views.budget_update, name='budget_update_budget'),
    path('budgets/delete/<int:id>/', views.budget_delete, name='budget_delete_budget'),

    path('categories/', views.categories, name='budget_categories'),
    path('categories/<int:id>/', views.category_details, name='budget_category_details'),
    path('categories/create/', views.category_create, name='budget_category_create'),
    path('categories/update/<int:id>/', views.category_update, name='budget_category_update'),
    path('categories/delete/<int:id>/', views.category_delete, name='budget_category_delete'),

    path('operations/create/', views.operation_create, name='budget_operation_create'),
    path('operations/update/<int:id>/', views.operation_update, name='budget_operation_update'),
    path('operations/delete/<int:id>/', views.operation_delete, name='budget_operation_delete'),

    path('archive/', views.archive, name='budget_archive'),
]
