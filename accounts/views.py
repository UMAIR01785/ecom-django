from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegisterForm
from . models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
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
            ### verfiy the email to active the user 
            current_site=get_current_site(request)
            mail_subject="Active the account !"
            message=render_to_string('accounts/verfiy_email.html',{
               'user':user,
               'domain':current_site,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Register is successfully check your email for verfiy')
            return redirect('login')
    else:
     form=RegisterForm()

    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)


def activate(request,uidb64,token):
    try:
      uid=urlsafe_base64_decode(uidb64).decode()
      user=Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,Account.DoesNotExist):
      user = None
    

    if user is not None and default_token_generator.check_token(user,token):
       user.is_active=True
       user.save()
       return redirect('login')
    else:
        # ALWAYS return something
        return redirect('register')

      






def login(request):
   if request.method == "POST":
      email=request.POST.get('email')
      password=request.POST.get('password')
      user= auth.authenticate(request,email=email,password=password)
      if user:
         messages.success(request,'Sucessfull login')
         auth.login(request,user)
         return redirect('home')
      else:
         messages.error(request,'Invaild information')
         return redirect('login')
   return render(request,'accounts/login.html')
   



def logout(request):
   auth.logout(request)
   return redirect('login')


def forgotpassword(request):
   if request.method == 'POST':
      email=request.POST.get('email')
      if Account.objects.filter(email=email).exists():
         user=Account.objects.get(email=email)
         ### 
         current_site=get_current_site(request)
         mail_subject="Forgot the password"
         message=render_to_string('accounts/resetpassword_validate.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
         })
         to_email=email
         send_email=EmailMessage(mail_subject,message,to=[to_email])
         send_email.send()
         messages.success(request,'Check your email to reset the password')
         return redirect('login')
      else:
         messages.error(request,'Account does not exist')
         return redirect('forgotpassword')
   return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
   try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Account._default_manager.get(pk=uid)
   except(ValueError,Account.DoesNotExist):
      user =None
   
   if user and default_token_generator.check_token(user,token):
      request.session['uid']=uid
      messages.success(request,'successfull now you can reset the password !')
      return redirect('resetpassword')
   else:
      messages.error(request,'invalid information !')
      return redirect('forgotpassword')

      
def resetpassword(request):
   if request.method == "POST":
      password=request.POST.get('password')
      confirm_password=request.POST.get('confirm_password')

      if password == confirm_password:
         uid=request.session['uid']
         user=Account.objects.get(pk=uid)
         user.set_password(password)
         user.save()
         messages.success(request,'sucessful reset the password')
         return redirect('login')
      else:
         messages.error(request,'Invlaid password')
         return redirect('forgotpassword')
   return render(request,'accounts/resetpassword.html')
   

   