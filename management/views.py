from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from vol.models import *
import datetime


def management_index(request):
    """
    Render the home page.

    **Template:**

    :template:`management/management_index.html`

    """
    return render(request, 'management/management_index.html')


def website_performance(request):
    """
    Render the home page.

    **Template:**

    :template:`management/website_performance.html`

    """
    return render(request, 'management/website_performance.html')


@method_decorator(login_required, name='dispatch')
class CustomerList(ListView):
    """
        Class which lists all the customer
    """
    model = Profile
    template_name = 'management/customer_management.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        last_month = datetime.date.today() - datetime.timedelta(days=30)
        number_customer_prev_month_not_loggedin = User.objects.filter(last_login__lt=(last_month)).filter(is_staff=0).count()
        total_customer = User.objects.filter(is_staff=0).count()
        context['customer_prev_month'] = User.objects.filter(last_login__lt=(last_month)).filter(is_staff=0)
        context['customer_prev_month_percentage'] = number_customer_prev_month_not_loggedin * 100 / total_customer
        context['customer_is_inactive'] = User.objects.filter(is_active=0).filter(is_staff=0)
        return context

    def get_queryset(self):
        return User.objects.filter(is_staff=0)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    """
        Class which lists all the customer
    """
    model = Profile
    template_name = 'management/user_management.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=1)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)
