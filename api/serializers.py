from rest_framework import serializers
from django.contrib.auth import get_user_model
from pets.models import Pet, Vaccination
from community.models import Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        read_only_fields = ['id']


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ['id', 'vaccine_name', 'date_given', 'next_due_date', 'notes']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class PetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    vaccinations = VaccinationSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'date_of_birth', 'age', 'photo', 'description', 'owner', 'vaccinations',
                  'comments', 'created_at']
        read_only_fields = ['id', 'created_at']