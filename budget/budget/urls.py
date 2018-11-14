from django.conf.urls.defaults import *

"""
Needed Urls:
Dashboard
Year Summary
Month Summary
CRUD Budget
CRUD BudgetEstimates

Eventually:
Custom date range
Week Summary
Day Summary
...?
"""

urlpatterns = patterns('budget.views',
    url(r'^$', 'dashboard', name='budget_dashboard'),
    url(r'^setup/$', 'setup', name='budget_setup'),
    
    # Summaries
    url(r'^summary/$', 'summary_list', name='budget_summary_list'),
    url(r'^summary/(?P<year>\d{4})/$', 'summary_year', name='budget_summary_year'),
    url(r'^summary/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'summary_month', name='budget_summary_month'),
    
    # Categories
    url(r'^category/', include('budget.categories.urls')),
    
    # Budget
    url(r'^budget/$', 'budget_list', name='budget_budget_list'),
    url(r'^budget/add/$', 'budget_add', name='budget_budget_add'),
    url(r'^budget/edit/(?P<slug>[\w-]+)/$', 'budget_edit', name='budget_budget_edit'),
    url(r'^budget/delete/(?P<slug>[\w-]+)/$', 'budget_delete', name='budget_budget_delete'),
    
    # BudgetEstimates
    url(r'^budget/(?P<budget_slug>[\w-]+)/estimate/$', 'estimate_list', name='budget_estimate_list'),
    url(r'^budget/(?P<budget_slug>[\w-]+)/estimate/add/$', 'estimate_add', name='budget_estimate_add'),
    url(r'^budget/(?P<budget_slug>[\w-]+)/estimate/edit/(?P<estimate_id>\d+)/$', 'estimate_edit', name='budget_estimate_edit'),
    url(r'^budget/(?P<budget_slug>[\w-]+)/estimate/delete/(?P<estimate_id>\d+)/$', 'estimate_delete', name='budget_estimate_delete'),
    
    # Transaction
    url(r'^transaction/', include('budget.transactions.urls')),
)
