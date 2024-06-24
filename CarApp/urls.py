from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/',views.RegisterView.as_view(),name='signup'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('', views.home, name='home'),
   
    path('profile/', views.profile_view, name=''),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('buy/<int:car_id>/', views.buy_car, name='buy_car'),
    path('orders/', views.order_history, name='profile'),
    path('orders/edit_profile', views.EditProfileView.as_view(), name='edit'),
    path('orders/pass_change/', views.PassChangeView.as_view(), name='pass_change'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)