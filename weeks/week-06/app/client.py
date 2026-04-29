import requests

PROJECT_CODE = "profiles-s19"

def build_payload(query: str, variables: dict = None) -> dict:
    return {"query": query, "variables": variables or {}}

url = "http://localhost:8205/graphql"

mutation_query = """
mutation Create($name: String!, $phone: String!) {
  createProfile(name: $name, phone: $phone) {
    id
    name
  }
}
"""
mutation_vars = {"name": "USSSSSSSSSSSSSS", "phone": "123123"}

try:
    print("--- Создание профиля ---")
    resp_m = requests.post(url, json=build_payload(mutation_query, mutation_vars))
    print(resp_m.json())
except Exception as e:
    print("Ошибка при создании:", e)


query_all = """
query {
  profiles {
    id
    name
    phone
  }
}
"""

try:
    print("\n--- Получение всех профилей ---")
    resp_q = requests.post(url, json=build_payload(query_all))
    data = resp_q.json()
    
    if "errors" in data:
        print("Ошибки:", data["errors"])
    else:
        print("Данные:", data["data"])
except Exception as e:
    print("Ошибка при получении:", e)
