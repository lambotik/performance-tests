from locust import HttpUser, SequentialTaskSet, task, between


# Последовательный сценарий: оформление заказа
class CheckoutFlow(SequentialTaskSet):
    @task
    def open_cart(self):
        self.client.get("/cart")

    @task
    def checkout(self):
        self.client.post("/checkout")

    @task
    def confirm(self):
        self.client.get("/order/confirm")


# Пользователь, выполняющий строго последовательный сценарий
class CheckoutUser(HttpUser):
    host = "https://api.example.com"
    tasks = [CheckoutFlow]
    wait_time = between(2, 4)

