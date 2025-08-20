# userprofile/admin.py
from django.contrib import admin, messages
from django.utils.crypto import get_random_string
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.shortcuts import redirect


def create_dummy_user(modeladmin, request, queryset):
    "Create 10 dummy users with random emails."
    for _ in range(10):
        email = f"dummy_{get_random_string(8)}@gmail.com"
        while CustomUser.objects.filter(email=email).exists():
            email = f"dummy_{get_random_string(8)}@gmail.com"

        CustomUser.objects.create_user(
            email=email,
            password="linked123",
            is_staff=True,
            is_active=True,
        )
    modeladmin.message_user(request, "10 dummy users created successfully!", level=messages.SUCCESS)

create_dummy_user.short_description = "Create 10 dummy users"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    ordering = ["email"]
    actions = [create_dummy_user]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and request.POST.get("action") == "create_dummy_user":
            if not self.has_add_permission(request):
                self.message_user(request, "You do not have permission to add users.", level=messages.ERROR)
            else:
                create_dummy_user(self, request, queryset=None)
            return redirect(request.path)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone","role"]
