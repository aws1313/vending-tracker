from rest_framework.views import APIView, Response, status
from rest_framework_api_key.permissions import HasAPIKey

class SoldView(APIView):
    permission_classes = (HasAPIKey, )

    def patch(self, request):
        print(request.data)
        return Response(status=status.HTTP_200_OK)


