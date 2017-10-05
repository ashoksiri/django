from rest_framework.serializers import ModelSerializer
from usermanage.models import *
from rest_framework import serializers

class CountriesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =   Countries
        fields  =   ('id','country_name','created_time','modified_time')

class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model   =   States
        fields  =   ('id','state_name','created_time','modified_time','countries')

class CitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =   Cities
        fields  =   ('id','city_name','created_time','modified_time','states')

class ClientsSerializers(serializers.ModelSerializer):
    class Meta:
        model   =   Clients
        fields  =   ('id','organization_name','address','contact_number','phone_number','email','row_status','requested_by','created_time','modified_time')

class UsersSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, read_only=True)
    class Meta:
        model = Users
        fields = ('id','username','first_name','password','last_name','email','age','gender','mobile_number','user_type','created_time','modified_time','clients')

    def get_validation_exclusions(self):
        exclusions = super(UsersSerializers, self).get_validation_exclusions()
        return exclusions + ['email']

class KeywordsSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Keywords
        fields  =   ('id','keyword','created_time','modified_time','source_type','status','clients')

class UpdateKeywordsSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Keywords
        fields  =   ('id','keyword','modified_time')

class DeleteKeywordsSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Keywords
        fields  =   ('id','status','modified_time')

class UpdateChannelPageSourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Channel_page_sources
        fields  =   ('id','channel_page','status','modified_time')

class DeleteChannelPageSourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Channel_page_sources
        fields = ('id', 'status', 'modified_time')



class PreferencesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Preferences
        fields  =   ('id','start_date','end_date','created_time','modified_time','row_status','requested_by','keywords','users')

class ChannelPageSourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Channel_page_sources
        fields  =   ('id','source_type','channel_page','created_time','status','modified_time','row_status','requested_by','clients')

class GetChannelPageSourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model   =	Channel_page_sources
        fields  =   ('id','source_type','channel_page','status','clients')