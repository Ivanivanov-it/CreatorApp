from rest_framework import serializers

from partners.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    roles = serializers.StringRelatedField(many=True)
    character = serializers.StringRelatedField()


    class Meta:
        model = Partner
        fields = '__all__'
