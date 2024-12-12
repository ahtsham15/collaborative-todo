from rest_framework import generics
from tasks.models.taskListModel import TaskList
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.serializers import TaskListSerializer

class TaskListView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_id = request.user.id
            print("user_id: ", user_id)
            print("request data: ", request.data)
            request.data['created_by'] = user_id
            print("request data: ", request.data)
            
            serializer = TaskListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "error", 
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {e}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
class TaskListDetailView(APIView):
    def get(self,request,id):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            },status=status.HTTP_401_UNAUTHORIZED)
        try:
            pass
        except Exception as e:
            return Response({
                "status": "error",
                "message":f"Error: {e}"
            },status=status.HTTP_400_BAD_REQUEST)