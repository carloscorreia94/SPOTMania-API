from rest_framework.response import Response
from rest_framework import status
#from abc import ABCMeta, abstractmethod

class OutResponse:
    #__metaclass__ = ABCMeta

    @classmethod
    def output(cls, return_status, http_status, data=None):
        args = {'status': return_status,'data': data}
        return Response(args, http_status)


    @classmethod
    def entry_already_exists(cls, data=None):
        return OutResponse.output('entry_already_exists', status.HTTP_400_BAD_REQUEST,data)

    @classmethod
    def invalid_arguments(cls, data=None):
        return OutResponse.output('invalid_arguments',status.HTTP_400_BAD_REQUEST,data)

    @classmethod
    def page_not_found(cls, data=None):
        return OutResponse.output('page_not_found',status.HTTP_404_NOT_FOUND,data)

    @classmethod
    def entry_not_existent(cls, data=None):
        return OutResponse.output('entry_not_existent', status.HTTP_400_BAD_REQUEST,data)

    @classmethod
    def content_created(cls, data=None):
        return OutResponse.output('content_created',status.HTTP_201_CREATED,data)

    @classmethod
    def action_performed(cls, data=None):
        return OutResponse.output('action_performed',status.HTTP_200_OK,data)

    @classmethod
    def empty_set(cls, data=None):
        return OutResponse.output('empty_set',status.HTTP_200_OK,data)

    @classmethod
    def content_set(cls, data=None):
        return OutResponse.output('content_set',status.HTTP_200_OK,data)

    @classmethod
    def content_deleted(cls):
        return OutResponse.output(None,status.HTTP_204_NO_CONTENT)