import re
import random
import string
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AuthenticationCode, UserProfile, Pet
from .serializers import (
    AuthenticationCodeSendSerializer,
    AuthenticationCodeVerifySerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    PetDetailSerializer
)


# логику перенести
class SendVerificationCodeView(generics.CreateAPIView):
    serializer_class = AuthenticationCodeSendSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Необходимо указать номер телефона'},
                            status=status.HTTP_400_BAD_REQUEST)

        valid_phone = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                               phone_number)

        if not valid_phone:
            return Response({'error': 'Необходимо указать корректный номер телефона'},
                            status=status.HTTP_400_BAD_REQUEST)

        auth_code, created = AuthenticationCode.objects.get_or_create(phone_number=phone_number)

        auth_code.code = ''.join(str(random.randint(0, 9)) for _ in range(4))
        auth_code.expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        auth_code.save()

        request.session['phone_number'] = phone_number

        return Response({'message': f'Код подтверждения {auth_code.code} отправлен на номер {phone_number}'})


# логику перенести
class VerifyCodeView(generics.CreateAPIView):
    serializer_class = AuthenticationCodeVerifySerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.session.get('phone_number')
        entered_code = request.data.get('code')
        auth_code = AuthenticationCode.objects.get(phone_number=phone_number)

        if entered_code == auth_code.code and auth_code.expiration_time > timezone.now():
            user, created = UserProfile.objects.get_or_create(phone_number=phone_number)
            auth_code.delete()

            if created:
                user.invite_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'refresh_token': str(refresh),
                             'access_token': str(access_token)})
        else:
            return Response({'error': 'Неверный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = UserProfile.objects.all()


class UserProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = UserProfile.objects.all()


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PetDetailSerializer
    queryset = Pet.objects.all()


class PetListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PetDetailSerializer
    queryset = Pet.objects.all()
