from django.urls import path
# Импортируем созданное нами представление
from .views import AdList, AdDetail, AdCreate, AdUpdate, AdDelete, UserResponseCreate, UserResponseList, UserResponseAccept, UserResponseDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('ad/', AdList.as_view(), name='ad'),
   path('ad/<int:pk>', AdDetail.as_view(), name='ad_detail'),
   path('ad/create/', AdCreate.as_view(), name='ad_create'),
   path('ad/<int:pk>/edit/', AdUpdate.as_view(), name='ad_update'),
   path('ad/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
   path('/response/', UserResponseList.as_view(), name='response'),
   path('/<int:pk>/response/create/', UserResponseCreate.as_view(), name='response_create'),
   path('/response/<int:pk>/delete/', UserResponseDelete.as_view(), name='response_delete'),
   path('/response/<int:pk>/accept/', UserResponseAccept.as_view(), name='response_accept'),
]
