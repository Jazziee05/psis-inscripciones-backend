from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.conf import settings
from .models import Student, Course, Enrollment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "email", "id_number"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "title", "capacity"]

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrolled_at"]
        read_only_fields = ["enrolled_at"]
class PublicRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name  = serializers.CharField(required=False, allow_blank=True)
    invite_code = serializers.CharField(write_only=True)

    def validate_username(self, v):
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError("Username ya existe.")
        return v

    def validate_invite_code(self, v):
        if not settings.REGISTRATION_CODE or v != settings.REGISTRATION_CODE:
            raise serializers.ValidationError("Código de invitación inválido.")
        return v

    def create(self, data):
        data.pop("invite_code", None)
        # Opción A: crear usuario *staff* (secretaría) si pasa el código
        user = User.objects.create_user(**data, is_staff=True, is_superuser=False)
        grp, _ = Group.objects.get_or_create(name="secretaria")
        user.groups.add(grp)
        return user