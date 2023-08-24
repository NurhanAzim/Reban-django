from django.urls import path

from . import views

app_name = "crm"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    # egg
    path("egg/all/<int:pk>/", views.EggView.as_view(), name="egg_view"),
    path("egg/add/", views.EggAdd.as_view(), name="egg_add"),
    path("egg/<str:date>/", views.EggDetail.as_view(), name="egg_detail"),
    path("egg/<str:date>/update/", views.EggUpdate.as_view(), name="egg_update"),
    path("egg/<str:date>/all/delete/", views.EggDelete.as_view(), name="egg_delete"),
    # chicken
    path("chicken/all/<int:pk>/", views.ChickenView.as_view(), name="chicken_view"),
    path("chicken/add/", views.ChickenAdd.as_view(), name="chicken_add"),
    path("chicken/<int:pk>/", views.ChickenDetail.as_view(), name="chicken_detail"),
    path("chicken/<int:pk>/update/", views.ChickenUpdate.as_view(), name="chicken_update"),
    path("chicken/<int:pk>/delete/", views.ChickenDelete.as_view(), name="chicken_delete"),
    # Egg Shipment
    path('egg/shipment/all/<int:pk>/', views.EggShipmentView.as_view(), name='egg_shipment_view'),
    path('egg/shipment/add/', views.EggShipmentAdd.as_view(), name='egg_shipment_add'),
    path('egg/shipment/<int:pk>/', views.EggShipmentDetail.as_view(), name='egg_shipment_detail'),
    path('egg/shipment/<int:pk>/delete/', views.EggShipmentDelete.as_view(), name='egg_shipment_delete'),
]