from django.core.cache import cache
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        database = "up"
        redis = "up"

        try:
            connection.ensure_connection()
        except Exception:
            database = "down"

        try:
            cache.set("health", "ok", timeout=5)
            cache.get("health")
        except Exception:
            redis = "down"

        return Response(
            {
                "status": "healthy" if database == "up" and redis == "up" else "unhealthy",
                "database": database,
                "redis": redis,
            }
        )