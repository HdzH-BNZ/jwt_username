from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, JoueursSerializer
from .models import User, Joueurs
from rest_framework.decorators import api_view
from rest_framework import status
#need un : pip install pyjwt
import jwt, datetime

# Create your views here.

@api_view(['POST'])
def RegisterView(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def LoginView(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed('Utilisateur non-trouvé')

    if not user.check_password(password):
        raise AuthenticationFailed('Mot de passe incorrect')

    payload= {
        "id" : user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response


@api_view(['GET'])
def UserView(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Non-authentifié')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Jeton expiré, vous êtes non-authentifié')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def LogOutView(request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "details" : "jeton supprimé avec succès"
        }
        return response

@api_view(['GET'])
def getJoueurs(request): 
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    joueurs = Joueurs.objects.all()
    serializer = JoueursSerializer(joueurs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)