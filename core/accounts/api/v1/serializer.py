from rest_framework import serializers
from ...models import Profile, User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
# ======================================================================================================================
# CustomRegistrationApiView: Handles user registration with password validation
class CustomRegistrationApiView(serializers.ModelSerializer):
    """
    Serializer for user registration, including password confirmation and validation.
    """

    password_confirmation = serializers.CharField(max_length=255, write_only=True)  # Password confirmation field

    class Meta:
        """
        Meta configuration for the serializer.
        """
        model = User  # Defines the associated model (User)
        fields = ("id", "email", "password", "password_confirmation")  # Specifies the fields included in API response

    def validate(self, data):
        """
        Validates that the passwords match and comply with Django's password strength requirements.
        """
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError({"detail": "Passwords do not match."})  # Ensures passwords are identical

        try:
            validate_password(data["password"])  # Runs Django's built-in password validation checks
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})  # Raises validation errors if password is weak

        return data

    def create(self, validated_data):
        """
        Creates a new user after removing the password confirmation field.
        """
        validated_data.pop("password_confirmation")  # Removes the confirmation field before user creation
        user = User.objects.create_user(  # Uses Django's custom user manager to securely create the user
            email=validated_data["email"],
            password=validated_data["password"]
        )
        user.save()  # Saves the user instance in the database
        return user
# ======================================================================================================================
# CustomLoginApiView: Handles user authentication
class CustomLoginApiView(serializers.Serializer):
    """
    Serializer for user login, validating email and password credentials.
    """

    email = serializers.CharField(label=_("Email"), write_only=True)  # Email field
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False,
                                     write_only=True)  # Password field
    token = serializers.CharField(label=_("Token"),
                                  read_only=True)  # Token field (typically used for authentication response)

    def validate(self, attrs):
        """
        Authenticates user credentials and returns user details.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email,
                                password=password)  # Authenticates user

            if not user:  # If authentication fails, return an error
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user  # Adds authenticated user to attributes
        return attrs
# ======================================================================================================================
# CustomProfileSerializer: Handles profile serialization
class CustomProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile details.
    """

    email = serializers.CharField(source="user.email", read_only=True)  # Displays email from the associated user model

    class Meta:
        """
        Meta configuration for the serializer.
        """
        model = Profile  # Specifies the associated Profile model
        fields = (
        "id", "email", "first_name", "last_name", "description")  # Specifies the fields included in API response
        read_only_fields = ["email", "first_name", "last_name"]  # Ensures these fields cannot be modified
# ======================================================================================================================
# CustomChangePasswordSerializer: Handles password change requests
class CustomChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user passwords securely.
    """

    old_password = serializers.CharField(required=True)  # Old password field
    new_password = serializers.CharField(required=True)  # New password field
    password_confirmation = serializers.CharField(required=True)  # Confirmation for the new password

    def validate(self, attrs):
        """
        Ensures the new passwords match.
        """
        if attrs["new_password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError({"detail": "Passwords do not match."})  # Ensures passwords match

        return attrs

    def save(self, **kwargs):
        """
        Saves the new password after validation.
        """
        password = self.validated_data["new_password"]
        user = self.context["request"].user  # Retrieves the current authenticated user
        user.set_password(password)  # Updates the user's password securely
        user.save()  # Saves changes
        return user
# ======================================================================================================================
# CustomResetPasswordSerializer: Handles password reset requests
class CustomResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting a user's password using their email.
    """

    email = serializers.EmailField()  # User's email field
    new_password = serializers.CharField(write_only=True, min_length=8, required=True)  # New password field

    def validate_new_password(self, value):
        """
        Validates the new password using Django's built-in password rules.
        """
        validate_password(value)  # Runs password strength validation
        return value

    def validate(self, data):
        """
        Ensures the email belongs to an existing user.
        """
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "No user associated with this email.")  # Prevents resetting passwords for non-existent users
        return data

    def save(self):
        """
        Updates the user's password after validation.
        """
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)  # Securely updates password
        user.save()

        return user
# ======================================================================================================================
# CustomActivationResendSerializer: Handles resending account activation emails
class CustomActivationResendSerializer(serializers.Serializer):
    """
    Serializer for resending account activation emails to users who have not yet verified their accounts.
    """

    email = serializers.EmailField(required=True)  # Email field

    def validate(self, attrs):
        """
        Checks if the user exists and whether their account is already verified.
        """
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()  # Retrieves user by email

        if not user:
            raise serializers.ValidationError("No user found with this email.")  # Ensures user exists

        if user.is_verified:
            raise serializers.ValidationError(
                "This account is already verified.")  # Prevents resending activation to verified users

        attrs["user"] = user  # Stores user data in attributes
        return attrs
# ======================================================================================================================