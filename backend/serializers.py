from rest_framework import serializers
from .models import UserProfile, AuthenticationCode


class UserDetailSerializer(serializers.ModelSerializer):
    # referrals = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ("phone_number", )

    # @staticmethod
    # def get_referrals(obj):
    #     referrals = obj.referrals.all()
    #     return [referral.phone_number for referral in referrals]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class AuthenticationCodeSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationCode
        fields = ('phone_number',)


class AuthenticationCodeVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationCode
        fields = ('code', )
