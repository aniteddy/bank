from typing import Any

from django.http import JsonResponse


def generic_404_response(data=None) -> JsonResponse:
    from rest_framework import status
    return JsonResponse({"success": False, "data": __convert_response_data_to_dict_if_required__(data)}, status=status.HTTP_404_NOT_FOUND)


def generic_400_response(data=None, client_message: str = None) -> JsonResponse:
    from rest_framework import status
    return JsonResponse({"success": False, "data": __convert_response_data_to_dict_if_required__(data),
                        "message": client_message}, status=status.HTTP_400_BAD_REQUEST)


def generic_successful_response(data=None) -> JsonResponse:
    from rest_framework import status
    return JsonResponse({"success": True, "data": __convert_response_data_to_dict_if_required__(data)}, status=status.HTTP_200_OK)


def __convert_response_data_to_dict_if_required__(data: Any) -> Any:
    if data is None:
        result = {}
    elif isinstance(data, str):
        result = {"message": data}
    elif isinstance(data, bool):
        result = {"result": data}
    elif isinstance(data, int):
        result = {"result": data}
    else:
        result = data
    return result
