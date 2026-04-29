import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

class CommentsService(service_pb2_grpc.CommentsServiceServicer):
    def GetComment(self, request, context):
        print(f"Пришел запрос за комментарием: {request.id}")

        return service_pb2.CommentResponse(
            id=request.id,
            text="ASASASASAS",
            author="s19"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CommentsServiceServicer_to_server(CommentsService(), server)
    
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
