from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from wdapp import views, apis
from importlib import import_module
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^api-token-auth/', views.obtain_auth_token),
#views
    # company
    url(r'^company/sign-in/$', auth_views.login,
        {'template_name': 'company/sign_in.html'},
        name = 'company-sign-in'),
    url(r'^company/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'company-sign-out'),
    url(r'^company/sign-up', views.company_sign_up,
        name = 'company-sign-up'),
    url(r'^company/$', views.company_home, name = 'company-home'),
    url(r'^company/employee/$', views.company_employee, name = 'company-employee'),
    #url(r'^$', views.company_login,
     #   {'template_name': 'company/sign_in.html'},
      #  name = 'company-sign-in'),
    #url(r'^company/sign-out', views.company_logout,
     #   {'next_page': '/'},
      #  name = 'company-sign-out'),
    #url(r'^company/sign-up', views.company_sign_up,
     #   name = 'company-sign-up'),
    #url(r'^company/$', views.company_home, name = 'company-home'),
    #business

    #url(r'^admin/', admin.site.urls),
    #url(r'^$', views.home, name='home'),
    #url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^business/sign-in/$', views.business_login,
        {'template_name': 'business/sign_in.html'},
        name = 'business-sign-in'),
    url(r'^business/sign-out', views.business_logout,
        {'next_page': '/'},
        name = 'business-sign-out'),
    url(r'^business/sign-up', views.business_sign_up,
        name = 'business-sign-up'),
    #url(r'^business/$', views.business_home, name = 'business-home'),

    #driver
    #url(r'^admin/', admin.site.urls),
    #url(r'^$', views.home, name='home'),
    #url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^driver/sign-in/$', views.driver_login,
        {'template_name': 'driver/sign_in.html'},
        name = 'driver-sign-in'),
    url(r'^driver/sign-out', views.driver_logout,
        {'next_page': '/'},
        name = 'driver-sign-out'),
    url(r'^driver/sign-up', views.driver_sign_up,
        name = 'driver-sign-up'),
    #url(r'^driver/$', views.driver_home, name = 'driver-home'),

    # company
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.company_profile),
    url(r'^company/company_profile/$', views.company_profile, name = 'company-profile'),


    url(r'^company/order/$', views.company_current_orders, name = 'company-order'),

    url(r'^company/stats/$', views.company_stats, name = 'company-stats'),


    # business
    url(r'^business/order/edit/$', views.business_edit_order, name = 'business-order-edit'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.driver_profile),
    url(r'^business/profile/$', views.business_profile, name = 'business-profile'),
    url(r'^business/order/$', views.business_order, name = 'business-order'),
    url(r'^business/stats/$', views.business_stats, name = 'business-stats'),

    #driver
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.driver_profile),
    url(r'^driver/profile/$', views.driver_profile, name = 'driver-profile'),
    url(r'^driver/profile/$', views.driver_profile, name = 'driver-profile'),
    url(r'^driver/trip/$', views.driver_trip, name = 'driver-trip'),
    url(r'^driver/trip/stop/$', views.driver_stop, name = 'driver-trip-stop'),
    url(r'^driver/trip/expense/$', views.driver_expense, name = 'driver-trip-expense'),


    url(r'^driver/stats/$', views.driver_stats, name = 'driver-stats'),


    url(r'^api/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),





    # APIs for company
    url(r'^api/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),
    url(r'^api/company/business$', apis.company_get_business),

    #url(r'^api/company/order/add/$', apis.company_add_order),
    #url(r'^api/company/order/latest/$', apis.company_get_latest_order),
    url(r'^api/company/driver/location/$', apis.company_driver_location),
    url(r'^api/comapny/order/revenue/$', apis.company_get_revenue),
     # driver

    url(r'^driver/$', views.company_home, name = 'driver-home'),

    url(r'^driver/profile/$', views.driver_profile, name = 'driver-profile'),

    url(r'^driver/order/$', views.business_order, name = 'driver-order'),

    url(r'^driver/profile/$', views.business_profile, name = 'driver-profile'),
    #APIs for Drivers
    url(r'^api/driver/trip/notification/(?P<last_request_time>.+)/$', apis.driver_trip_notification),
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', apis.driver_pick_orders),
    url(r'^api/driver/order/latest/$', apis.driver_get_latest_orders),
    url(r'^api/driver/order/complete/$', apis.driver_complete_orders),
    #url(r'^api/driver/location/update/$', apis.driver_update_location),
    # APIs for business
    url(r'^api/business/order/notification/(?P<last_request_time>.+)/$', apis.business_order_notification),
    url(r'^api/business/company/$', apis.business_get_company),
    url(r'^api/business/order/$', apis.business_get_orders),
    #url(r'^api/business/order/add/$', apis.business_add_order),
    #url(r'^api/business/order/latest/$', apis.business_get_latest_order),
    url(r'^api/business/driver/location/$', apis.business_driver_location),
    url(r'^api/business/order/expenditure/$', apis.business_get_expenditure),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
