from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# ======================================================================================================================
# Custom User Manager: Defines methods for creating standard and superuser accounts
class UserManager(BaseUserManager):
    """
    Custom manager for handling user creation.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')  # Ensures an email is provided

        email = self.normalize_email(email)  # Normalizes email format (e.g., lowercase handling)
        user = self.model(email=email, **extra_fields)  # Creates user instance
        user.set_password(password)  # Hashes and sets the password securely
        user.save()  # Saves the user instance to the database
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and returns a superuser with elevated permissions.
        """
        extra_fields.setdefault('is_staff', True)  # Ensures superuser has staff access
        extra_fields.setdefault('is_superuser', True)  # Ensures superuser privileges
        extra_fields.setdefault('is_active', True)  # Activates the account by default
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')  # Ensures proper staff status
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  # Ensures superuser privileges

        return self.create_user(email, password, **extra_fields)  # Calls the base user creation method

# ======================================================================================================================
# Custom User Model: Defines a custom user model that extends Django’s built-in authentication system
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email instead of username for authentication.
    """

    email = models.EmailField(max_length=255, unique=True)  # Defines email as the unique identifier
    is_staff = models.BooleanField(default=True)  # Determines whether the user can access the admin panel
    is_active = models.BooleanField(default=True)  # Indicates whether the account is active
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Specifies the email field as the primary identifier for authentication
    REQUIRED_FIELDS = []  # No additional required fields beyond email

    objects = UserManager()  # Assigns the custom user manager to handle user creation

    def __str__(self):
        """
        Returns the email as the string representation of the user.
        """
        return self.email

# ======================================================================================================================
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
# ======================================================================================================================
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:  # If a new user is created
        Profile.objects.create(user=instance)
# ======================================================================================================================