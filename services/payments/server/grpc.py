import asyncio
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from contracts.services.payments import payments_service_pb2
from contracts.services.payments import payments_service_pb2_grpc
from libs.grpc.server.interceptors.logger_interceptor import GRPCLoggerInterceptor
from libs.grpc.server.interceptors.exception_interceptor import GRPCExceptionInterceptor
from libs.logger import get_logger
from services.payments.apps.payments.api.grpc import PaymentsMockService


async def serve():
    logger = get_logger("PAYMENTS_MOCK_SERVICE_GRPC_SERVER")
    logger.info(f'Starting server at 0.0.0.0:9007')

    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=100),
        interceptors=[
            GRPCLoggerInterceptor(logger),
            GRPCExceptionInterceptor(logger)
        ]
    )
    server.add_insecure_port("0.0.0.0:9007")

    payments_service_pb2_grpc.add_PaymentsServiceServicer_to_server(PaymentsMockService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            payments_service_pb2.DESCRIPTOR.services_by_name['PaymentsService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
