from django.shortcuts import render
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from spots.models import Spot
from .models import Favorites, FollowerRelation
from rollfeverapi.common import validation_utils, validation_geo, output_messages
from rollfeverapi.common import validation_messages
from rollfeverapi.common.output_messages import OutResponse
from rest_framework.response import Response
from .models import Favorites
from rest_framework import status
from rest_auth.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rollfeverapi.common.views import GenericView


class Followers(GenericView):

    def get(self, request, username=None, following=False):

        try:
            inUser = request.user if username is None else MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        if following:
            ret = FollowerRelation.get_following(inUser)
        else:
            ret = FollowerRelation.get_follows(inUser)

        if len(ret) == 0:
            return OutResponse.empty_set()

        return OutResponse.content_set(ret)


class Following(GenericView):

    def get(self, request, username=None):
        return Followers.get(Followers.as_view(),request,username,True)

class FollowManagement(GenericView):

    def post(self, request, username):

        try:
            inUser = request.user
            otherUser = MyUser.objects.get(username=username)

            if inUser.username == username:
                return OutResponse.invalid_arguments()

        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        same_follow_relation = FollowerRelation.objects.filter(user_created=inUser, user_following=otherUser)
        if same_follow_relation.exists():
            return OutResponse.entry_already_exists()

        _status = FollowerRelation.do_follow(inUser,otherUser)

        return OutResponse.content_created(_status)

    def delete(self, request, username):

        try:
            inUser = request.user
            otherUser = MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        _status = FollowerRelation.do_unfollow(inUser,otherUser)
        if not _status:
            return OutResponse.entry_not_existent()

        return OutResponse.action_performed(_status)


# Create your views here.
class UserFavorites(GenericView):

    def get(self, request,spot = None, username = None):
        if spot is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user if username is None else MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        ret = Favorites.get_spot(inUser)

        if len(ret) == 0:
            return OutResponse.empty_set()

        return OutResponse.content_set(ret)

    def delete(self, request,spot, username = None):
        if username is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user
            inSpot = Spot.objects.get(id=spot)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        _status = Favorites.delete_favorite(inUser,inSpot)
        if not _status:
            return OutResponse.entry_not_existent()

        return OutResponse.content_deleted()


    def post(self, request,spot, username =None):
        if username is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user
            inSpot = Spot.objects.get(id=spot)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        create = Favorites.create_favorite(inUser,inSpot)
        if not create:
            return OutResponse.entry_already_exists()

        return OutResponse.content_created(create)