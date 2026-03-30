from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PetForm, VaccinationForm
from .models import Pet, Vaccination


class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pets:pet_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Pet {form.instance.name} added successfully!')
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pets:pet_list')

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f'Pet {form.instance.name} updated successfully!')
        return super().form_valid(form)


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_confirm_delete.html'
    success_url = reverse_lazy('pets:pet_list')

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        pet_name = self.get_object().name
        messages.success(request, f'Pet {pet_name} deleted successfully.')
        return super().delete(request, *args, **kwargs)


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)


class VaccinationCreateView(LoginRequiredMixin, CreateView):
    model = Vaccination
    form_class = VaccinationForm
    template_name = 'pets/vaccination_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.pet = Pet.objects.get(pk=self.kwargs['pet_pk'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.pet = self.pet
        messages.success(self.request, f'Vaccination {form.instance.vaccine_name} added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pets:pet_detail', kwargs={'pk': self.pet.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.pet
        return context