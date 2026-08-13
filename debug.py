import grpc_requests
from grpc_requests import Client
from contracts.services.users import rpc_get_user_pb2 as get_user
import contracts.services.users as user_service

# Подключаемся
client = Client.get_by_endpoint("localhost:9003")

print("Доступные сервисы:")
for service in client.service_names:
    print(f"  - {service}")

# Указываем сервис
service_name = "contracts.services.gateway.users.UsersGatewayService"

# Получаем все методы
methods_meta = client.get_methods_meta(service_name)

print(f"=== Методы для {service_name} ===")
for method_name in methods_meta.keys():
    print(f"  {method_name}")

# Выбираем первый метод из списка (если не знаем точное имя)
# Или замените на конкретное имя, которое увидите в выводе
first_method = list(methods_meta.keys())[0]
print(f"\nПробуем вызвать метод: {first_method}")

# Отправляем запрос
request_data = {"id": "31df9dce-bf3a-48c1-8b05-6b83e09b6cc9"}

try:
    response = client.request(service_name, first_method, request_data)
    print(f"\n=== Ответ ===")
    print(response)
except Exception as e:
    print(f"Ошибка: {e}")
