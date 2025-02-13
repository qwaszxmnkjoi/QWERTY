from django.utils import timezone
from django.views.generic import TemplateView

from customer.models import User, Category, Country


class ChatView(TemplateView):
    template_name = 'chat/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        user = User.objects.filter(chat_id=kwargs.get('chat_id')).first()
        country = Country.objects.get(slug=kwargs['country'])
        category = Category.objects.get(slug=kwargs['category'], country=country)
        # messages = category.message.all().order_by('dt_create')[:10]
        context.update({
            'title': f'{country.name} {category.name}',
            'not_found_text': None,
            'placeholder_text': None,
            'placeholder_caption': None,
            'user': user,
            'country': country,
            'category': category,
            'messages': []
        })
        return context


chat_view = ChatView.as_view()
