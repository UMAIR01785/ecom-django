from django.shortcuts import render,redirect,HttpResponse
from . forms import RegisterForm
from . models import Accounts
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
# verify Email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split('@')[0]

            user=Accounts.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number=phone_number
            user.save()

            # verify the emial
            current_site=get_current_site(request)
            mail_subject="Pleae active the account!"
            message=render_to_string('accounts/verfiyemail.html',{
                'user':user,
                'domain':current_site,
                'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),


            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            # messages.success(request,'Rigester is sucessful!')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegisterForm()
    context={
            'form': form
        }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)

        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
     auth.logout(request)
     messages.success(request,'You have been sucessfully logout')
     return redirect('login')
def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Accounts.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Your account is active !')
        return redirect('login')
    else:
        messages.error(request,'Invalid Account')
        return redirect('register')
    
    