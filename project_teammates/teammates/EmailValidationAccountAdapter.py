from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.utils.translation import ugettext as _
import json
from django.http import HttpResponse


class MyCoolAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        if email.split(".")[-1] != "edu":
            raise ValidationError(_("Registration using non-education email addresses is prohibited. Please supply your university email address."))
        return email

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field

        data = form.cleaned_data
        print('data: ',data)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        if data.get('skills'):
            setattr(user, "skills", data.get('skills'))
        if data.get('university'):
            setattr(user, "university", data.get('university'))
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        return user

    def ajax_response(self, request, response, redirect_to=None, form=None,
                      data=None):
        resp = {}
        status = response.status_code

        if redirect_to:
            status = 200
            resp['location'] = redirect_to
        if form:
            if request.method == 'POST':
                if form.is_valid():
                    status = 200
                else:
                    status = 400
            else:
                status = 200
            resp['form'] = self.ajax_response_form(form)
            if hasattr(response, 'render'):
                response.render()
            resp['html'] = response.content.decode('utf8')
        if data is not None:
            resp['data'] = data
        print('some', data)
        return HttpResponse(json.dumps(resp),
                            status=status,
                            content_type='application/json')
