# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.db import transaction  # Import atomic transaction
from Auth.models import User,OTP
from Auth.Seializer import SignupSerializer,OTPVerificationSerializer
from Auth.crud import generateOtp, sendEmail, save_otp_in_database, user_otp_expiration_timer

class Signup(viewsets.ModelViewSet):
    """
    A viewset for creating a new user and sending an OTP for verification.
    """
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    def create(self, request, *args, **kwargs):
        try:
            # Extract the email from the request data
            email = request.data.get('email')

            # Check if the user with the given email already exists
            user = User.objects.filter(email=email).first()
            if user:
                return JsonResponse(data={'details': 'User already exists', 'statuscode': 400}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the request data using the serializer
            serializer_response = SignupSerializer(data=request.data)
            if serializer_response.is_valid():
                # Use atomic transaction to ensure data integrity
                with transaction.atomic():
                    # Extract validated data from the serializer
                    email = serializer_response.validated_data['email']
                    password = serializer_response.validated_data['password']
                    username = serializer_response.validated_data['username']
                    usertype = serializer_response.validated_data['usertype']

                    # Create a new user
                    user = User.objects.create(username=username, email=email, password=password, user_type=usertype)
                    user.save()
                    user.refresh_from_db()

                    # Generate OTP
                    otp = generateOtp()

                    # Email body with OTP
                    body = f"""
                    <html>
                        <body>
                            <h1>SignUp OTP</h1>
                            <p>Your OTP is: <strong>{otp}</strong></p>
                            <p style="color: red;"><strong>Notice:</strong> Do not share this OTP with anyone.</p>
                        </body>
                    </html>"""

                    # Save OTP to the database
                    response = save_otp_in_database(email=email, otp=otp)
                    if not response:
                        # Rollback the transaction if OTP saving fails
                        raise Exception("Error occurred while saving the user OTP")

                    # Send OTP via email
                    email_response = sendEmail(recipient=email, subject="User SignUp OTP", body=body)
                    if email_response:
                        # Start the OTP expiration timer
                        user_otp_expiration_timer(email=email)
                        return JsonResponse(data={"details": "OTP has been sent to your email"}, status=status.HTTP_201_CREATED)
                    else:
                        # Rollback the transaction if email sending fails
                        raise Exception("Error occurred while sending the OTP email")
            else:
                return JsonResponse(data={"details": "Error occurred while validating the data", "errors": serializer_response.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return the error response in case of an exception
            return JsonResponse(data={"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOtp(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            serializer = OTPVerificationSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data['Email']
                otp = serializer.validated_data['OTP']
                checkOTP = OTP.objects.filter(Email=email, OTP=otp)
                if checkOTP.exists():
                    checkOTP.delete()
                    return Response({"details": "OTP Verified"}, status=status.HTTP_200_OK)
                else:
                    return Response({"details": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"details": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    