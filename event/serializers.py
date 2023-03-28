from rest_framework import serializers
from event.models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','phoneNumber','username','password','isAdmin','eventBooked']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 


class EventSer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class UserEventSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','eventBooked']