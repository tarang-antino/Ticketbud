from rest_framework import serializers
from event.models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','phoneNumber','username','password','isAdmin'
                ,'eventBooked'
                    # ,"is_superuser"
                ]
        # fields='__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        # print(validated_data)
        password=validated_data.pop('password',None)
        # is_superuser=validated_data.pop("is_superuser",None)
        isAdmin=validated_data.pop("isAdmin",None)
        # print(password,isAdmin,is_superuser)
        instance=self.Meta.model(**validated_data)
        # print(instance.is_superuser)
        if password is not None:
            instance.set_password(password)
        # if is_superuser is not None:
        if isAdmin is not None:
            instance.is_superuser=isAdmin
            instance.isAdmin=isAdmin
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