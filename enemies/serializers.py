from rest_framework import serializers

from enemies.models import Enemy



class EnemySerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    weakness = serializers.StringRelatedField(many=True)


    class Meta:
        model = Enemy
        fields = '__all__'
