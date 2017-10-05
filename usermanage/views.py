# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions, status
from rest_framework import generics
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.models import Application
from usermanage.models import *
from usermanage.serializers import *

class Home(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response("HOME")

class CountryView(viewsets.ModelViewSet):
    queryset            = Countries.objects.all()
    serializer_class    = CountriesSerializers
    def create(self, request, *args, **kwargs):
        serializer =   CountriesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"result":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class StateView(viewsets.ModelViewSet):
    queryset            = States.objects.all()
    serializer_class    = StatesSerializer
    def create(self, request, *args, **kwargs):
        serializer = StatesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"result":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"result":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class CityView(viewsets.ModelViewSet):
    queryset            = Cities.objects.all()
    serializer_class    = CitiesSerializers
    def create(self, request, *args, **kwargs):
        serializer  =   CitiesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result":"City saved"})
        else:
            return  Response({"error":serializer.errors})


####### Author : Srinivas 		#####
####### Date   : 18 August 2017	  ###
'''
    Client View is used to create the clients.
    Method takes the input parameters as 
    REQUESTED PARAMETERS: contact_number, requested_by, organization_name and email as a mandatory fields.
    METHOD: Post
    Method checks if the user is exists in out database or not with an email field.
        if user presents then then it throws an error as Email already exists
        else user will be saved to the database and provide the respose to the client.
'''
class ClientView(viewsets.ModelViewSet):
    # permission_classes  =   (IsAuthenticated,)
    queryset            =   Clients.objects.all()
    serializer_class    =   ClientsSerializers
    def create(self, request, *args, **kwargs):
        serializer     =   ClientsSerializers(data=request.data)
        if serializer.is_valid():
            try:
            	user_email  =   Clients.objects.filter(email=request.data['email'])
            	if user_email:
            		return Response({'result':'Email already exists, Please provide another Email Id'}, status=status.HTTP_400_BAD_REQUEST)
            	else:
                    serializer.save()
                    return  Response({'result':'Client details saved succesfully', "data":serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
            	return Response( str(e) )
        else:
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


__author__ = "Srinivas"
####### Date   : 18 August 2017	  ###
'''
    GetClients View is used to get all the clients from the database.
    Method is used when superAdmin wants to get all the client details.
    REQUESTED PARAMETERS: None
    METHOD: Get
'''
class GetClients(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset    =   Clients.objects.all()
        serializer  =   ClientsSerializers(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)

####### Author : Srinivas 		#####
####### Date   : 18 August 2017	  ###
'''
    Update Clien tView is used to update the client details in the database.
    Partial Update method will not ask for all the fields to update.
    It will update only the fields provided by the client for that particular client_id.
    REQUESTED PARAMETERS: field provided by the user with in the model.
    METHOD: Put
'''
class UpdateClient(GenericAPIView, UpdateModelMixin):
    queryset    =   Clients.objects.all()
    serializer_class =  ClientsSerializers
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

####### Author : Srinivas 		#####
####### Date   : 18 August 2017	  ###
'''
    This view is used for Saving or adding user in the database.
    Method is used when superAdmin wants to get all the client details.
'''
class UserSave (viewsets.ModelViewSet):
    queryset            =   Users.objects.all()
    serializer_class	=	UsersSerializers

    def create(self, request, *args, **kwargs):
        serializer = UsersSerializers(data=request.data)
        if serializer.is_valid():
            user            =   Users()
            user.username   =   request.data['email']

            try:
                user.first_name = request.data['first_name']
            except KeyError:
                user.first_name  =   ""

            try:
                user.last_name = serializer.data['last_name']
            except KeyError:
                user.last_name = ""

            try:
                user = Users.objects.get (email=serializer.data['email'])
                return Response ({'email': 'Email Already existed. Please Enter New Email address!'},
                                 status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                pass
                user.email = serializer.data['email']
            except KeyError:
                user.email = ""

            try:
                user.gender = serializer.data['gender']
            except KeyError:
                user.gender = ""

            try:
                user.age = serializer.data['age']
            except KeyError:
                user.gender = ""

            user.is_staff = False

            user.is_superuser = False

            try:
                user.set_password (serializer.data['password'])
            except KeyError:
                user.set_password ("password")

            try:
                user.clients_id =   request.data['clients']
            except KeyError:
                user.clients_id =   1
            user.save ()

            a = None

            try:
                a = Application.objects.get (user=user)
            except ObjectDoesNotExist:
                a = Application.objects.create (user=user,
                                                client_type=Application.CLIENT_CONFIDENTIAL,
                                                authorization_grant_type=Application.GRANT_PASSWORD, name=user.username)
            return_data = {}
            return_data['username']         = user.username
            return_data['client_id']        = a.client_id
            return_data['client_secret']    = a.client_secret
            return_data['user_id']          = user.id
            return Response ({"response":{"status_code":201, "status_message":"CREATED", "data":return_data}}, status=status.HTTP_201_CREATED)
        else:
            return Response ({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)

class UpdateKeywordView(GenericAPIView, UpdateModelMixin):
    queryset            =   Keywords.objects.all()
    serializer_class    =   UpdateKeywordsSerializers
    def put(self, request, keyword_id, *args, **kwargs):
        current_time_date = datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
        serializer = UpdateKeywordsSerializers(data=request.data)
        if serializer.is_valid():
            Keywords.objects.filter(id=keyword_id).update(keyword=request.data['keyword'], clients='1', modified_time=current_time_date)
            return Response({"response":{"status_code":202, "status_message":"ACCEPTED", "data":"updated succesfully"}})
        else:
            return Response({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":serializer.errors}})

class DeleteKeywordView(GenericAPIView, UpdateModelMixin):
    queryset            =   Keywords.objects.all()
    serializer_class    =   DeleteKeywordsSerializers
    def put(self, request, keyword_id, *args, **kwargs):
        current_time_date = datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
        serializer = DeleteKeywordsSerializers(data=request.data)
        if serializer.is_valid():
            Keywords.objects.filter(id=keyword_id).update(status=request.data['status'], clients='1', modified_time=current_time_date)
            return Response({"response":{"status_code":202, "status_message":"ACCEPTED", "data":"updated succesfully"}})
        else:
            return Response({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":serializer.errors}})


class RetrievePreferences(generics.ListAPIView):
    queryset            =   Preferences.objects.all()
    serializer_class    =   PreferencesSerializers
    def get(self, request, user_id=0):
        try:
            preference            =   Preferences.objects.get(users_id=user_id)
            preferenceData        =   PreferencesSerializers(preference)
            preference_data       =   preferenceData.data

            keyword_id            =   preference_data['keywords']
            keyword_object        =   Keywords.objects.get(id=keyword_id)
            keyword_name          =   keyword_object.keyword

            preference_response_data                = {}
            preference_response_data['keywords']    = keyword_name
            preference_response_data['start_date']  = preference_data['start_date']
            preference_response_data['end_date']    = preference_data['end_date']
            return Response(preference_response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response ({"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUserKeywordData(generics.ListAPIView):
    queryset    =   Users.objects.all()
    serializer_class    =   UsersSerializers
    def get(self,request,user_id):
        try:
            user_object     =   Users.objects.get(id=user_id)
            client_id       =   user_object.clients_id
            keyword_data    =   Keywords.objects.filter(clients_id=client_id,status=1)
            keywordlist = []
            for data in keyword_data:
                keyword_dict            = {}
                keyword_serialized_data =   KeywordsSerializers(data)
                keyword_data            =   keyword_serialized_data.data
                keyword_dict['keyword'] = keyword_data['keyword']
                keywordlist.append(keyword_data)
            return Response({"response":{"status_code":200, "statuse_message":"Accepted", "data":keywordlist}})
        except Exception as e:
            return Response(str(e))

# class DeactivateKeyword(generics.CreateAPIView):
#     queryset            =   Keywords.objects.all()
#     serializer_class    =   KeywordsSerializers
#     def create(self,request,*args, **kwargs):
#         try:
#

class GetChannelPages(generics.ListAPIView):
    queryset            =   Channel_page_sources.objects.all()
    serializers_class   =   GetChannelPageSourcesSerializers
    def get(self, request, user_id):
        try:
            user_object             =   Users.objects.get(id=user_id)
            client_id               =   user_object.clients_id
            channel_page_object     =   Channel_page_sources.objects.filter(clients_id=client_id)
            subscribed_list         =   []
            for data in channel_page_object:
                slist = []
                channel_page_data   =   GetChannelPageSourcesSerializers(data)
                subscribed_data = channel_page_data.data
                slist=   channel_page_data.data['source_type']
                slist.append()
                subscribed_list.append(subscribed_data)
            return Response({"response":{"status_code":200, "status_message":"Ok", "data":subscribed_list}})
        except Exception as e:
            return Response(str(e))


class DeleteChannelView(generics.CreateAPIView):
    queryset = Channel_page_sources.objects.all()
    serializer_class = DeleteChannelPageSourcesSerializers

    def put(self, request, channel_id, *args, **kwargs):
        current_time_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = DeleteChannelPageSourcesSerializers(data=request.data)
        if serializer.is_valid():
            Channel_page_sources.objects.filter(id=channel_id).update(status=request.data['status'],
                                                                      clients='1', modified_time=current_time_date)
            return Response(
                {"response": {"status_code": 202, "status_message": "ACCEPTED", "data": "deleted succesfully"}})
        else:
            return Response(
                {"response": {"status_code": 400, "status_message": "BAD REQUEST", "data": serializer.errors}})

class UpdateChannelView(generics.CreateAPIView):
    queryset = Channel_page_sources.objects.all()
    serializer_class = UpdateChannelPageSourcesSerializers

    def put(self, request, channel_id, *args, **kwargs):
        current_time_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = UpdateChannelPageSourcesSerializers(data=request.data)
        if serializer.is_valid():
            Channel_page_sources.objects.filter(id=channel_id).update(
                channel_page=request.data['channel_page'],
                clients='1', modified_time=current_time_date)
            return Response(
                {"response": {"status_code": 202, "status_message": "ACCEPTED",
                              "data": "updated succesfully"}})
        else:
            return Response(
                {"response": {"status_code": 400, "status_message": "BAD REQUEST",
                              "data": serializer.errors}})


                        # def put(self, request, *args, **kwargs):
    #     self.partial_update (request, *args, **kwargs)
    #     return Response({"response":{"status_code":202, "status_message":"ACCEPTED", "data":"updated succesfully"}})

class RetrieveChannelPages(generics.ListAPIView):
    queryset            =   Channel_page_sources.objects.all()
    serializers_class   =   GetChannelPageSourcesSerializers
    def get(self, request, user_id):
        try:
            user_object             =   Users.objects.get(id=user_id)
            client_id               =   user_object.clients_id
            channel_page_object     =   Channel_page_sources.objects.filter(clients_id=client_id,status=1)
            subscribed_list         =   []
            for data in channel_page_object:
                channel_page_data   =   GetChannelPageSourcesSerializers(data)
                subscribed_data     =   channel_page_data.data
                subscribed_list.append(subscribed_data)
            return Response({"response":{"status_code":200, "status_message":"Ok", "data":subscribed_list}})
        except Exception as e:
            return Response(str(e))

class SavePreferences(viewsets.ModelViewSet):
    queryset	        =	Preferences.objects.all()
    serializer_class    =   PreferencesSerializers
    def create(self, request, *args, **kwargs):
        requested_data  =   request.data
        serializer      =   PreferencesSerializers(data=requested_data)
        if serializer.is_valid():
            try:
            	user_exists =   Preferences.objects.get(Q(users__id=request.data['users']))
                #if user_exists:
                self.updatePreference(requested_data, user_exists)
                return Response("User Preferences has been updated.")
                #else:
            except:
                serializer.save()
                return Response("User Preferences has been saved succesfully")
            # except Exception as e:
            #     return Response(str(e))
        else:
            return Response({"Error ":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def updatePreference(self,requested_data, user_exists):
        serializer  =   PreferencesSerializers(user_exists, data=requested_data)
        if serializer.is_valid():
            # serializer.data['modified_time']    =   datetime.datetime.now()
            serializer.save()
            return serializer.data
        else:
            return serializer.errors

class SaveChannelsPages(viewsets.ModelViewSet):
    queryset	        =	Channel_page_sources.objects.all()
    serializer_class    =   ChannelPageSourcesSerializers
    def create(self, request, *args, **kwargs):
        serializer      =   ChannelPageSourcesSerializers(data=request.data)
        if serializer.is_valid():
            channel_exists  =   Channel_page_sources.objects.filter(Q(clients=request.data['clients']),Q(source_type=request.data['source_type']), Q(channel_page=request.data['channel_page']))
            if channel_exists:
                return Response({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":"Channel already present for the client" }}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response ({"response":{"status_code":200, "status_message":"OK", "data": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response":{"status_code":400, "status_message":"BAD REQUEST", "data": serializer.errors}}, status=status.HTTP_201_CREATED)




class KeywordData(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    queryset = Keywords.objects.all()
    serializer_class    =   KeywordsSerializers
    def post(self, request, *args, **kwargs):
        current_time    =   datetime.datetime.now()
        serializer = KeywordsSerializers(data=request.data)
        if serializer.is_valid():
            keywordcheck    =   Keywords.objects.filter(keyword=request.data['keyword'], clients__id=1, status=1)
            if keywordcheck:
                return Response ({"response":{"status_code":400, "status_message":"BAD REQUEST","data":"Keyword already present for the client"}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"response":{"status_code":200, "status_message":"OK","data":serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        print("ID==>", request.data['id'])
        obj = Keywords.objects.get(id=request.data['id'])

        self.partial_update(request,*args, **kwargs)
        # return self.partial_update(request,*args, **kwargs)
        return "Update"


__author__ = "Srinivas"

class LoginView(viewsets.ModelViewSet):

    queryset            =   Users.objects.all()
    serializer_class    =   UsersSerializers

    def list(self, request):
        return Response ({"response":{"status_code":405, 'status_message': 'METHOD NOT ALLOWED', "data":""}}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self,request, *args, **kwargs):
        username        =    request.data['username']
        password        =   request.data['password']

        user = authenticate(username=username,password=password)
        try:
            if user is not None:
                if user.is_active:
                    login (request, user)
                    #return Response ("LOGGED")
                else:
                    return Response ({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":"User is Blocked"}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response ({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":"Invalid User Details"}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response ({"response":{"status_code":400, "status_message":"BAD REQUEST", "data":"Invalid Username or Password"}}, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        a = None
        try:
            a = Application.objects.get(user=user)
        except ObjectDoesNotExist:
            a = Application.objects.create (user=user,
                                            client_type=Application.CLIENT_CONFIDENTIAL,
                                            authorization_grant_type=Application.GRANT_PASSWORD, name=user.username)
        return_data = {}
        return_data['username']                 = user.username
        return_data['user_id']                  = user.id
        return_data['grant_type']               = Application.GRANT_PASSWORD
        return_data['client_id']                = a.client_id
        return_data['client_secret']            = a.client_secret
        return_data['is_preferences_active']    = user.is_preferences_active
        return_data['display_name'] = user.first_name+' '+user.last_name

        return Response ({"response":{"status_code":200, "status_message":"SAVED OK", "data":return_data}}, status=status.HTTP_201_CREATED)



