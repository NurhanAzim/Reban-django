from django.urls import path

from . import views

app_name = "crm"
urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    # egg
    path("egg/all/<int:pk>/", views.egg_view, name="egg_view"),
    path("egg/add/", views.egg_add, name="egg_add"),
    path("egg/<str:date>/", views.egg_detail, name="egg_detail"),
    path("egg/<str:date>/update/", views.egg_update, name="egg_update"),
    path("egg/<str:date>/all/delete/", views.egg_delete, name="egg_delete"),
    # chicken
    path("chicken/all/<int:pk>/", views.chicken_view, name="chicken_view"),
    path("chicken/add/", views.chicken_add, name="chicken_add"),
    path("chicken/<int:pk>/", views.chicken_detail, name="chicken_detail"),
    path("chicken/<int:pk>/update/", views.chicken_update, name="chicken_update"),
    path("chicken/<int:pk>/delete/", views.chicken_delete, name="chicken_delete"),
    # Egg Shipment
    path('egg/shipment/all/<int:pk>/', views.egg_shipment_view, name='egg_shipment_view'),
    path('egg/shipment/add/', views.egg_shipment_add, name='egg_shipment_add'),
    path('egg/shipment/<int:pk>/', views.egg_shipment_detail, name='egg_shipment_detail'),
    path('egg/shipment/<int:pk>/delete/', views.egg_shipment_delete, name='egg_shipment_delete'),
]