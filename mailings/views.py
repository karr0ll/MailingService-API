from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm
from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data()
    #     owner = self.request.user
    #     context_data['user'] =
    #     return context_data


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user = self.request.user
        context_data['user'] = user
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            new_mailing = form.save()
            new_mailing.customers.owner, new_mailing.user = user
            return super().form_valid(form)


# class Reporter(models.Model): => User
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#
# class Article(models.Model): => Mailing
#     headline = models.CharField(max_length=100)
#     pub_date = models.DateField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

# r = Reporter(first_name="John", last_name="Smith", email="john@example.com")

# a = Article(id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
# Create an Article via the Reporter object:
#
# new_article = r.article_set.create(
# ...     headline="John's second story", pub_date=date(2005, 7, 29)
# ... )



class MailingDetailView(DetailView):
    model = Mailing

    def get_title(self):
        return self.object.title


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('subject', 'body')
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse('mailings:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')