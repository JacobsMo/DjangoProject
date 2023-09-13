import logging
from core.views import BaseAPIView
from django.http import HttpRequest
from typing import Any
from rest_framework.response import Response
from .tasks import start_mailing
from .mailing_service import MailingService
from .serializers import MailingSerializer, MailingIdSerializer, MailingUpdateMethodSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_226_IM_USED


logger = logging.getLogger("debug")


class MailingAPIView(BaseAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request: HttpRequest, mailing_id: int, *args: Any, **kwargs: Any) -> Response:
        serializer = MailingIdSerializer(data={"mailing_id": mailing_id})

        if serializer.is_valid():
            mailing_data = MailingService.get_mailing_by_id(serializer.validated_data.get("mailing_id"))

            if mailing_data is not None:
                return Response({"success": True, "mailing_data": mailing_data})
            else:
                return Response({"success": False, "detail": "Mailing not found. Your mailing can be finished yet"}, status=HTTP_404_NOT_FOUND)

        else:
            return Response({"success": False, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, mailing_id: int, *args: Any, **kwargs: Any) -> Response:
        serializer = MailingIdSerializer(data={"mailing_id": mailing_id})

        if serializer.is_valid():
            mailing_id = serializer.validated_data.get("mailing_id")

            mailing_data = MailingService.get_mailing_by_id(mailing_id=mailing_id)
            if mailing_data is not None:
                if MailingService.delete_mailing_by_id(mailing_id=mailing_id):
                    return Response({"success": True, "deleted_mailing_data": mailing_data})

                else:
                    return Response({"success": False, "detail": "Mailing is running, try later"}, status=HTTP_226_IM_USED)

            else:
                return Response({"success": False, "detail": "Mailing not found. Your mailing can be finished yet"}, status=HTTP_404_NOT_FOUND)

        else:
            return Response({"success": False, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, mailing_id: int, *args: Any, **kwargs: Any) -> Response:
        data = {
            "mailing_id": mailing_id,
            "data": request.data
        }

        serializer = MailingUpdateMethodSerializer(data=data)

        if serializer.is_valid():
            mailing_id = serializer.validated_data.get("mailing_id")

            if MailingService.get_mailing_by_id(mailing_id=mailing_id) is not None:

                if MailingService.update_mailing_by_id(
                    mailing_id=mailing_id, data=serializer.validated_data.get("data")
                ):
                    return Response({"success": True})

                else:
                    return Response({"success": False, "detail": "Mailing is running, try later"}, status=HTTP_226_IM_USED)

            else:
                return Response({"success": False, "detail": "Mailing not found. Your mailing can be finished yet"}, status=HTTP_404_NOT_FOUND)

        else:
            return Response({"success": False, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class MailingCreationAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = MailingSerializer(data=request.POST)

        if serializer.is_valid():
            task_id = MailingService.generate_task_id()

            start_time = serializer.validated_data.get("start_time")
            subject = serializer.validated_data.get("subject")
            message = serializer.validated_data.get("message")
            filter = serializer.validated_data.get("filter", None)
            template_name = serializer.validated_data.get("template_name", None)

            MailingService.add_mailing(
                mailing_id=task_id,
                start_time=start_time,
                subject=subject,
                message=message,
                filter=filter,
            )

            logger.debug(f"New task added: task_id={task_id}; start_time={start_time}")

            start_mailing.apply_async((task_id, subject, message, filter, template_name), eta=start_time, task_id=task_id)
            
            return Response({"success": True, "detail": {"task_id": task_id, "start_time": start_time}})
            
        else:
            return Response({"success": False, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)
    