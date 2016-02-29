import random, string, logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages

from items.models import InterUser

from items.forms import (
      CreateUserForm,
      UserRegForm,
      OrganizationFormSelfRegistration,
      SetPasswordForm,
)

logger = logging.getLogger(__name__)

def register(request):
    """
    Register a new user with a new organization
    """
    if request.method == 'POST':
        user_reg_form = UserRegForm(request.POST, prefix = "a")
        org_form = OrganizationFormSelfRegistration(request.POST, prefix = "b")
        if user_reg_form.is_valid() and org_form.is_valid():
            new_org = org_form.save(commit=False)
            new_user = user_reg_form.save(commit=False)
            new_user.backend='django.contrib.auth.backends.ModelBackend'
            new_user.is_active = False
            new_user.save()
            new_org.user = new_user
            new_org.save()
            
            email_new_user(request, new_user)

            return HttpResponseRedirect(reverse('register_email_instructions'))
    else:
        user_reg_form = UserRegForm(prefix = "a")
        org_form = OrganizationFormSelfRegistration(prefix = "b")

    return render_to_response("registration/register.html",
        {'user_reg_form':user_reg_form, 'org_form': org_form},
        RequestContext(request))


def register_email_instructions(request):
    """
    After the user has registered, give the instructions for confirming
    """
    return render_to_response('registration/check_email.html', RequestContext(request))


def register_email_code_password(request, code):
    """
    Allow system created accounts to create a password.
    """
    # find user based on confirmation code
    try:
        user = InterUser.objects.get(confirmation_code=code)
    except InterUser.DoesNotExist:
        return render_to_response('registration/set_password.html', {'no_code': True}, RequestContext(request))

    # save password
    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            user.is_active = True
            user.is_confirmed = True
            user.save()
            messages.add_message(request, messages.INFO, 'Your account is activated.  Log in below.')
            return HttpResponseRedirect(reverse('auth_login'))
    else:
        form = SetPasswordForm(user=user)

    return render_to_response('registration/set_password.html', {'form': form}, RequestContext(request))


def email_new_user(request, user):
    """
    Send email to newly created accounts
    """
    if not user.confirmation_code:
        user.confirmation_code = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(30))
        user.save()
      
    host = request.get_host()

    content = '''To activate your account, please click the link below or copy it to your web browser.  You will need to create a new password.
http://%s%s
''' % (host, reverse('register_password', args=[user.confirmation_code]))

    logger.debug(content)

    send_mail(
        "A SignalBack account has been created for you",
        content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email], fail_silently=False
    )
