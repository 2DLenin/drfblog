from rest_framework import serializers
from .models import Entry, UserProfile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, \
    CommonPasswordValidator, NumericPasswordValidator


class UserProfileCreateSerializer(serializers.ModelSerializer):

    UserProfile = serializers.ReadOnlyField(source='profile.nickname')
    nickname = serializers.CharField(source="profile.name")
    avatar = serializers.ImageField(source="profile.avatar", required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname', 'avatar', 'UserProfile')
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [CommonPasswordValidator().validate,
                                                            MinimumLengthValidator().validate,
                                                            NumericPasswordValidator().validate,
                                                            UserAttributeSimilarityValidator().validate]
                         },
            'username': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            'nickname': {'validators': [UniqueValidator(queryset=User.objects.all())]}
        }

    def create(self, validated_data):
        credentials = {'username': validated_data.pop('username'), 'password': validated_data.pop('password')}
        user = User.objects.create_user(**credentials)
        user_profile_data = {'user': user, **validated_data}
        UserProfile.objects.create(**user_profile_data)
        return user


class EntryCreateSerializer(serializers.ModelSerializer):

    class CurrentAuthor:

        requires_context = True

        def __call__(self, serializer_field):
            return serializer_field.context['request'].user.profile

        def __repr__(self):
            return '%s()' % self.__class__.__name__

    author = serializers.HiddenField(default=CurrentAuthor())

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'author', 'preview_image', 'topic',)


class EntryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'author', 'preview_image', 'topic',)


class RateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'






