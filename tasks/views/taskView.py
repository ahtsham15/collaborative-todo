from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from tasks.models.taskModel import Task
from tasks.models.userModel import User
from tasks.serializers import TaskSerializer
from tasks.serializers import TaskDoSerializer

class TaskDoView(APIView):
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_id = request.user.id
            try:
                user = User.objects.get(id=user_id)
                print("user: ",user)
            except User.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data.copy()
            if 'is_completed' not in data:
                data['is_completed'] = False
            
            print("data: ", data)
            serializer = TaskDoSerializer(data=data)
            print("serializer initial data: ", serializer.initial_data)
            if serializer.is_valid():
                task = serializer.save()
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "error",
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)