from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.conf import settings
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)
from rest_framework.views import APIView
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from ...models import User, Profile
from .serializer import (
    CustomRegistrationApiView,
    CustomLoginApiView,
    CustomProfileSerializer,
    CustomChangePasswordSerializer,
    CustomActivationResendSerializer,
    CustomResetPasswordSerializer,
)


# ======================================================================================================================
# RegisterApiView: Handles user registration
class RegisterApiView(generics.GenericAPIView):
    """
    This API view allows users to register their accounts.
    """

    queryset = User.objects.all()  # Retrieves all users
    serializer_class = CustomRegistrationApiView  # Uses a serializer for validation and user creation
    permission_classes = [
        permissions.AllowAny
    ]  # Allows any user (authenticated or not) to register

    def post(self, request, *args, **kwargs):
        """
        Handles user registration via POST request.
        """
        serializer = self.get_serializer(
            data=request.data
        )  # Serializes the request data
        if serializer.is_valid():
            user = serializer.save()  # Saves the validated user
            return Response(
                {
                    "detail": "User created successfully",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        """
        Retrieves all registered users.
        """
        users = User.objects.all()
        serializer = self.get_serializer(
            users, many=True
        )  # Serializes multiple user instances
        return Response(serializer.data, status=status.HTTP_200_OK)


# ======================================================================================================================
# CustomAuthToken: Handles user authentication and token generation
class CustomAuthToken(ObtainAuthToken):
    """
    This view authenticates a user and returns an authentication token.
    """

    serializer_class = CustomLoginApiView  # Uses CustomLoginApiView for authentication

    def post(self, request, *args, **kwargs):
        """
        Authenticates a user and generates a token.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(
            user=user
        )  # Generates or retrieves an authentication token
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


# ======================================================================================================================
class CustomDeleteToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ======================================================================================================================
# CustomProfileView: Retrieves user profile details
class CustomProfileView(generics.GenericAPIView):
    """
    This API view allows authenticated users to retrieve their profile information.
    """

    queryset = Profile.objects.all()  # Retrieves all profiles
    serializer_class = CustomProfileSerializer  # Uses CustomProfileSerializer for serialization
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Ensures only authenticated users can access profile data

    def get_object(self):
        """
        Retrieves the authenticated user's profile.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, user=self.request.user
        )  # Ensures the profile exists
        return obj


# ======================================================================================================================
# CustomChangePasswordView: Handles password changes for authenticated users
class CustomChangePasswordView(generics.GenericAPIView):
    """
    This API view allows authenticated users to change their password.
    """

    serializer_class = CustomChangePasswordSerializer  # Uses serializer for password validation
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Ensures only logged-in users can change passwords
    queryset = User.objects.all()  # Retrieves all users

    def get_object(self):
        """
        Returns the authenticated user object.
        """
        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Handles password updates via PUT request.
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"detail": "Old password incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(
                serializer.data.get("new_password")
            )  # Securely updates the password
            user.save()
            return Response(
                {"detail": "Password updated."},
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


# ======================================================================================================================
# CustomResetPasswordView: Handles password resets via email
class CustomResetPasswordView(generics.GenericAPIView):
    """
    This API view allows users to reset their password by providing their email.
    """

    serializer_class = CustomResetPasswordSerializer  # Uses CustomResetPasswordSerializer for validation
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Ensures only authenticated users can reset passwords

    def post(self, request, *args, **kwargs):
        """
        Handles password resets via POST request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]

        user = get_object_or_404(User, email=email)
        user.set_password(
            new_password
        )  # Securely updates the password
        user.save()

        return Response(
            {"detail": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )


# ======================================================================================================================
# CustomActivationView: Handles account activation via token verification
class CustomActivationView(APIView):
    """
    This API view verifies a user's activation token and activates their account.
    """

    def get(self, request, token, *args, **kwargs):
        """
        Decodes the activation token and verifies the user.
        """
        try:
            decode = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )  # Decodes the token
            user_id = decode["user_id"]
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(User, id=user_id)

        if not user_obj.is_verified:
            user_obj.is_verified = True
            user_obj.save()
            return Response(
                {"detail": "Verified"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ======================================================================================================================
# CustomActivationResendView: Resends activation email
class CustomActivationResendView(generics.GenericAPIView):
    """
    This API view resends the account activation email.
    """

    serializer_class = CustomActivationResendSerializer  # Uses CustomActivationResendSerializer for validation

    def post(self, request, *args, **kwargs):
        """
        Handles activation email resending via POST request.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)["token"]

        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "matin20001313@gmail.com",
            to=[user_obj.email],
        )

        try:
            email_obj.send()  # Sends activation email
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Email sent successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        """
        Generates an authentication token for the user.
        """
        refresh = RefreshToken.for_user(user)
        return {"token": str(refresh.access_token)}


# ======================================================================================================================
