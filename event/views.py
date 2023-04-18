# from django.shortcuts import render
import random as r

from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, Event, Home
from event.serializers import *
from event.tasks import *
# from django.http import HttpResponse

# otp for forgotPassword
otp = ''


# Used to register User or admin
class UserList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        Users = User.objects.all()
        serializerOfModel = UserSer(Users, many=True)
        # token = AccessToken.for_user(Users)
        resp = Response(serializerOfModel.data, status=status.HTTP_200_OK)
        # r.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    # Used to register User or admin
    def post(self, request):
        print(request.data)
        serializers1 = UserSer(data=request.data)
        try:
            with transaction.atomic():
                serializers1 = UserSer(data=request.data)
                serializers1.is_valid(raise_exception=True)
                if serializers1.is_valid():
                    Users = serializers1.save()
                    send_email.delay(email=request.data["email"], types="register", info={"name": request.data["name"]})
                    # send_email.delay(name = request.data["name"], otp = otp,
                    #                   email = request.data["email"], types = "register")
                    # Users = User.objects.get(username = request.data["username"])
                    # Users = serializers.deserialize('xml', serializers1)
                    # serializers2 = UserSer(data = U)
                    # print("-----------", Users)
                    token = AccessToken.for_user(Users)
                    # print("+++++++++++", type(token))
                    return Response(
                        {"message": "Successfully Registered", "data": serializers1.data, "token": str(token)},
                        status=status.HTTP_201_CREATED)
                return Response(serializers1.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializers1.errors, status=status.HTTP_400_BAD_REQUEST)
            # print("+++++++++++++++++++++++++++++++++-------------------", e)
            # # a = serializers1.save()
            # serializers1.errors['username'][0] = 'Username already taken... \n I think great minds think alike'
            # print("- = - = - = - = - = - = - = -", serializers1.errors['username'][0])
            # serializers1.errors
        # return Response(serializers1.errors, status=status.HTTP_400_BAD_REQUEST)
        # if serializers1.is_valid():
        #     Users = serializers1.save()
        #     send_email.delay(email = request.data["email"], types = "register", info = {"name":request.data["name"]})
        #     # send_email.delay(name = request.data["name"], otp = otp,
        #                           email = request.data["email"], types = "register")
        #     # Users = User.objects.get(username = request.data["username"])
        #     # Users = serializers.deserialize('xml', serializers1)
        #     # serializers2 = UserSer(data = U)
        #     # print("-----------", Users)
        #     token = AccessToken.for_user(Users)
        #     # print("+++++++++++", type(token))
        #     return Response({"message":"Successfully Registered", "data":serializers1.data, "token":str(token)}
        #                       , status=status.HTTP_201_CREATED)
        # # # return Response(serializers1.data, status=status.HTTP_201_CREATED)
        # return Response(serializers1.errors, status=status.HTTP_400_BAD_REQUEST)


# -----> used to directly access the user using tokens
# class UserDetails(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get_object(self, pk):
#         try:
#             user = User.objects.get(id = pk)
#         except User.DoesNotExist:
#             raise Http404
#         return user
#     def get(self, request):
#         pk = request.user.id
#         user = self.get_object(pk)
#         serializers = UserSer(user)
#         username = request.user.username #gets the username of the user in the token
#         print("----------", username)
#         # print("-------------", user)
#         # print("-------------", request.user.isAdmin)
#         if isUser(username, serializers):
#             r = Response(serializers.data, status=status.HTTP_200_OK)
#             r.headers["Access-Control-Allow-Origin"] = "*"
#             return r
#         raise PermissionDenied("User Not Have Permission")
#     def put(self, request):
#         pk = request.user.id
#         user = self.get_object(pk)
#         serializers = UserSer(user, data = request.data)
#         if serializers.is_valid():
#             serializers.save()
#             username = request.user.username
#             # return Response(serializers.data, status=status.HTTP_201_CREATED)
#             if isUser(username, serializers):
#                 return Response(serializers.data, status=status.HTTP_201_CREATED)
#             raise PermissionDenied("User Not Have Permission")
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self, request):
#         pk = request.user.id
#         user = self.get_object(pk)
#         serializers = UserSer(user, data = request.data)
#         username = request.user.username
#         if isUser(username, serializers):
#             user.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         raise PermissionDenied("User Not Have Permission")

