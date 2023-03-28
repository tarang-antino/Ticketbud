from django.shortcuts import render
from event.models import *
from event.serializers import *
from rest_framework.response import Response
from rest_framework import status,generics,mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class UserList(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        Users=User.objects.all()
        serializers=UserSer(Users,many=True)
        # token=AccessToken.for_user(Users)
        r=Response(serializers.data,status=status.HTTP_200_OK)
        # r.headers["Access-Control-Allow-Origin"] = "*"
        return r
    def post(self,request):
        serializers1=UserSer(data=request.data)
        if serializers1.is_valid():
            Users=serializers1.save()
            # Users=User.objects.get(username=request.data["username"])
            # Users=serializers.deserialize('xml',serializers1)
            # serializers2=UserSer(data=U)
            # print("-----------",Users)
            token=AccessToken.for_user(Users)
            # print("+++++++++++",type(token))
            return Response({"data":serializers1.data,"token":str(token)},status=status.HTTP_201_CREATED)
            # return Response(serializers1.data,status=status.HTTP_201_CREATED)
        return Response(serializers1.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            user=User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        return user
    def get(self,request,pk):
        user=self.get_object(pk)
        serializers=UserSer(user)
        username = request.user.username #gets the username of the user in the token
        print("----------",username)
        # print("-------------",user)
        # print("-------------",request.user.isAdmin)
        if isUser(username,serializers):
            r=Response(serializers.data,status=status.HTTP_200_OK)
            r.headers["Access-Control-Allow-Origin"] = "*"
            return r
        raise PermissionDenied("User Not Have Permission")
    def put(self,request,pk):
        user=self.get_object(pk)
        serializers=UserSer(user,data=request.data)
        if serializers.is_valid():
            serializers.save()
            username = request.user.username
            # return Response(serializers.data,status=status.HTTP_201_CREATED)
            if isUser(username,serializers):
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            raise PermissionDenied("User Not Have Permission")
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        user=self.get_object(pk)
        serializers=UserSer(user,data=request.data)
        username = request.user.username
        if isUser(username,serializers):
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("User Not Have Permission")

class UserLogin(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        try:
            user=User.objects.get(username=username)
            
        except User.DoesNotExist:
             raise AuthenticationFailed("User Not Found")
        serializers=UserSer(user)
        # print(serializers.data['password'])
        if user.check_password(password):
                raise AuthenticationFailed("Password Dont match!!")
                # return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        token=AccessToken.for_user(user)
            # print("+++++++++++",type(token))
        return Response({"data":serializers.data,"token":str(token)},status=status.HTTP_202_CREATED)
        
        

class EventList(APIView):
    def get(self,request):
        Events=Event.objects.all()
        serializers=EventSer(Events,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=EventSer(data=request.data)
        if request.user.isAdmin:
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("User Not Have Permission")

class EventDetails(APIView):
    def get_object(self,pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,pk):
        event=self.get_object(pk)
        serializers=EventSer(event)
        return Response(serializers.data)
    def put(self,request,pk):
        event=self.get_object(pk)
        serializers=EventSer(event,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        event=self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Event_Book(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,pk):
        event=self.get_object(pk)
        
        serializers=EventSer(event)
        # print(serializers.data)
        # serializers.data['capacity']-=1
        # if serializers.is_valid():
        #     serializers.save()
        # print("---------\n\n",serializers.data)
        return Response(serializers.data)
    
    def put(self,request,pk):
        event=self.get_object(pk)
        serializers=EventSer(event)
        # print("------------------------",serializers.data['name'])
        otherEvents=Event.objects.filter(name__startswith=serializers.data['name'] , capacity__gte=0)
        # print("------------------------",otherEvents)
        for i in otherEvents:
            serializersOther=EventSer(i)
            # print("------------------------",serializersOther.data)
        # print("------------------------",request.data)
        if serializers.data['capacity']>0:
            
            d={'capacity':serializers.data['capacity']-1}
            
        else:
            d={'capacity':serializers.data['capacity']}
            # request.data
            otherEvents=Event.objects.filter(name=serializers.data['name'] , capacity__gte=0)
        
        serializers=EventSer(event,data=d,partial=True)
        userEvent={'eventBooked':[pk]}
        # user=User.objects.get(id=request.user.id)
        # print("^^^^^^^^^^^",type(request.user))
        tag=UserEventSer(request.user,data=userEvent,partial=True)
        # print("-----------------------",tag.is_valid(),request.user)
        # print("&&&&&&&&&&&&&&&&&&&&&&&&",tag)
        if tag.is_valid():
            # print("Helooooooooo")
            tag.save()
        #     print("-----------------------",tag.data)
        if serializers.is_valid():
            event=serializers.save()
            # userEvent={'eventBooked':[pk]}
            # # user=User.objects.get(id=request.user.id)
            # print("^^^^^^^^^^^",type(event))
            # tag=UserEventSer(request.user,data=userEvent,partial=True)
            # print("-----------------------",tag.is_valid(),tag.errors,request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

def isUser(username,user):
    if username==user.data['username']:
        return True
    return False




#add user easily

# class UserList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSer
#     def get(self,request):
#         return self.list(request)
#     def post(self,request):
#         return self.create(request)
# class UserDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSer
#     def get(self,request,pk):
#         return self.retrieve(request,pk)
#     def put(self,request,pk):
#         return self.update(request,pk)
#     def delete(self,request,pk):
#         return self.destroy(request,pk)