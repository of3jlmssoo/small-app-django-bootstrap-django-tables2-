from django.shortcuts import render
# import requests
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from accounts.forms import RegistrationFrom

from .forms import RegistrationFrom
from .models import Account

# Create your views here.

from django.http import HttpResponse


def register(request):
    return HttpResponse('register')


def login(request):
    return HttpResponse('login')


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        print(f'==> register.py register() {request.method=} {form.is_valid()=}')
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            is_approver = form.cleaned_data['is_approver']

            username = email.split("@")[0]

            print(f'==> register.py register() create_user will be called')
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.is_approver = is_approver

            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Registration successful')
            # return redirect('register')
            # messages.success(request, 'thank you sent you a verification mail')
            return redirect('/accounts/login/?command=verification&email=' + email)
        # else:
        #     return HttpResponse(form.errors.values())
    else:
        print(f'==> register.py register() {request.method=}')
        form = RegistrationFrom()

    # form = RegistrationFrom()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'your are now logged in')
            url = request.META.get('HTTP_REFERER')
            print(f'{url=}')
            try:
                query = requests.utils.urlparse(url).query
                print('query ->>>', query)  # query = next=/cart/checkout/
                params = dict(x.split("=") for x in query.split('&'))
                print(f'===> {params=}')
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except BaseException:
                pass
                return redirect('/tabletest/')
        else:
            print("==========else==============")
            messages.error(request, 'invalid  login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    print(f'==> logout')
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # check token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'configurations your accout is activated')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, '/tabletest/')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'please reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'password reset mail has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request, 'the account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'this link has been expired...')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'passwords donot match...')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