# used to delete users and edit users
class UserDetails(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        return user

    def get(self, request, pk):
        user = self.get_object(pk)
        serializerOfModel = UserSer(user)
        return Response(serializerOfModel.data, status=status.HTTP_200_OK)

        #  -----> check current requested user is the user from the tokens
        # username = request.user.username  # gets the username of the user in the token
        # print("----------", username)
        # # print("-------------", user)
        # # print("-------------", request.user.isAdmin)
        # if isUser(username, serializers):
        #     r = Response(serializers.data, status=status.HTTP_200_OK)
        #     r.headers["Access-Control-Allow-Origin"] = "*"
        #     return r
        # raise PermissionDenied("User Not Have Permission")

    # Edits user
    def put(self, request, pk):
        print(request.data)
        information = {"name": ""}
        if request.data["name"] != "":
            information["Updname"] = request.data["name"]
        if request.data["phoneNumber"] != "":
            information["phn"] = request.data["phoneNumber"]
        if request.data["email"] != "":
            information["email"] = request.data["email"]

        user = self.get_object(pk)
        serializersOfUser = UserSer(user, data=request.data, partial=True)
        if serializersOfUser.is_valid():
            serializersOfUser.save()
            username = request.user.username
            information["name"] = user.name
            send_email.delay(email=user.email, types="edit", info=information)
            return Response(serializersOfUser.data, status=status.HTTP_201_CREATED)

            #  -----> check current requested user is the user from the tokens
        #     if isUser(username, serializers):
        #         return Response(serializers.data, status=status.HTTP_201_CREATED)
        #     raise PermissionDenied("User Not Have Permission")
        # return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # used to delete users
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # --> check current requested user is the user from the tokens

        # serializers = UserSer(user, data = request.data)
        # username = request.user.username
        # if isUser(username, serializers):
        #     user.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # raise PermissionDenied("User Not Have Permission")


# used to log in user and admin
class UserLogin(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # print("get request called of user login")
        return Response({"message": "User Not Found in database"}, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        # test_view(request)
        username = request.data['username']
        password = request.data['password']
        print("++++++++++++++++++", request.data)
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            return Response({"message": "Username not correct"}, status=status.HTTP_404_NOT_FOUND)
        serializerOfUser = UserSer(user)
        # print(serializers.data['password'])
        if user.check_password(password):
            token = AccessToken.for_user(user)
            # print("+++++++++++", type(token))
            return Response({"message": "User logged in!!\n", "data": serializerOfUser.data, "token": str(token)},
                            status=status.HTTP_202_ACCEPTED)
        raise AuthenticationFailed("Password do not match")
        # return Response(status=status.HTTP_401_UNAUTHORIZED)


# used for forgot password
class ForgotPassword(APIView):
    def genOtp(self):
        OTP = ""
        for i in range(4):
            OTP += str(r.randint(1, 9))
        return OTP

    # otp = '2121'

    # sends OTP to the mail after verifying the email of the user
    def post(self, request):
        print(request.data)
        username = request.data['username']
        email = request.data['email']
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            return Response({"message": "User Not Found in database"}, status=status.HTTP_404_NOT_FOUND)
        if user.email == email:
            global otp
            otp = self.genOtp()
            # a = send_email.delay(user.name, otp, email)
            send_email.delay(email=request.data["email"], types="OTP", info={"otp": otp, "name": user.name})
            return Response({"message": "Email Send....... Please check your mail"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Mail not send"}, status=status.HTTP_404_NOT_FOUND)

    # used to reset the password
    def put(self, request):
        # user = request.user
        # user = User.objects.get(id = pk)
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User Not Found in database"}, status=status.HTTP_404_NOT_FOUND)
        global otp
        print(request.data["OTP"], otp)
        if request.data["OTP"] == otp:
            print("---------------", request.data["newPassword"])
            user.set_password(request.data["newPassword"])
            user.save()
            return Response({"message": "Password Updated"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "OTP do not match"}, status=status.HTTP_400_BAD_REQUEST)


# used to add An event
class EventList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        Events = Event.objects.all()
        serializersOfEvent = EventSer(Events, many=True)
        return Response(serializersOfEvent.data)

    # used to add An event
    def post(self, request):
        serializersOfEvent = EventSer(data=request.data)
        if serializersOfEvent.is_valid():
            serializersOfEvent.save()
            return Response(serializersOfEvent.data, status=status.HTTP_201_CREATED)
        return Response(serializersOfEvent.errors, status=status.HTTP_400_BAD_REQUEST)
    # --> check current requested user is the adminUser from the tokens
    # if not request.user.isAdmin:
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(serializers.data, status=status.HTTP_201_CREATED)
    #     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    # raise PermissionDenied("User Not Have Permission")


# used to get the events booked by the user
class MyEvents(APIView):
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        # print("++++++++++", user.eventBooked)
        serializersOfEvent = EventSer(user.eventBooked, many=True)
        # print("++++++++++", serializers.data)
        return Response(serializersOfEvent.data, status=status.HTTP_202_ACCEPTED)


# used to edit event and delete event
class EventDetails(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        event = self.get_object(pk)
        serializers = EventSer(event)
        return Response(serializers.data)

    # used to edit event
    def put(self, request, pk):
        event = self.get_object(pk)
        serializers = EventSer(event, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        # --> check current requested user is the adminUser from the tokens
        # if not request.user.isAdmin:
        #     if serializers.is_valid():
        #         serializers.save()
        #         return Response(serializers.data, status=status.HTTP_201_CREATED)
        #     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        # raise PermissionDenied("User Not Have Permission")

    # used to delete event
    def delete(self, request, pk):
        print("Delete Api called of an event")
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # --> check current requested user is the adminUser from the tokens
        # if not request.user.isAdmin:
        #     event.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # raise PermissionDenied("User Not Have Permission")


# used to book event
class Event_Book(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        event = self.get_object(pk)
        user = User.objects.filter(eventBooked=event)
        serializersOfUserEvents = UserEventSer(user, many=True)
        # print(serializers.data)
        # serializers.data['capacity']- = 1
        # if serializers.is_valid():
        #     serializers.save()
        # print("---------\n\n", serializers.data)
        return Response(serializersOfUserEvents.data)

    # used to book event
    def put(self, request, pk):
        user = User.objects.get(id=request.data["id"])
        print(request.user)
        # user = request.user
        event = self.get_object(pk)
        serializersOfEvent = EventSer(event)
        # print("------------------------", serializers.data['name'])

        # print("------------------------", serializersOther.data)
        # print("------------------------", request.data)
        if serializersOfEvent.data['capacity'] > 0:  # checking capacity is greater than 0

            d = {'capacity': serializersOfEvent.data['capacity'] - 1}  # decrementing capacity by one

            # ------>mapping with the user
            if user.eventBooked:
                listOfEvents = [i.id for i in user.eventBooked.all()]
                print("------------", listOfEvents)
                if pk not in listOfEvents:  # checks the event is already in the event booked list of the user
                    listOfEvents.append(pk)
                    d = {'capacity': serializersOfEvent.data['capacity'] - 1}  # decrementing capacity by one
                else:
                    return Response({"message": "Event already booked by the user"},
                                    status=status.HTTP_208_ALREADY_REPORTED)
                print("++++++++++++++", listOfEvents)
                userEvent = {'eventBooked': listOfEvents}
            else:
                userEvent = {'eventBooked': [pk]}
            # user = User.objects.get(id = user.id)
            # print("^^^^^^^^^^^", type(user))
            tag = UserEventSer(user, data=userEvent, partial=True)
            serializersOfEvent = EventSer(event, data=d, partial=True)  # ---->mapping the event with decreased capacity
            # print("-----------------------", tag.is_valid(), user)
            # print("&&&&&&&&&&&&&&&&&&&&&&&&", tag)
            if tag.is_valid():
                # print("Hello!! Tag is valid")
                if serializersOfEvent.is_valid():
                    tag.save()
                    serializersOfEvent.save()
                    # print(serializers.data)
                    send_email.delay(email=user.email, types="book-event",
                                     info={"name": user.name, "eventName": serializersOfEvent.data["name"],
                                           "time": serializersOfEvent.data["startTime"] + "-" +
                                                   serializersOfEvent.data["endTime"]
                                           }
                                     )
                    return Response({"message": "Event Book", "data": serializersOfEvent.data},
                                    status=status.HTTP_201_CREATED)

            return Response({"message": "Event Book", "data": serializersOfEvent.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            # ---> returning the event on different slot with greater capacity than 0
            otherEvents = Event.objects.filter(name__startswith=serializersOfEvent.data['name'], capacity__gte=1)
            # print("------------------------", otherEvents)
            serializersOfEvent = EventSer(otherEvents, many=True)
            events = {}
            for i in otherEvents:
                serializersOther = EventSer(i)
                events[serializersOther.data["name"] + str(serializersOther.data["shows"])] = serializersOther.data[
                    "capacity"]
            print(events)
            return Response({"message": "List", "data": serializersOfEvent.data}, status=status.HTTP_200_OK)

    # used to delete event (not currently we are using temporary post for this)
    def delete(self, request, pk):

        # print("++++++", user.eventBooked.all())
        # user = request.user
        user = User.objects.get(id=request.data["id"])
        event = self.get_object(pk)
        serializersOfEvent = EventSer(event)
        d = {'capacity': serializersOfEvent.data['capacity'] + 1}  # incrementing capacity by one
        serializers1 = EventSer(event, data=d, partial=True)
        user.eventBooked.remove(pk)  # de-mapping the user
        if serializers1.is_valid():
            serializers1.save()
        return Response(serializers1.data, status=status.HTTP_200_OK)
        # user =  User.objects.get(id = request.user.id)
        # print("++++++", user.eventBooked.all())
        # l = [i.id for i in request.user.eventBooked.all()]
        # print(l)
        # l.remove(pk)
        # print(l)
        # userEvent = {"id":request.user.id, 'eventBooked':l}
        # serializers = UserEventSer(request.user, data = userEvent)
        # print("---------\n", serializers.data)
        # if serializers.is_valid():
        #     print("---------\n", serializers.data)
        #     print("Hello! Serializers are valid")
        # serializers.save()
        # serializers.delete() 
        # print("---------\n\n", serializers.data["eventBooked"])
        # serializers.data["eventBooked"].remove(pk)
        # print("---------\n\n", serializers.data)
        # serializers.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


# used to reschedule the booked event of the user (not currently :- using a temporary function)
class EventRes(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # used to reschedule the booked event of the user
    def get(self, request, pk):
        event = self.get_object(pk)
        serializersOfEvent = EventSer(event)
        d = {'capacity': serializersOfEvent.data['capacity'] + 1}  # incrementing capacity by one
        serializers1 = EventSer(event, data=d, partial=True)
        request.user.eventBooked.remove(pk)  # de-mapping the user
        if serializers1.is_valid():
            serializers1.save()
        otherEvents = Event.objects.filter(name__startswith=serializersOfEvent.data['name'], capacity__gte=1).exclude(
            id=serializersOfEvent.data['id'])
        # print("------------------------", otherEvents)

        serializers2 = EventSer(otherEvents, many=True)
        # events = {}
        # for i in otherEvents:
        #     serializersOther = EventSer(i)
        #     events[serializersOther.data["name"]+str(serializersOther.data["shows"])] =
        #     serializersOther.data["capacity"]
        # print(events)
        return Response(serializers2.data, status=status.HTTP_200_OK)
        # return Response(events, status=status.HTTP_200_OK)
    # def put(self,  request,  pk):
    #     event = self.get_object(pk)
    #     a = Event_Book()
    #     # print("-------", a.get(request = request, pk = pk))
    #     ab = a.put(request = request, pk = pk)
    #     print(ab.status_code)
    #     # if ab!= Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST):
    #     if ab.status_code == 201:
    #         print("---------------------", "Hello")
    #     elif ab.status_code == 400:
    #         print("**********************", "bye")
    #     else:
    #         print("+++++++++++++", "NO")

    #     return ab


# used to update the password of the user
class UpdatePassword(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        # user = request.user
        print(request.data)
        user = User.objects.get(id=pk)
        if user.check_password(request.data["oldPassword"]):
            user.set_password(request.data["newPassword"])
            user.save()
            send_email.delay(email=user.email, types="NewPass", info={"name": user.name})

            return Response({"message": "Password Updated"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Password do not match"}, status=status.HTTP_400_BAD_REQUEST)


class HomeList(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        Homes = Home.objects.all()
        serializersOfEvent = HomeSer(Homes, many=True)

        resp = Response(serializersOfEvent.data, status=status.HTTP_200_OK)

        return resp

    # Used to register Home or admin
    def post(self, request):
        print(request.data)
        serializers1 = HomeSer(data=request.data)
        if serializers1.is_valid():
            serializers1.save()

            return Response({"message": "Successfully Registered", "data": serializers1.data},
                            status=status.HTTP_201_CREATED)
            # return Response(serializers1.data, status=status.HTTP_201_CREATED)
        return Response(serializers1.errors, status=status.HTTP_400_BAD_REQUEST)


# checks username user and user from the tokens
def isUser(username, user):
    print(user.is_valid())
    if username == user.data['username']:
        return True
    return False


#######################################################################################################################
#                                                                                                                     #
#                                                 Temporary changes                                                   #
#                                                                                                                     #
#######################################################################################################################

# used to get the user details by post request
class UserDetailsNew(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        return user

    def post(self, request, pk):
        user = self.get_object(pk)
        serializersOfUser = UserSer(user)
        return Response(serializersOfUser.data, status=status.HTTP_200_OK)

        #  -----> check current requested user is the user from the tokens
        # username = request.user.username  # gets the username of the user in the token
        # print("----------", username)
        # # print("-------------", user)
        # # print("-------------", request.user.isAdmin)
        # if isUser(username, serializers):
        #     r = Response(serializers.data, status=status.HTTP_200_OK)
        #     r.headers["Access-Control-Allow-Origin"] = "*"
        #     return r
        # raise PermissionDenied("User Not Have Permission")


# used to get the event details by post request
class EventDetailsNew(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        event = self.get_object(pk)
        serializers = EventSer(event)
        return Response(serializers.data)


# used to get the user details list by post request
class UserListNew(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        Users = User.objects.all()
        serializersOfUser = UserSer(Users, many=True)
        # token = AccessToken.for_user(Users)
        resp = Response(serializersOfUser.data, status=status.HTTP_200_OK)
        # r.headers["Access-Control-Allow-Origin"] = "*"
        return resp


# used to get the list of users booked the event by post request
class Event_BookNew(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        event = self.get_object(pk)
        user = User.objects.filter(eventBooked=event)
        serializersOfUserEvents = UserEventSer(user, many=True)
        # print(serializers.data)
        # serializers.data['capacity']- = 1
        # if serializers.is_valid():
        #     serializers.save()
        # print("---------\n\n", serializers.data)
        return Response(serializersOfUserEvents.data)


# used to reschedule the event already booked by the user by post request
class EventResNew(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        event = self.get_object(pk)
        user = User.objects.get(id=request.data["id"])
        print(event)
        # user = request.user
        serializersOfEvents = EventSer(event)
        d = {'capacity': serializersOfEvents.data['capacity'] + 1}  # incrementing capacity by one
        serializers1 = EventSer(event, data=d, partial=True)
        user.eventBooked.remove(pk)  # de-mapping the user
        if serializers1.is_valid():
            serializers1.save()
            send_email.delay(email=user.email, types="event-res",
                             info={"userid": request.data["id"], "eventId": pk, "name": user.name,
                                   "eventName": serializersOfEvents.data["name"],
                                   "time": serializersOfEvents.data["startTime"] + "-"
                                           + serializersOfEvents.data["endTime"]})
        otherEvents = Event.objects.filter(name__startswith=serializersOfEvents.data['name'], capacity__gte=1).exclude(
            id=serializersOfEvents.data['id'])
        # print("------------------------", otherEvents)

        serializers2 = EventSer(otherEvents, many=True)
        # events = {}
        # for i in otherEvents:
        #     serializersOther = EventSer(i)
        #     events[serializersOther.data["name"]+str(serializersOther.data["shows"])] =
        #     serializersOther.data["capacity"]
        # print(events)
        return Response(serializers2.data, status=status.HTTP_200_OK)


# used to get the event details list by post request
class EventListNew(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        Events = Event.objects.all()
        serializersOfEvents = EventSer(Events, many=True)
        d = {}
        for i in serializersOfEvents.data:
            if d.get(i["name"]):
                d[i["name"]].append(i)
            else:
                d[i["name"]] = [i]

        return Response(serializersOfEvents.data)
        # return Response(d)


# used to delete the event already booked by the user by post request
class Event_Book_Delete(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):

        # print("++++++", user.eventBooked.all())
        # user = request.user
        user = User.objects.get(id=request.data["id"])
        event = self.get_object(pk)
        serializers = EventSer(event)
        d = {'capacity': serializers.data['capacity'] + 1}  # incrementing capacity by one
        serializers1 = EventSer(event, data=d, partial=True)
        user.eventBooked.remove(pk)  # de-mapping the user
        if serializers1.is_valid():
            serializers1.save()
            send_email.delay(email=user.email, types="delete",
                             info={"name": user.name, "eventName": serializers1.data["name"],
                                   "time": serializers1.data["startTime"] + "-" + serializers1.data["endTime"]})
        return Response(serializers1.data, status=status.HTTP_200_OK)


class HomeListNew(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        Users = Home.objects.all()
        serializersOfHome = HomeSer(Users, many=True)
        # token = AccessToken.for_user(Users)
        resp = Response(serializersOfHome.data, status=status.HTTP_200_OK)
        # r.headers["Access-Control-Allow-Origin"] = "*"
        return resp

# #add user easily

# class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSer
#     def get(self, request):
#         return self.list(request)
#     def post(self, request):
#         return self.create(request)
# class UserDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                       mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSer
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
#     def put(self, request, pk):
#         return self.update(request, pk)
#     def delete(self, request, pk):
#         return self.destroy(request, pk)

# add Home images easily
# class HomeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Home.objects.all()
#     serializer_class = HomeSer
#     def get(self, request):
#         return self.list(request)
#     def post(self, request):
#         return self.create(request)
