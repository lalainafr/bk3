from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
# token - mail confirmation import
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .form import RegisterCustomerForm
from .token import generate_token

User = get_user_model()


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        # on decode le pk et on le compare si ca correspond à l'id du user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    # on decode le token et le compare par rapport au token generé
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Votre compte a été activé, pour pouvez vous authentifier actuelement..",
        )
        return redirect("login")
    return render(request, "account/activate_fail.html")


# register customer
def register_user(request):
    if request.method == "POST":
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.save()

            # email content
            email_subject = "Activer votre compte"
            message = render_to_string(
                "account/activate.html",
                {
                    "user ": user,
                    "domain": "127.0.0.1:8000",
                    # encoder le user.pk
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    # generer un token pour le user.pk
                    # en utilisant token.py avec 'six'
                    "token": generate_token.make_token(user),
                },
            )

            # send mail
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(email_subject, message, email_from, recipient_list)
            messages.success(
                request,
                "Un message vous est envoyé sur votre adress email afin de valider votre compte",
            )
            return redirect("login")
        else:
            # print("ERREURS DU FORMULAIRE :", form.errors)
            messages.warning(request, "Something went wrong")
            return redirect("register_user")
    else:
        form = RegisterCustomerForm()
        context = {"form": form}
        return render(request, "account/register_user.html", context)


# login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")
        else:
            messages.warning(request, "Invalid username or password")
            return redirect("login")
    else:
        return render(request, "account/login.html")


# logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")
