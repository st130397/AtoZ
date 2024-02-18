import uuid

from rest_framework import status
from rest_framework.response import Response
from .models import Blog, CustomUser
from .serializers import BlogSer, UserSer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from blog.common_utils import Authentication

auth_obj = Authentication()
# Create your views here.

@api_view(["GET"])
def userDetail(request):
    try:
        user_details = auth_obj.authenticate_token(request.GET.get('token', ''))
        if user_details.get('role') == 'admin':
            models = CustomUser.objects.all()
            serilz = UserSer(models, many=True)
            response = []
            for item in serilz.data:
                item.pop('passkey')
                response.append(item)
            return Response({'status': 'success', 'data': response}, status=200)
        return Response({'error': 'Un-authorised Access'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def register(request):
    try:
        data = {}
        if request.method == 'POST':
            data['first_name'] = request.data.get('first_name')
            data['last_name'] = request.data.get('last_name')
            data['mobile_number'] = request.data.get('mobile_number')
            data['email'] = request.data.get('email')
            data['role'] = request.data.get('role')
            data['pincode'] = request.data.get('pincode')
            data['username'] = request.data.get('username')
            data['passkey'] = request.data.get('passkey')
            if auth_obj.validate_email(data['email']) and \
                    auth_obj.validate_password(data['passkey']):
                serializer = UserSer(data=request.data)
                if request.data.get('token', ''):
                    authenticate = auth_obj.authenticate_token(request.data.get('token', ''))
                else:
                    authenticate = auth_obj.authenticate_user(request.data.get('username'), 'author')
                if serializer.is_valid() and authenticate:
                    serializer.save()
                    return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'error', 'data': {'message': 'Invalid Email or Password'}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    try:
        if request.method == 'POST':
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                return Response({'error': 'Unsupported content type'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            user = auth_obj.validate_login(request)
            if user:
                token = auth_obj.generate_token(user)
                if token:
                    user['token'] = token
                    return Response({'status': 'success', 'data': user}, status=200)
                return Response({'error': 'Unable to generate token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def getContent(request):
    try:
        user_details = auth_obj.authenticate_token(request.GET.get('token', ''))
        if user_details:
            models = Blog.objects.all()
            serilz = BlogSer(models, many=True)
            res = []
            for item in serilz.data:
                if item.get('createdBy', '') == user_details.get('username') or \
                        item.get('role', '') == 'admin':
                    res.append(item)
            return Response({'status': 'success', 'data': res}, status=200)
        return Response({'status': 'error', 'data': 'Unauthorized'},
                                            status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def content(request):
    try:
        data = {}
        user_details = auth_obj.authenticate_token(request.data.get('token'))
        if user_details:
            data['title'] = request.data.get('title')
            data['body'] = request.data.get('body')
            data['summary'] = request.data.get('summary')
            data['category'] = request.data.get('category')
            data['createdBy'] = request.data.get('createdBy')
            serilz = BlogSer(data=data)
            if serilz.is_valid():
                serilz.save()
                return Response({'status': 'success', 'data': serilz.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'data': serilz.errors},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'status': 'error', 'data': 'Unauthorized'},
                                status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def updateContent(request):
    try:
        user_details = auth_obj.authenticate_token(request.GET.get('token', ''))
        if user_details:
            try:
                title = request.GET.get('title', '')
                content = Blog.objects.filter(title=title)
            except Blog.DoesNotExist:
                return Response({'status': 'error', 'message': 'Blog not found'},
                                status=status.HTTP_404_NOT_FOUND)
            data = {}
            if user_details.get('role') == 'admin' or user_details.get('username') == content.get('createdBy'):
                data['title'] = request.data.get('title')
                data['body'] = request.data.get('body')
                data['summary'] = request.data.get('summary')
                data['category'] = request.data.get('category')
                data['createdBy'] = request.data.get('createdBy')
                serializer = BlogSer(content, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 'success', 'data': serializer.data})
                else:
                    return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'data': 'Unauthorized'},
                                            status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def deleteContent(request):
    try:
        user_details = auth_obj.authenticate_token(request.GET.get('token', ''))
        if user_details:
            content = None
            try:
                content = Blog.objects.filter(title=request.GET.get('title', ''))
            except Blog.DoesNotExist:
                return Response({'status': 'error', 'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
            if user_details.get('role') == 'admin' or user_details.get('username') == content.get('createdBy'):
                content.delete()
                return Response({'status': 'success', 'message': 'Record Deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'error', 'data': 'Unauthorized'},
                                            status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'error', 'data': {'message': 'Internal Server Error'}},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout(request):
    try:
        if request.method == 'GET':
            user_details = auth_obj.authenticate_token(request.GET.get('token', ''))
            if user_details:
                res = auth_obj.logout(request.GET.get('token', ''))
                if res:
                    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            return Response({'status': 'error', 'data': 'Unauthorized'},
                                            status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def searchContent(request):
    try:
        query = request.GET.get('query', '')
        if query:
            results = Blog.objects.filter(Q(body__icontains=query) | Q(summary__icontains=query) | Q(title__icontains=query) | Q(category__icontains=query))
        else:
            results = Blog.objects.all()
        serializer = BlogSer(results, many=True)

        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


