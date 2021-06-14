from rest_framework import serializers
from .models import User, Joueurs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'username']
        #pour cacher le mot de passe dans le retour du POST
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    #pour le haching :
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class JoueursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joueurs
        fields = '__all__'