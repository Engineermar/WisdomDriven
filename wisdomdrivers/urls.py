from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from wdapp import views, apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^api-token-auth/', views.obtain_auth_token),
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
    #business
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.b_home, name='home'),
    url(r'^api-token-auth/', views.business_obtain_auth_token),
    url(r'^business/sign-in/$', auth_views.login,
        {'template_name': 'business/sign_in.html'},
        name = 'business-sign-in'),
    url(r'^business/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'business-sign-out'),
    url(r'^business/sign-up', views.business_sign_up,
        name = 'business-sign-up'),
    url(r'^business/$', views.business_home, name = 'business-home'),
    #driver
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.d_home, name='home'),
    url(r'^api-token-auth/', views.driver_obtain_auth_token),
    url(r'^driver/sign-in/$', auth_views.login,
        {'template_name': 'driver/sign_in.html'},
        name = 'driver-sign-in'),
    url(r'^driver/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'driver-sign-out'),
    url(r'^driver/sign-up', views.driver_sign_up,
        name = 'driver-sign-up'),
    url(r'^driver/$', views.driver_home, name = 'driver-home'),
    # company
    url(r'^company/account/$', views.company_account, name = 'company-account'),
    url(r'^company/account/$', views.company_account, name = 'company-account'),
    url(r'^company/cargo/$', views.company_cargo, name = 'company-cargo'),
    url(r'^company/cargo/add/$', views.company_add_cargo, name = 'company-add-cargo'),
    url(r'^company/cargo/edit/$', views.company_edit_cargo, name = 'company-edit-cargo'),
    url(r'^company/order/$', views.business_order, name = 'company-order'),
    url(r'^company/order/cargomanifest/$', views.company_current_orders, name = 'company-current-order'),
    url(r'^company/order/edit/$', views.company_edit_order, name = 'company-edit-cargo'),
    #url(r'^company/company/$', views.company_company, name = 'company-company'),
    url(r'^company/report/$', views.company_report, name = 'company-report'),
     # business
    url(r'^business/account/$', views.business_account, name = 'business-account'),
    url(r'^business/account/$', views.business_account, name = 'business-account'),
    url(r'^business/order/$', views.business_order, name = 'business-order'),
    url(r'^business/order/cargomanifest/$', views.business_current_orders, name = 'business-current-order'),
    url(r'^business/order/edit/$', views.business_edit_order, name = 'business-edit-cargo'),
    #url(r'^business/order/$', views.business_order, name = 'business-order'),
    #url(r'^company/company/$', views.company_company, name = 'company-company'),
    url(r'^business/report/$', views.business_report, name = 'business-report'),
    #driver
    url(r'^driver/account/$', views.driver_account, name = 'driver-account'),
    url(r'^driver/account/$', views.driver_account, name = 'driver-account'),
    url(r'^driver/trip/$', views.driver_trip, name = 'driver-trip'),
    url(r'^driver/trip/stop/$', views.driver_stop, name = 'driver-trip-stop'),
    url(r'^driver/trip/expense/$', views.driver_expense, name = 'driver-trip-expense'),
   # url(r'^driver/trip/$', views.driver_order, name = 'driver-order'),
    url(r'^driver/trip/cargomanifest/$', views.driver_current_orders, name = 'driver-current-order'),
    #url(r'^driver/trip/edit/$', views.driver_edit_order, name = 'driver-edit-cargo'),
    #url(r'^company/company/$', views.company_company, name = 'company-company'),
    url(r'^driver/report/$', views.driver_report, name = 'driver-report'),
    
    # Sign In/ Sign Up/ Sign Out
   # url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),
    # Sign In/ Sign Up/ Sign Out
   # url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/driver/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),
    # Sign In/ Sign Up/ Sign Out
   # url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/business/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),

    # APIs for companyS
    url(r'^api/company/companys/$', apis.company_get_companys),
    url(r'^api/company/cargos/$', apis.company_get_cargos),
    url(r'^api/company/order/add/$', apis.company_add_order),
    url(r'^api/company/order/latest/$', apis.company_get_latest_order),
    url(r'^api/company/driver/location/$', apis.company_driver_location),
    url(r'^api/comapny/order/revenue/$', apis.company_get_revenue),
     # driver
    url(r'^driver/sign-in/$', auth_views.login,
        {'template_name': 'driver/sign_in.html'},
        name = 'driver-sign-in'),
    url(r'^driver/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'driver-sign-out'),
    url(r'^driver/sign-up', views.driver_sign_up,
        name = 'driver-sign-up'),
    url(r'^driver/$', views.driver_home, name = 'driver-home'),

    url(r'^driver/account/$', views.driver_account, name = 'driver-account'),
    #url(r'^driver/cargo/$', views.driver_cargo, name = 'driver-cargo'),
   # url(r'^driver/cargo/add/$', views.driver_add_cargo, name = 'driver-add-cargo'),
   # url(r'^driver/cargo/edit/$', views.driver_edit_cargo, name = 'driver-edit-cargo'),
    url(r'^driver/order/$', views.business_order, name = 'driver-order'),
    #url(r'^driver/company/$', views.business_company, name = 'driver-company'),
    url(r'^driver/report/$', views.business_report, name = 'driver-report'),
    #APIs for Drivers
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', apis.driver_pick_orders),
    url(r'^api/driver/order/latest/$', apis.driver_get_latest_orders),
    url(r'^api/driver/order/complete/$', apis.driver_complete_orders),
    url(r'^api/driver/location/update/$', apis.driver_update_location),
    # APIs for businessS
    url(r'^api/business/companys/$', apis.business_get_companys),
    url(r'^api/business/order/$', apis.business_get_orders),
    url(r'^api/business/order/add/$', apis.business_add_order),
    url(r'^api/business/order/latest/$', apis.business_get_latest_order),
    url(r'^api/business/driver/location/$', apis.business_driver_location),
    url(r'^api/business/order/expenditure/$', apis.business_get_expenditure),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
