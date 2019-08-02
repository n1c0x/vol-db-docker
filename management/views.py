from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import *
from django.contrib.auth.decorators import login_required
from vol.models import *
import datetime
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    template_name = 'management/management_index.html'
    queryset = Vol.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        last_month = datetime.date.today() - datetime.timedelta(days=30)
        context['new_number_customer_pre_month'] = User.objects.filter(date_joined__gt=(last_month)).filter(is_staff=0).count()
        context['flights'] = Vol.objects.all().count()
        context['customer'] = User.objects.filter(is_staff=0).count()
        return context

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


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
        # context['customer_prev_month'] = User.objects.filter(last_login__lt=(last_month)).filter(is_staff=0)
        context['customer_prev_month'] = User.objects.filter(is_staff=0).filter(Q(last_login__lt=(last_month)) | Q(last_login__isnull=True))
        context['customer_prev_month_percentage'] = number_customer_prev_month_not_loggedin * 100 / total_customer
        context['customer_is_inactive'] = User.objects.filter(is_active=0).filter(is_staff=0)
        return context

    def get_queryset(self):
        return User.objects.filter(is_staff=0)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CustomerCreate(CreateView):
    """ Class to create a customer """
    model = Profile
    template_name = 'management/customer/add.html'
    form_class = ProfileForm
    second_form_class = SignupForm
    success_url = '/management/customer_management'

    def get_context_data(self, **kwargs):
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        context['user_form'] = self.second_form_class
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            customer = form.save(commit=False)
            customer.user_id = user.id
            customer.save()
        return super(CustomerCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CustomerUpdate(UpdateView):
    """ Class to update a customer """
    model = User
    template_name = 'management/customer/add.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    # form_class = ProfileForm
    # second_form_class = SignupForm
    success_url = '/management/customer_management'

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdate, self).get_context_data(**kwargs)
        # context['user_form'] = self.second_form_class
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            customer = form.save(commit=False)
            customer.user_id = user.id
            customer.save()
        return super(CustomerCreate, self).form_valid(form)

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
