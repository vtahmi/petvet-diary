from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from pets.models import Pet
from .models import Comment
from .forms import CommentForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'community/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.pet = get_object_or_404(Pet, pk=self.kwargs['pet_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pet = self.pet
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pets:pet_detail', kwargs={'pk': self.pet.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.pet
        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'community/comment_confirm_delete.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('pets:pet_detail', kwargs={'pk': self.object.pet.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully.')
        return super().delete(request, *args, **kwargs)
