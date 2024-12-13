from rest_framework import generics
from tasks.models.taskListModel import TaskList
from tasks.models.userModel import User
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
            shared_with = request.data.get('shared_with', [])
            print("shared_with: ", shared_with)
            if not isinstance(shared_with, list):
                return Response({
                    "status": "error",
                    "message": "Invalid format for shared_with"
                },status=status.HTTP_400_BAD_REQUEST)
            shared_with_users = User.objects.filter(id__in=shared_with)
            print("shared_with_users: ", len(shared_with_users))
            if len(shared_with_users) != len(shared_with):
                return Response({
                    "status": "error",
                    "message": "Some users Id are not valid"
                },status=status.HTTP_400_BAD_REQUEST)
            serializer = TaskListSerializer(data=request.data)
            if serializer.is_valid():
                task_list = serializer.save()
                task_list.shared_with.set(shared_with_users)
                task_list.save()
                serializer = TaskListSerializer(task_list)
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
        
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            },status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_id = request.user.id
            task_list = TaskList.objects.filter(created_by=user_id)
            serializer = TaskListSerializer(task_list,many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {e}"
            },status=status.HTTP_400_BAD_REQUEST)

        
class TaskListDetailView(APIView):
    def get(self,request,pk):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            },status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_id = request.user.id
            user_obj = User.objects.get(id=user_id)
            if user_obj is None:
                return Response({
                    "status": "error",
                    "message": "User not found"
                },status=status.HTTP_404_NOT_FOUND)
            try:
                taskList = TaskList.objects.get(id=pk,created_by=user_obj)
            except TaskList.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Task list not found"
                },status=status.HTTP_404_NOT_FOUND)
            serializer = TaskListSerializer(taskList)
            return Response({
                "status": "success",
                "data": serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message":f"Error: {e}"
            },status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            },status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_id = request.user.id
            user_obj = User.objects.get(id=user_id)
            if user_obj is None:
                return Response({
                    "status": "error",
                    "message": "User not found"
                },status=status.HTTP_404_NOT_FOUND)
            try:
                taskList = TaskList.objects.get(id=pk,created_by=user_id)
            except TaskList.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Task list not found"
                },status=status.HTTP_404_NOT_FOUND)
            serializer = TaskListSerializer(taskList,data=request.data,partial=True)
            if serializer.is_valid():

                shared_with = request.data.get('shared_with',[])
                if not isinstance(shared_with,list):
                    return Response({
                        "status": "error",
                        "message": "Invalid format for shared_with"
                    },status=status.HTTP_400_BAD_REQUEST)
                
                shared_with_users = User.objects.filter(id__in=shared_with)
                if len(shared_with_users) != len(shared_with):
                    return Response({
                        "status": "error",
                        "message": "Some users Id are not valid"
                    },status=status.HTTP_400_BAD_REQUEST)   
            
                existing_shared_with = taskList.shared_with.all()
                taskList.shared_with.add(*shared_with_users)
                serializer.save()
                updated_serializer = TaskListSerializer(taskList)
                return Response({
                    "status": "success",
                    "data": updated_serializer.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "errors": serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {e}"
            },status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            },status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_id = request.user.id
            user_obj = User.objects.get(id=user_id)
            if user_obj is None:
                return Response({
                    "status": "error",
                    "message": "User not found"
                },status=status.HTTP_404_NOT_FOUND)
            taskList = TaskList.objects.get(id=pk,created_by=user_id)
            if taskList:
                taskList.delete()
                return Response({
                    "status": "success",
                    "message": "Task list deleted successfully"
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Task list not found2"
                },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {e}"
            },status=status.HTTP_400_BAD_REQUEST)