from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pets.models import Pet, Vaccination
#from appointments.models import Appointment


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        owners_group, created = Group.objects.get_or_create(name='Pet Owners')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Pet Owners" group'))

        vets_group, created = Group.objects.get_or_create(name='Veterinarians')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Veterinarians" group'))

        pet_ct = ContentType.objects.get_for_model(Pet)

        owner_permissions = Permission.objects.filter(
            content_type=pet_ct,
            codename__in=['add_pet', 'change_pet', 'delete_pet', 'view_pet']
        )
        owners_group.permissions.set(owner_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Pet Owners'))

        vet_permissions = Permission.objects.filter(
            content_type=pet_ct,
            codename='view_pet'
        )
        vets_group.permissions.set(vet_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Veterinarians'))

        self.stdout.write(self.style.SUCCESS('✅ Groups setup completed!'))