from rest_framework import serializers

from employee.models import EmployeeTree


class ParentSerializer(serializers.ModelSerializer):  # Этот класс нужен, чтобыы нормально сер-ать full_name родителя
    class Meta:
        model = EmployeeTree
        fields = ('full_name',)


class EmployeeTreeSerializer(serializers.ModelSerializer):
    # parent = ParentSerializer(read_only=True)
    hired_at = serializers.DateField('%B %d, %Y')
    is_leaf = serializers.BooleanField(source="is_leaf_node")

    class Meta:
        model = EmployeeTree
        fields = ('pk', 'full_name', 'hired_at', 'salary', 'level', 'is_leaf','image')
