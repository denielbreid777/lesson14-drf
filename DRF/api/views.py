from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, ValidationError

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthor, IsModerated, IsCartOwner

from .models import Category, Product, Comment, CartItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from .serializers import (CategorySerializer, UserSerializer, ProductSerializer, CommentSerializer, 
                          CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, CartItemCreateSerializer)

from rest_framework.pagination import PageNumberPagination



class APIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000




#----------User Below **********************************************************
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#----------Category Below **********************************************************
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


#----------Product Below **********************************************************
class ProductListView(ListAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = APIListPagination

class MyProductsListView(ListAPIView): 
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = APIListPagination
    
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class ProductRetrieveView(RetrieveAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class ProductDeleteView(DestroyAPIView):    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

class ProductUpdateView(UpdateAPIView):
    # queryset = Product.objects.all().filter(is_visible=True)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


#----------Comment Below **********************************************************
# class CommentListView(ListAPIView):
#     # queryset = Comment.objects.all().filter(is_visible=True)
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     # permission_classes = [IsModerated]

class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    
class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

#----------Cart Below **********************************************************

class CartRetriveView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        print("CURRENT USER:", self.request.user.username, self.request.user.id)
        return Cart.objects.get_or_create(user=self.request.user)

#?????????????????????????

class CartListView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = APIListPagination

class CartItemListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = APIListPagination


class CartItemCreateView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = self.request.user.cart
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        item = CartItem.objects.filter(cart=cart, product=product).first()

        if item:
            item.quantity += quantity
            item.save()
        else:
            serializer.save(cart=cart)

class CartItemUpdateView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

class CartItemDeleteView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]


#----------Order Below **********************************************************

class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = APIListPagination

    # def get_queryset(self):
    #     return Order.objects.filter(user=self.request.user)
    

class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = self.request.user.cart
        items = cart.items.all()

        if not items.exists():
            raise ValidationError("Cart is empty.")

        order = serializer.save(user=self.request.user, total_price=cart.total_price)

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.subtotal
            )

        items.delete()


#----------Admin Below **********************************************************
 
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = APIListPagination
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]