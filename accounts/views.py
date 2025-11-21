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
                messages.success(request, 'You are now logged in!')
                return redirect('dashboard')
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
        

@login_required(login_url='login')
def dashboard(request):
        return render(request,"accounts/dashboard.html")

def forgotpassword(request):
        if request.method=="POST":
            email = request.POST.get('email')
            if Accounts.objects.filter(email=email).exists():
                user=Accounts.objects.get(email__exact=email)

                #email verify for forgotpassword
                current_site=get_current_site(request)
                mail_subject="Reset the password!"
                message=render_to_string('accounts/email_verify_password.html',{
                    'user':user,
                    'domain':current_site,
                    'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),


                })
                to_email=email
                send_email=EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                return redirect('login')

            else:
                 messages.error(request,'Didnot find the error !')
                 return redirect('forgotpassword')
            
        return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
          uid=urlsafe_base64_decode(uidb64).decode()
          user=Accounts._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Accounts.DoesNotExist):
            user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Sucess full reset the password')
        return redirect('resetpassword')
    else:
         messages.error(request,"Error for some Problem plz try again")
         return redirect('login')


def resetpassword(request):
     if request.method=="POST":
          password=request.POST.get('password')
          confirm_pssword=request.POST.get('confirm_password')

          if password == confirm_pssword:
               uid = request.session.get('uid')
               user=Accounts.objects.get(pk=uid)
               user.set_password(password)
               user.save()
               messages.success(request,'sucessfull update the password')
               return redirect('login')
               


          else:
               messages.error(request,'password doesnot match')
               return redirect('resetpassword')

               
     return render(request,'accounts/resetpassword.html')