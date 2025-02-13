import typing

from django import template

from customer.models import User

register = template.Library()


@register.simple_tag(name='customer_get')
def customer_get(chat_id: typing.Optional[str] = None) -> typing.Optional[User]:
    user = None
    if chat_id:
        user, _ = User.objects.get_or_create(chat_id=chat_id)
    return user

