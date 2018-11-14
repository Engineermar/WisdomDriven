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

    url(r'^company/account/$', views.company_account, name = 'company-account'),
    url(r'^company/cargo/$', views.company_cargo, name = 'company-cargo'),
    url(r'^company/cargo/add/$', views.company_add_cargo, name = 'company-add-cargo'),
    url(r'^company/cargo/edit/(?P<cargo_id>\d+)/$', views.company_edit_cargo, name = 'company-edit-cargo'),
    url(r'^company/order/$', views.company_order, name = 'company-order'),
    url(r'^company/customer/(?P<company_id>\d+)/$', views.company_customer, name = 'company-customer'),
    url(r'^company/report/$', views.company_report, name = 'company-report'),

    # Sign In/ Sign Up/ Sign Out
   # url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/company/order/notification/(?P<last_request_time>.+)/$', apis.company_order_notification),


    # APIs for CUSTOMERS
    url(r'^api/customer/companys/$', apis.customer_get_companys),
    url(r'^api/customer/cargos/(?P<company_id>\d+)/$', apis.customer_get_cargos),
    url(r'^api/customer/order/add/$', apis.customer_add_order),
    url(r'^api/customer/order/latest/$', apis.customer_get_latest_order),
    url(r'^api/customer/driver/location/$', apis.customer_driver_location),


    #APIs for Drivers
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', apis.driver_pick_orders),
    url(r'^api/driver/order/latest/$', apis.driver_get_latest_orders),
    url(r'^api/driver/order/complete/$', apis.driver_complete_orders),
    url(r'^api/driver/order/revenue/$', apis.driver_get_revenue),
    url(r'^api/driver/location/update/$', apis.driver_update_location),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
