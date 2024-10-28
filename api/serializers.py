from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        # This ensures that fields not provided in the request remain unchanged
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
