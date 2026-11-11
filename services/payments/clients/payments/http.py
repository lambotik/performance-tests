# Импорты стандартных и сторонних библиотек
import uuid
from datetime import date

from httpx import Response  # HTTP-ответ от клиента

# Импорт конфигурации и утилит
from config import settings  # глобальные настройки проекта
from libs.http.client.base import HTTPClient  # базовый HTTP-клиент
from libs.http.client.handlers import handle_http_error, HTTPClientError  # декоратор и базовая ошибка
from libs.logger import get_logger  # получение инстанса логгера
from libs.routes import APIRoutes  # маршруты API
# Импорт схем данных для работы с платежами
from services.payments.apps.payments.schema.payments import (
    PaymentSystem,
    PaymentStatus,
    PaymentSchema,
    RefundPaymentRequestSchema,
    RefundPaymentResponseSchema,
    CapturePaymentRequestSchema,
    CapturePaymentResponseSchema,
    AuthorizePaymentRequestSchema,
    AuthorizePaymentResponseSchema
)


# ============================
# Хелпер-функция для фейкового платежа
# ============================
def build_authorized_payment() -> PaymentSchema:
    """
    Создаёт фейковый объект платежа со статусом "AUTHORIZED".

    Используется при отключённой платёжной системе.
    """
    return PaymentSchema(
        id=uuid.uuid4(),
        status=PaymentStatus.AUTHORIZED,
        system=PaymentSystem.MASTERCARD,
        message="success"
    )


# ============================
# Кастомное исключение для HTTP-клиента
# ============================
class PaymentsHTTPClientError(HTTPClientError):
    """
    Ошибка, специфичная для клиента PaymentsHTTPClient.
    Используется в декораторе @handle_http_error.
    """
    pass


# ============================
# HTTP-клиент для сервиса платежей
# ============================
class PaymentsHTTPClient(HTTPClient):
    """
    Клиент для общения с сервисом платежей через HTTP.
    Включает методы для операций: авторизация, списание и возврат средств.
    """

    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def refund_payment_api(self, request: RefundPaymentRequestSchema) -> Response:
        """
        Низкоуровневый метод отправки POST-запроса на возврат платежа.

        Оборачивается в декоратор, который отлавливает и логирует ошибки.
        """
        return await self.post(
            f'{APIRoutes.PAYMENTS}/refund-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def capture_payment_api(self, request: CapturePaymentRequestSchema) -> Response:
        """
        Низкоуровневый метод для захвата платежа.
        """
        return await self.post(
            f'{APIRoutes.PAYMENTS}/capture-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def authorize_payment_api(self, request: AuthorizePaymentRequestSchema) -> Response:
        """
        Низкоуровневый метод для авторизации платежа.
        """
        return await self.post(
            f'{APIRoutes.PAYMENTS}/authorize-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    async def refund_payment(self, amount: float, payment_id: uuid.UUID) -> RefundPaymentResponseSchema:
        """
        Возврат средств по платежу.

        Если платёжная система отключена (например, на стенде), возвращается фейковый ответ.
        """
        if not settings.payments_system_enabled:
            return RefundPaymentResponseSchema(payment=build_authorized_payment())

        # Создаём тело запроса и отправляем
        request = RefundPaymentRequestSchema(
            amount=amount,
            system=PaymentSystem.MASTERCARD,
            payment_id=payment_id
        )
        response = await self.refund_payment_api(request)

        # Валидируем ответ в Pydantic-модель
        return RefundPaymentResponseSchema.model_validate_json(response.text)

    async def capture_payment(self, payment_id: uuid.UUID) -> CapturePaymentResponseSchema:
        """
        Захват (списание) ранее авторизованного платежа.
        """
        if not settings.payments_system_enabled:
            return CapturePaymentResponseSchema(payment=build_authorized_payment())

        request = CapturePaymentRequestSchema(
            system=PaymentSystem.MASTERCARD,
            payment_id=payment_id
        )
        response = await self.capture_payment_api(request)
        return CapturePaymentResponseSchema.model_validate_json(response.text)

    async def authorize_payment(
            self,
            cvv: str,
            amount: float,
            expiry_date: date,
            card_number: str,
            card_holder: str,
    ) -> AuthorizePaymentResponseSchema:
        """
        Авторизация платежа по банковской карте.

        :param cvv: CVV-код карты
        :param amount: Сумма платежа
        :param expiry_date: Срок действия карты
        :param card_number: Номер карты
        :param card_holder: Владелец карты
        :return: Ответ с результатом авторизации
        """
        if not settings.payments_system_enabled:
            return AuthorizePaymentResponseSchema(payment=build_authorized_payment())

        request = AuthorizePaymentRequestSchema(
            cvv=cvv,
            amount=amount,
            system=PaymentSystem.MASTERCARD,
            expiry_date=expiry_date,
            card_number=card_number,
            card_holder=card_holder
        )
        response = await self.authorize_payment_api(request)
        return AuthorizePaymentResponseSchema.model_validate_json(response.text)


# ============================
# Фабрика для создания клиента
# ============================
def get_payments_http_client() -> PaymentsHTTPClient:
    """
    Фабричная функция для получения клиента с конфигурацией и логгером.

    :return: Инстанс PaymentsHTTPClient
    """
    logger = get_logger("PAYMENTS_SERVICE_HTTP_CLIENT")
    return PaymentsHTTPClient(config=settings.payments_http_client, logger=logger)
