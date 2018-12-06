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
    url(r'^main/sign-in/$', auth_views.login,
        {'template_name': 'main/sign_in.html'},
        name = 'main-sign-in'),
    url(r'^main/sign-out', auth_views.logout,
        {'next_page': '/'},
       name = 'main-sign-out'),
    url(r'^main/about', views.main_about,
       name = 'main-about'),
    url(r'^main/home_back', views.main_home_back,
       name = 'main-home'),
    url(r'^main/company/sign-up', views.company_sign_up,
        name = 'company-sign-up'),
    url(r'^main/$', views.main_home, name = 'main-home'),
    url(r'^main/company/employee/$', views.company_employee, name = 'company-employee'),
    url(r'^main/business/sign-up', views.business_sign_up,
        name = 'business-sign-up'),
    url(r'^main/business/$', views.business_home, name = 'business-home'),
    url(r'^main/driver/sign-up', views.driver_sign_up,
        name = 'driver-sign-up'),
    url(r'^main/driver/$', views.driver_home, name = 'driver-home'),

    # company
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.company_profile),
    url(r'^main/company/company_profile/$', views.company_profile, name = 'company-profile'),


    url(r'^main/company/order/$', views.company_current_orders, name = 'company-order'),

    url(r'^main/company/stats/$', views.company_stats, name = 'company-stats'),


    # business
    url(r'^main/business/order/edit/$', views.business_edit_order, name = 'business-order-edit'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.driver_profile),
    url(r'^main/business/business_profile/$', views.business_profile, name = 'business-profile'),
    url(r'^main/business/order/$', views.business_order, name = 'business-order'),
    url(r'^main/business/stats/$', views.business_stats, name = 'business-stats'),

    #driver
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.driver_profile),
    url(r'^main/driver/driver_profile/$', views.driver_profile, name = 'driver-profile'),
    #url(r'^main/driver/profile/$', views.driver_profile, name = 'driver-profile'),
    url(r'^main/driver/trip/$', views.driver_trip, name = 'driver-trip'),
    url(r'^main/driver/trip/stop/$', views.driver_stop, name = 'driver-trip-stop'),
    url(r'^main/driver/trip/expense/$', views.driver_expense, name = 'driver-trip-expense'),


    url(r'^main/driver/stats/$', views.driver_stats, name = 'driver-stats'),


    url(r'^api/main/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),





    # APIs for company
    url(r'^api/main/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),
    url(r'^api/main/company/business$', apis.company_get_business),

    #url(r'^api/main/company/order/add/$', apis.company_add_order),
    #url(r'^api/main/company/order/latest/$', apis.company_get_latest_order),
    url(r'^api/main/company/driver/location/$', apis.company_driver_location),
    url(r'^api/comapny/order/revenue/$', apis.company_get_revenue),
     # driver



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
    url(r'^api/main/business/order/notification/(?P<last_request_time>.+)/$', apis.business_order_notification),
    url(r'^api/business/main/company/$', apis.business_get_company),
    url(r'^api/business/order/$', apis.business_get_orders),
    #url(r'^api/business/order/add/$', apis.business_add_order),
    #url(r'^api/business/order/latest/$', apis.business_get_latest_order),
    url(r'^api/business/driver/location/$', apis.business_driver_location),
    url(r'^api/business/order/expenditure/$', apis.business_get_expenditure),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
