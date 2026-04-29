import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

class UsersService(service_pb2_grpc.UsersServiceServicer):
    def GetUser(self, request, context):
        print(f"Запрос юзера: {request.id}")
        return service_pb2.UserResponse(id=request.id, name="Ivan", email="s19@edu.ru")

    def ListUsers(self, request, context):
        print("Стриминг списка юзеров...")
        users = [
            {"id": "1", "name": "Admin", "email": "admin@test.ru"},
            {"id": "2", "name": "User1", "email": "u1@test.ru"},
        ]
        for u in users:
            yield service_pb2.UserResponse(id=u["id"], name=u["name"], email=u["email"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    service_pb2_grpc.add_UsersServiceServicer_to_server(UsersService(), server)
    
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
