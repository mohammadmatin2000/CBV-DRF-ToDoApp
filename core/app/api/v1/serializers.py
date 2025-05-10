from rest_framework import serializers
from ...models import ToDoApp


# ======================================================================================================================
# UserSerializer: A serializer for converting ToDoApp model instances into JSON format
class UserSerializer(serializers.ModelSerializer):
    """
    This serializer transforms ToDoApp model data into JSON responses for the API.
    """

    absolute_url = (
        serializers.SerializerMethodField()
    )  # Generates an absolute API URL for the object

    class Meta:
        """
        Meta class defines the configuration for the serializer.
        """

        model = ToDoApp  # Specifies that this serializer is based on the ToDoApp model
        fields = (
            "id",
            "author",
            "content",
            "absolute_url",
        )  # Defines the fields to be included in the API response

    def get_absolute_url(self, obj):
        """
        Generates the absolute URL for the object using the request context.
        """
        return self.context["request"].build_absolute_uri(
            obj.pk
        )  # Builds a fully qualified URL for the object

    def to_representation(self, obj):
        """
        Customizes the serializer representation before sending the API response.
        """
        request = self.context[
            "request"
        ]  # Retrieves the request context
        rep = super().to_representation(
            obj
        )  # Calls the base representation method

        # If a specific object (based on primary key) is requested, remove the absolute_url field from the response
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop(
                "absolute_url"
            )  # Prevents absolute URL from appearing when retrieving a single object

        return rep  # Returns the customized response dictionary


# ======================================================================================================================
