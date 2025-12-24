from django.shortcuts import render, redirect
from . forms import RegisterForm
from . models import Account
# Create your views here.
def register(request):
    if request.method == "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']

            user=Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                phone_number=phone_number
            )
            user.save()
            return redirect('register')
    else:
     form=RegisterForm()

    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)