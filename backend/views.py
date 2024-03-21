import re
import random
import string
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AuthenticationCode, UserProfile, Pet
from .serializers import *


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

        # request.session['phone_number'] = phone_number

        return Response({'message': f'Код подтверждения {auth_code.code} отправлен на номер {phone_number}'})


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = AuthenticationCodeVerifySerializer

    def create(self, request, *args, **kwargs):
        # phone_number = request.session.get('phone_number')
        phone_number = request.data.get('phone_number')
        entered_code = request.data.get('code')
        auth_code = AuthenticationCode.objects.get(phone_number=phone_number)

        if entered_code == auth_code.code and auth_code.expiration_time > timezone.now():
            user, created = UserProfile.objects.get_or_create(phone_number=phone_number)
            auth_code.delete()

            if created:
                user.invite_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                user.save()

            # refresh = RefreshToken.for_user(user)
            # access_token = str(refresh.access_token)

            # return Response({'refresh_token': str(refresh), 'access_token': str(access_token)})

            return Response({"message": "Успешная авторизация"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)


# class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = UserDetailSerializer
#     queryset = UserProfile.objects.all()
#
#
# class UserProfileListCreateView(generics.ListCreateAPIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = UserDetailSerializer
#     queryset = UserProfile.objects.all()

class BaseViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.all()


class CategoryViewSet(BaseViewSet):
    model = Category
    serializer_class = CategoryDetailSerializer


class FoodViewSet(BaseViewSet):
    model = Food
    serializer_class = FoodDetailSerializer


class PurchaseFoodView(generics.CreateAPIView):
    serializer_class = BuyFoodSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        food_id = request.data.get('food_id')
        try:
            user = UserProfile.objects.get(pk=user_id)
            food = Food.objects.get(pk=food_id)
            if user.balance >= food.price:
                user_food, created = UserStorageFood.objects.get_or_create(user=user, food=food)
                if not created:
                    user_food.count += 1
                    user_food.save()
                return Response("Еда успешно куплена", status=status.HTTP_200_OK)
            else:
                return Response("Нехватка средств для покупки", status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)
        except Food.DoesNotExist:
            return Response("Скин не найден", status=status.HTTP_404_NOT_FOUND)


class CategoryFoodViewSet(BaseViewSet):
    model = CategoryFood
    serializer_class = CategoryFoodDetailSerializer


class PersonalityViewSet(BaseViewSet):
    model = Personality
    serializer_class = PersonalityDetailSerializer


class SkinViewSet(BaseViewSet):
    model = Skin
    serializer_class = SkinDetailSerializer


class PurchaseSkinView(generics.CreateAPIView):
    serializer_class = UserStorageSkinDetailSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        skin_id = request.data.get('skin_id')
        try:
            user = UserProfile.objects.get(pk=user_id)
            skin = Skin.objects.get(pk=skin_id)
            if user.balance >= skin.price:
                user.balance -= skin.price
                user.save()
                UserStorageSkin.objects.create(user=user, skin=skin)
                return Response("Скин успешно куплен", status=status.HTTP_200_OK)
            else:
                return Response("Нехватка средств для покупки", status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)
        except Skin.DoesNotExist:
            return Response("Скин не найден", status=status.HTTP_404_NOT_FOUND)


class PetViewSet(BaseViewSet):
    model = Pet
    serializer_class = PetDetailSerializer


class PetPointsAPIView(generics.RetrieveAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetPointsSerializer
    lookup_url_kwarg = 'pk'


class IncreasePetPointsView(generics.CreateAPIView):
    serializer_class = PetPointsIncreaseSerializer

    def perform_create(self, serializer):
        pet_id = serializer.validated_data['pet_id']
        characteristic = serializer.validated_data['characteristic']
        value = serializer.validated_data['value']
        try:
            pet = Pet.objects.get(pk=pet_id)
            if characteristic == 'mood':
                pet.mood_points += value
            elif characteristic == 'purity':
                pet.purity_points += value
            elif characteristic == 'starvation':
                pet.starvation_points += value
            else:
                raise serializers.ValidationError("Неверная характеристика")
            pet.save()
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Питомец не найден")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GameViewSet(BaseViewSet):
    model = Game
    serializer_class = GameDetailSerializer


class UserStorageFoodViewSet(BaseViewSet):
    model = UserStorageFood
    serializer_class = UserStorageFoodDetailSerializer


class UserStorageSkinViewSet(BaseViewSet):
    model = UserStorageSkin
    serializer_class = UserStorageSkinDetailSerializer


class UserProfileViewSet(BaseViewSet):
    model = UserProfile
    serializer_class = UserDetailSerializer


class UserProfileSetNickView(generics.CreateAPIView):
    serializer_class = UserSetNickSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        name = request.data.get('name')
        try:
            user = UserProfile.objects.get(pk=user_id)
            user.name = name
            user.save()
            return Response("Имя пользователя изменено", status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)


class UserProfileEditBalanceView(generics.CreateAPIView):
    serializer_class = UserEditBalanceSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        balance = request.data.get('balance')
        try:
            user = UserProfile.objects.get(pk=user_id)
            user.balance += balance
            user.save()
            return Response("Баланс пользователя изменен", status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)


class AdminViewSet(BaseViewSet):
    model = Admin
    serializer_class = AdminDetailSerializer
