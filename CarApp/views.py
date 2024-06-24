from django.shortcuts import render,redirect
from . import forms
from .forms import ChangeUserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Brand, Order
from .models import Order
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        form.save()  
        messages.success(self.request, 'Account Created Successfully')
        return super().form_valid(form)
   

class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    brands = Brand.objects.all()
    cars = Car.objects.all()
    selected_brand = request.GET.get('brand')
    if selected_brand:
        cars = cars.filter(brand__name=selected_brand)
    else:
        cars = Car.objects.all()
    return render(request, 'home.html', {'brands': brands, 'cars': cars, 'selected_brand': selected_brand})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = car
            comment.save()
            return redirect('car_detail', car_id=car.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'car': car,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'car_details.html', context)


@login_required
def buy_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        Order.objects.create(user=request.user, car=car)
        return redirect('profile')
    return redirect('car_detail', car_id=car_id)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'orders': orders})

@login_required
def profile_view(request):
    user = request.user
    data = Car.objects.filter(author=user)
    orders = Order.objects.filter(user=user)  
    
    context = {
        'data': data,
        'user': user,
        'orders': orders,
    }
    
    return render(request, 'profile.html', context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile Update Successfully')
        return super().form_valid(form)  
    
class PassChangeView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'pass_change.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Password Updated Successfully')
        return super().form_valid(form)
    

