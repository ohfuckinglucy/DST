import time
import requests
import grpc
import service_pb2
import service_pb2_grpc

ITERATIONS = 1000

def run_rest_bench():
    print("REST benchmark...")
    start = time.time()
    for _ in range(ITERATIONS):
        requests.get("http://localhost:8000/profiles/1") 
    end = time.time()
    return end - start

def run_grpc_bench():
    print("gRPC benchmark...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.UsersServiceStub(channel)
        start = time.time()
        for _ in range(ITERATIONS):
            stub.GetUser(service_pb2.UserRequest(id="1"))
        end = time.time()
    return end - start

if __name__ == "__main__":
    t_rest = run_rest_bench()
    t_grpc = run_grpc_bench()
    print(f"REST: {t_rest:.4f}s | gRPC: {t_grpc:.4f}s")
    print(f"gRPC быстрее в {t_rest/t_grpc:.1f} раз")
