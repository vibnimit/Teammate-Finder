from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.utils.translation import ugettext as _

class MyCoolAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        # *** here goes your code ***
        if email.split(".")[-1] != "edu":
            raise ValidationError(_("Registration using non-education email addresses is prohibited. Please supply your university email address."))
        return email