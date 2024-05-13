from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from recipient.models import Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'name', 'description']
    success_url = reverse_lazy('recipient:list')


class RecipientListView(ListView):
    model = Recipient


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'name', 'description']
    success_url = reverse_lazy('recipient:list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipient:list')


class RecipientDetailView(DetailView):
    model = Recipient
