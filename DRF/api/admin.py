from django.contrib import admin
from .models import Comment, Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User


# Inline ---- **********************************************************

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('product', 'user', 'text', 'is_visible', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ('product', 'quantity', "subtotal")
    readonly_fields = ('cart', "subtotal",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity', 'price', 'total_price')
    readonly_fields = ('price', 'total_price')




# Admin Registration ---- **********************************************************

admin.site.unregister(User)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_visible", "created_at")
    search_fields = ('name', 'is_visible',)
    list_filter = ('is_visible', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product",  "is_visible", "created_at")
    search_fields = ("text", "is_visible", "user__username", "product__title")
    list_filter = ("is_visible", "created_at")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "user", "price", "is_active", "created_at")
    search_fields = ("title",)
    list_filter = ("category", "is_active", "user")
    inlines = [CommentInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price")
    search_fields = ("user__username",)
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "created_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]


