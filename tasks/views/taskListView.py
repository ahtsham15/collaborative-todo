from rest_framework import generics
from tasks.models.taskListModel import TaskList
from tasks.models.userModel import User
from tasks.models.taskModel import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from tasks.serializers import TaskListSerializer
from tasks.utils.constFunction import send_task_update_message

class TaskListView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "User not found"
                }, status=status.HTTP_401_UNAUTHORIZED)

            request.data['created_by'] = user.id
            shared_with = request.data.get('shared_with', [])

            if not isinstance(shared_with, list):
                return Response({
                    "status": "error", 
                    "message": "Invalid format for shared_with"
                }, status=status.HTTP_400_BAD_REQUEST)

            shared_with_users = User.objects.filter(id__in=shared_with)
            if len(shared_with_users) != len(shared_with):
                return Response({
                    "status": "error",
                    "message": "Some users Id are not valid"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TaskListSerializer(data=request.data)
            if serializer.is_valid():
                task_list = serializer.save()
                task_list.shared_with.set(shared_with_users)
                task_list.save()
                room_name = "test_consumer_group"
                send_task_update_message(room_name, {"message": "Task list created", "data": serializer.data})
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
                room_name = "test_consumer_group"
                send_task_update_message(room_name, {"message": "Task list updated", "data": serializer.data})
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
        
    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "message": "Access token not provided or invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)
    
        try:
            user_id = request.user.id
            user_obj = get_object_or_404(User, id=user_id)
            taskList = TaskList.objects.get(id=pk, created_by=user_id)
        
            if taskList:
                # Ensure that all related tasks are deleted first
                Task.objects.filter(list=taskList).delete()

                # Delete the task list
                taskList.delete()

                # Optionally, send a WebSocket update if needed (this part is commented out in your code)
                # channel_layer = get_channel_layer()
                # room_name = "task_list_{}".format(pk)
                # async_to_sync(channel_layer.group_send)(
                #     room_name,
                #     {
                #         "type": "task_update",
                #         "message": "Task list deleted successfully"
                #     }
                # )

                return Response({
                    "status": "success",
                    "message": "Task list deleted successfully"
                }, status=status.HTTP_200_OK)

        except TaskList.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Task list not found"
            }, status=status.HTTP_404_NOT_FOUND)
    
        except IntegrityError:
            # Handle the case where deleting task list fails due to foreign key constraints
            return Response({
                "status": "error",
                "message": "Cannot delete task list because there are related tasks"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {e}"
            }, status=status.HTTP_400_BAD_REQUEST)