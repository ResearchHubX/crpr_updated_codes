from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'short_message', 'created_at', 'image_preview')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'message')
    ordering = ('-created_at',)
    list_per_page = 20  # Pagination: 20 reviews per page

    def image_preview(self, obj):
        """Display a small preview of the uploaded image in the admin panel."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

    def short_message(self, obj):
        """Display a truncated version of the review message."""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = "Message"

    fieldsets = (
        ('Reviewer Info', {'fields': ('name', 'image')}),
        ('Review Details', {'fields': ('message', 'rating')}),
        ('Meta', {'fields': ('created_at',)}),
    )

    readonly_fields = ('created_at', 'image_preview')

# Register your model here.
from django.contrib import admin
from .models import Projects, Collaborator, ProjectFile

# Inline for Project Files
class ProjectFileInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = ProjectFile
    extra = 1  # Number of empty fields to show by default
    fields = ('file', 'description')  # Fields to display in the inline section

# Inline for Collaborators
class CollaboratorInline(admin.TabularInline):
    model = Collaborator
    extra = 1
    fields = ('name', 'email', 'image')  # Fields to display in the inline section

# Customize Projects Admin Panel
@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'creator', 'status', 'occupation', 'date')
    search_fields = ('name', 'title', 'status', 'creator__username')  # Ensure creator can be searched
    list_filter = ('status', 'occupation', 'postgraduate_type', 'is_secure', 'creator')
    readonly_fields = ('creator', 'date',)
    inlines = [ProjectFileInline, CollaboratorInline]  # Attach inline models here
    fieldsets = (
        ('Project Details', {'fields': ('name', 'title', 'description', 'image', 'creator', 'date')}),
        ('Links & Contact', {'fields': ('email', 'Github_link', 'project_url')}),
        ('Status & Classification', {'fields': ('status', 'occupation', 'postgraduate_type', 'is_secure')}),
    )  # Organizing sections for better readability
     # ✅ Pagination: Limit to 20 projects per page
    list_per_page = 30

# Hide ProjectFile and Collaborator Admin since they are inside Projects
admin.site.register(ProjectFile)
admin.site.register(Collaborator)

admin.site.unregister(ProjectFile)
admin.site.unregister(Collaborator)


@admin.register(NewsAndEvents)
class NewsAndEventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'news_item', 'event_item')
    search_fields = ('title',)
    list_filter = ('news_item', 'event_item')
    
@admin.register(PayPalPayment)
class PayPalPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'amount', 'status', 'created_at')
    search_fields = ('payment_id', 'user__username', 'status')
    list_filter = ('status', 'created_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username',)
    list_filter = ('end_date',)
    readonly_fields = ('is_active',)

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True
    

admin.site.register(Document)

@admin.register(UpdateSubscriber)
class UpdateSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    
     # Make fields read-only
    readonly_fields = ('email', 'name', 'subscribed_at', 'is_active')