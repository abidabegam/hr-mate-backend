from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models.onboarding_task import OnboardingTask
from .models.referral import Referral
from .models.performance_review import PerformanceReview
from .models.notification import Notification
from .models.message import Message
from .models import UserDetails, RegistrationRequest

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role'
    )
    list_filter = (
        'is_staff',
        'is_active',
        'role'
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extra info'), {'fields': ('role',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'role'
            )
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not obj.username:
            obj.username = obj.email.split('@')[0]
        super().save_model(request, obj, form, change)


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'manager',
        'department',
        'salary',
        'bonus',
        'stock_options',
        'approved',
        'updated_at',
        'phone',
        'created_at'
    )
    search_fields = (
        'user__email',
        'manager__email',
        'department'
    )
    list_filter = (
        'approved',
        'department',
        'created_at'
    )
    readonly_fields = (
        'updated_at',
        'created_at'
    )
    fields = (
        'user',
        'manager',
        'job',
        'department',
        'job_title',
        'location',
        'salary',
        'bonus',
        'stock_options',
        'profile_picture',
        'approved',
        'updated_at',
        'phone'
    )


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'posted_at',
        'is_approved'
    )
    search_fields = ('user__email',)
    list_filter = (
        'is_approved',
        'posted_at'
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'recipient',
        'text',
        'timestamp',
        'is_read'
    )
    list_filter = (
        'is_read',
        'timestamp'
    )
    search_fields = (
        'text',
        'sender__email',
        'recipient__email'
    )


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'completed',
        'due_date',
        'created_at'
    )
    search_fields = (
        'title',
        'user__email'
    )
    list_filter = (
        'completed',
        'created_at'
    )
    fields = (
        'user',
        'title',
        'description',         # ✅ Add this line
        'due_date',            # ✅ Add this line
        'completed',
        'uploaded_document'
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'position',
        'referrer',
        'status',
        'created_at'
    )
    search_fields = (
        'full_name',
        'email',
        'position'
    )
    list_filter = (
        'status',
        'created_at'
    )


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'reviewer',
        'rating',
        'created_at'
    )
    search_fields = (
        'user__email',
        'reviewer__email'
    )
    list_filter = (
        'created_at',
        'rating'
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'is_read',
        'created_at'
    )
    search_fields = (
        'user__email',
        'message'
    )
    list_filter = (
        'is_read',
        'created_at'
    )
