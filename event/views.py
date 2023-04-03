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
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        Users=User.objects.all()
        serializers=UserSer(Users,many=True)
        # token=AccessToken.for_user(Users)
        r=Response(serializers.data,status=status.HTTP_200_OK)
        # r.headers["Access-Control-Allow-Origin"] = "*"
        return r
    def post(self,request):
        print(request.data)
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

# -----> used to directly access the user using tokens
# class UserDetails(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get_object(self,pk):
#         try:
#             user=User.objects.get(id=pk)
#         except User.DoesNotExist:
#             raise Http404
#         return user
#     def get(self,request):
#         pk=request.user.id
#         user=self.get_object(pk)
#         serializers=UserSer(user)
#         username = request.user.username #gets the username of the user in the token
#         print("----------",username)
#         # print("-------------",user)
#         # print("-------------",request.user.isAdmin)
#         if isUser(username,serializers):
#             r=Response(serializers.data,status=status.HTTP_200_OK)
#             r.headers["Access-Control-Allow-Origin"] = "*"
#             return r
#         raise PermissionDenied("User Not Have Permission")
#     def put(self,request):
#         pk=request.user.id
#         user=self.get_object(pk)
#         serializers=UserSer(user,data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             username = request.user.username
#             # return Response(serializers.data,status=status.HTTP_201_CREATED)
#             if isUser(username,serializers):
#                 return Response(serializers.data,status=status.HTTP_201_CREATED)
#             raise PermissionDenied("User Not Have Permission")
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request):
#         pk=request.user.id
#         user=self.get_object(pk)
#         serializers=UserSer(user,data=request.data)
#         username = request.user.username
#         if isUser(username,serializers):
#             user.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         raise PermissionDenied("User Not Have Permission")

