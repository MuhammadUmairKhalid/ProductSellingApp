from rest_framework import serializers
# from models import User
class SignupSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    usertype=serializers.CharField()
    def validate(self, data):
        if 'email' not in data:
            raise serializers.ValidationError({"Email":"This field is required."})
        if 'username' not in data:
            raise serializers.ValidationError({"OTP":"This field is required."})
        if 'password' not in data:
            raise serializers.ValidationError({"OTP":"This field is required."})
        if type(data['email']) != str:
            raise serializers.ValidationError({"Email":"This field should be string."})
        if type(data['username']) != str:
            raise serializers.ValidationError({"OTP":"This field should be string."})
        return data

    
class OTPVerificationSerializer(serializers.Serializer):
    Email = serializers.EmailField(max_length=150)
    OTP = serializers.CharField(max_length=100)
    
    def validate(self, data):
        if 'Email' not in data:
            raise serializers.ValidationError({"Email":"This field is required."})
        if 'OTP' not in data:
            raise serializers.ValidationError({"OTP":"This field is required."})
        if type(data['Email']) != str:
            raise serializers.ValidationError({"Email":"This field should be string."})
        if type(data['OTP']) != str:
            raise serializers.ValidationError({"OTP":"This field should be string."})
        return data
    