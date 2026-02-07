from django.contrib import admin
from .models import Conversation, Message, Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "parent", "order", "created_at"]
    list_filter = ["user", "created_at"]
    search_fields = ["name", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["user", "order", "name"]


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["role", "content", "agent", "is_auto_chat", "created_at"]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "conversation_type",
        "user",
        "folder",
        "created_at",
        "updated_at",
    ]
    list_filter = ["conversation_type", "folder", "created_at"]
    search_fields = ["title", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [MessageInline]

    filter_horizontal = ["agents"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["conversation", "role", "agent", "is_auto_chat", "created_at"]
    list_filter = ["role", "is_auto_chat", "created_at"]
    search_fields = ["content", "conversation__title"]
    readonly_fields = ["created_at"]
