
from rest_framework import serializers

from accounts.models import CustomUser


class UserBattleStatsSerializer(serializers.ModelSerializer):
    wins = serializers.IntegerField(source='stats.wins')
    losses = serializers.IntegerField(source='stats.losses')


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'wins','losses']