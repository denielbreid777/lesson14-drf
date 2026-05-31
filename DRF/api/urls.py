from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ( UserView,
                    CategoryCreateView, CategoryDeleteView, CategoryListView, 
                    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductRetrieveView,
                    MyProductsListView,
                    CommentCreateView, CommentUpdateView, CommentDeleteView, 
                    CartRetriveView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView, CartItemListView,
                    OrderListView, OrderCreateView,
                    AdminProductViewSet, AdminCommentViewSet, AdminUserViewSet)

router = DefaultRouter()
router.register('admin/products', AdminProductViewSet)
router.register('admin/comments', AdminCommentViewSet)
router.register('admin/users', AdminUserViewSet)


urlpatterns = [
    #---Admin Below 
    path('', include(router.urls)),
    # path('admin/users/', AdminUserListView.as_view()),
    # path('admin/user/create/', AdminUserCreateView.as_view()),
    # path('admin/user/<int:pk>/update/', AdminUserUpdateView.as_view()),
    # path('admin/user/<int:pk>/delete/', AdminUserDeleteView.as_view()),
    
    #---author Below 
    path('auth/register/', UserView.as_view()),

    #---category Below 
    path('categories/', CategoryListView.as_view()),
    path('categories/', CategoryCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDeleteView.as_view()),

    #---product Below 
    path('products/', ProductListView.as_view()),
    path('products/my_products/', MyProductsListView.as_view()),
    path('products/<int:pk>', ProductRetrieveView.as_view()),
    path('products/auth/', ProductCreateView.as_view()),
    path('products/auth/<int:pk>/', ProductUpdateView.as_view()),
    path('products/auth/<int:pk>/', ProductDeleteView.as_view()),

    #---comment Below
    # path('comments/', CommentListView.as_view()),
    path('comments/create/', CommentCreateView.as_view()),
    path('comments/<int:pk>/', CommentUpdateView.as_view()),
    path('comments/<int:pk>/', CommentDeleteView.as_view()),

    #---cart Below 
    # path('cart/items/', CartItemListView.as_view()),
    path('cart_item/auth/', CartItemCreateView.as_view()),
    path('cart/auth/<int:pk>/', CartItemUpdateView.as_view()),
    path('cart/auth/<int:pk>/', CartItemDeleteView.as_view()),
    
    #---cart Below 
    path('order/', OrderListView.as_view()),
    path('order/', OrderCreateView.as_view()),

    #---token Below 
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

]  
