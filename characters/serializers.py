from rest_framework import serializers

from characters.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    roles = serializers.StringRelatedField(many=True)


    class Meta:
        model = Character
        fields = '__all__'
