from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_zip(value):
    if not value.isdigit():
        raise ValidationError(
            _("%(value)s is not a valid zip code"),
            params={"value": value},
        )
    list_value = value.split(" ")
    str_value = "".join(list_value)
    return str_value


def validate_city(value):
    if len(value) < 2:
        raise ValidationError(
            _("%(value)s is not a valid city name"),
            params={"value": value},
        )


def validate_address(value):
    if len(value) <= 1 or value.isnumeric():
        raise ValidationError(
            _("%(value)s is not a valid address"),
            params={"value": value},
        )


def validate_phone(value):
    for i in str(value[1:]):
        if i.isspace():
            pass

        elif not i.strip(" ").isdigit():
            raise ValidationError(
                _(f"{value} is not a valid phone number"),
                params={"value": i},
            )
    if not value.strip(" ")[0] in "+":
        raise ValidationError(
            _(f"{value} is not a phone number, Please enter a no like +91 67xxxxxxxx"
              ),
            params={"value": value},
        )


class User(AbstractUser):
    gender = models.CharField(
        max_length=11,
        choices=(("M", "Male"), ("F", "Female"), ("O", "Others")),
        null=True,
        db_index=True
    )
    phone = models.CharField(
        _("phone"),
        max_length=15,
        validators=[MinLengthValidator(10)],
        help_text=_("It should be +91 67xxx"),
        db_index=True
    )
    address1 = models.TextField(_("address 1"), validators=[validate_address], null=True, db_index=True)
    address2 = models.TextField(_("address 2"),
                                validators=[validate_address],
                                blank=True,
                                null=True,
                                db_index=True)
    city = models.CharField(_("city"),
                            max_length=500,
                            validators=[validate_city],
                            db_index=True)
    state = models.CharField(_("state"), max_length=250, null=True, db_index=True)
    country = models.CharField(_("country"), max_length=250, null=True, db_index=True)
    zip_code = models.CharField(_("zip code"),
                                max_length=6,
                                validators=[validate_zip], null=True, db_index=True)
    university_name = models.CharField(_("University or College Name"),max_length=250, db_index=True)
    registration_no = models.PositiveBigIntegerField(_("Registration No"), db_index=True, null=True)

    class Meta:
        unique_together = ("email",)