class UserDetails(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            user=User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        return user
    def get(self,request,pk):
        user=self.get_object(pk)
        serializers=UserSer(user)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
        #  -----> check current requested user is the user from the tokens
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
        serializers=UserSer(user,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            username = request.user.username
            return Response(serializers.data,status=status.HTTP_201_CREATED)

            #  -----> check current requested user is the user from the tokens
            if isUser(username,serializers):
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            raise PermissionDenied("User Not Have Permission")
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # --> check current requested user is the user from the tokens

        # serializers=UserSer(user,data=request.data)
        # username = request.user.username
        # if isUser(username,serializers):
        #     user.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # raise PermissionDenied("User Not Have Permission")

class UserLogin(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        try:
            user=User.objects.get(username=username)
            
        except User.DoesNotExist:
             raise AuthenticationFailed("User Not Found in database")
        serializers=UserSer(user)
        # print(serializers.data['password'])
        if user.check_password(password):
                token=AccessToken.for_user(user)
            # print("+++++++++++",type(token))
                return Response({"data":serializers.data,"token":str(token)},status=status.HTTP_202_ACCEPTED)
        raise AuthenticationFailed("Password Dont match!!")
                # return Response(status=status.HTTP_401_UNAUTHORIZED)


class EventList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        Events=Event.objects.all()
        serializers=EventSer(Events,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=EventSer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    # --> check current requested user is the adminuser from the tokens
        # if not request.user.isAdmin:
        #     if serializers.is_valid():
        #         serializers.save()
        #         return Response(serializers.data,status=status.HTTP_201_CREATED)
        #     return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        # raise PermissionDenied("User Not Have Permission")

class EventDetails(APIView):
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
        return Response(serializers.data)
    
    # need to add only if admin in put of eventdetails
    def put(self,request,pk):
        event=self.get_object(pk)
        serializers=EventSer(event,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
        # --> check current requested user is the adminuser from the tokens
        # if not request.user.isAdmin:
        #     if serializers.is_valid():
        #         serializers.save()
        #         return Response(serializers.data,status=status.HTTP_201_CREATED)
        #     return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        # raise PermissionDenied("User Not Have Permission")
    
    # need to add only if admin in delete of eventdetails
    def delete(self,request,pk):
        event=self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        # --> check current requested user is the adminuser from the tokens
        # if not request.user.isAdmin:
        #     event.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # raise PermissionDenied("User Not Have Permission")

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
        user= User.objects.get(id=request.user.id)
        serializers=UserEventSer(user)
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
        
            # print("------------------------",serializersOther.data)
        # print("------------------------",request.data)
        if serializers.data['capacity']>0:  #checking capacity is greater than 0
            
            d={'capacity':serializers.data['capacity']-1} #decrementing capacity by one
            
            # ------>mapping with the user
            if request.user.eventBooked:
                l=[i.id for i in request.user.eventBooked.all()]
                print("------------",l)
                if pk not in l: #checks the event is already in the event booked list of the user
                    l.append(pk)
                    d={'capacity':serializers.data['capacity']-1} #decrementing capacity by one
                else:
                    return Response({"message":"Event already booked by the user"},status=status.HTTP_208_ALREADY_REPORTED)
                print("++++++++++++++",l)
                userEvent={'eventBooked':l}
            else:
                userEvent={'eventBooked':[pk]}
            # user=User.objects.get(id=request.user.id)
            # print("^^^^^^^^^^^",type(request.user))
            tag=UserEventSer(request.user,data=userEvent,partial=True)
            serializers=EventSer(event,data=d,partial=True) # ------>mapping the event with decreased capacity
            # print("-----------------------",tag.is_valid(),request.user)
            # print("&&&&&&&&&&&&&&&&&&&&&&&&",tag)
            if tag.is_valid():
                # print("Helooooooooo")
                if serializers.is_valid():
                    tag.save()
                    serializers.save()
                    # print(serializers.data)
            
                    return Response(serializers.data,status=status.HTTP_201_CREATED)

            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            # ---> returning the event on different slot with greater capacity than 0
            otherEvents=Event.objects.filter(name__startswith=serializers.data['name'] , capacity__gte=1)
            # print("------------------------",otherEvents)
            events={}
            for i in otherEvents:
                serializersOther=EventSer(i)
                events[serializersOther.data["name"]+str(serializersOther.data["shows"])]=serializersOther.data["capacity"]
            print(events)
            return Response(events,status=status.HTTP_200_OK)

    
    
    def delete(self,request,pk):
        
        # print("++++++",request.user.eventBooked.all())
        
        event=self.get_object(pk)
        serializers=EventSer(event)
        d={'capacity':serializers.data['capacity']+1} #incrementing capacity by one
        serializers1=EventSer(event,data=d,partial=True)
        request.user.eventBooked.remove(pk) #demapping the user
        if serializers1.is_valid():
            serializers1.save()
        return Response(serializers1.data,status=status.HTTP_200_OK)
        # user= User.objects.get(id=request.user.id)
        # print("++++++",user.eventBooked.all())
        # l=[i.id for i in request.user.eventBooked.all()]
        # print(l)
        # l.remove(pk)
        # print(l)
        # userEvent={"id":request.user.id,'eventBooked':l}
        # serializers=UserEventSer(request.user,data=userEvent)
        # print("---------\n",serializers.data)
        # if serializers.is_valid():
        #     print("---------\n",serializers.data)
        #     print("Helooooooooo")
            # serializers.save()
        # serializers.delete() 
        # print("---------\n\n",serializers.data["eventBooked"]) 
        # serializers.data["eventBooked"].remove(pk)
        # print("---------\n\n",serializers.data)
        # serializers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventRes(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get (self,request,pk):
        event=self.get_object(pk)
        serializers=EventSer(event)
        d={'capacity':serializers.data['capacity']+1} #incrementing capacity by one
        serializers1=EventSer(event,data=d,partial=True)
        request.user.eventBooked.remove(pk) #demapping the user
        if serializers1.is_valid():
            serializers1.save()
        otherEvents=Event.objects.filter(name__startswith=serializers.data['name']).exclude(id=serializers.data['id'])
        # print("------------------------",otherEvents)
        
        serializers2=EventSer(otherEvents,many=True)
        # events={}
        # for i in otherEvents:
        #     serializersOther=EventSer(i)
        #     events[serializersOther.data["name"]+str(serializersOther.data["shows"])]=serializersOther.data["capacity"]
        # print(events)
        return Response(serializers2.data,status=status.HTTP_200_OK)
        # return Response(events,status=status.HTTP_200_OK)
    # def put(self, request, pk):
    #     event=self.get_object(pk)
    #     a=Event_Book()
    #     # print("-------",a.get(request=request,pk=pk))
    #     ab=a.put(request=request,pk=pk)
    #     print(ab.status_code)
    #     # if ab!=Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST):
    #     if ab.status_code==201:
    #         print("---------------------","Hello")
    #     elif ab.status_code==400:
    #         print("**********************","bye")
    #     else:
    #         print("+++++++++++++","nooooooo")
        
    #     return ab
        
        

class UpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        # user=request.user
        user = User.objects.get(id=pk)
        if user.check_password(request.data["oldPassword"]):
            user.set_password(request.data["newPassword"])
            return Response({"message":"Password Updated"},status=status.HTTP_202_ACCEPTED)
        return Response({"message":"Password do not match"},status=status.HTTP_400_BAD_REQUEST)

def isUser(username,user):
    print(user.is_valid())
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
    # queryset=User.objects.all()
    # serializer_class=UserSer
    # def get(self,request,pk):
    #     return self.retrieve(request,pk)
    # def put(self,request,pk):
    #     return self.update(request,pk)
    # def delete(self,request,pk):
    #     return self.destroy(request,pk)