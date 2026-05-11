from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    RegisterSerializer,
    TopUpBalanceSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TopUpBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=TopUpBalanceSerializer,
        responses=UserSerializer,
    )
    def post(self, request):
        serializer = TopUpBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        request.user.balance += amount
        request.user.save()

        response_serializer = UserSerializer(request.user)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
