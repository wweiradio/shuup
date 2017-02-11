# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2017, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf import settings
from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response


class PermissionHelperMixin(object):
    """
    Mixin to return a helper text to admin users in permission configuration.
    """
    @classmethod
    def get_help_text(cls):
        raise NotImplementedError()


class ProtectedModelViewSetMixin(object):
    """
    Mixin to catch ProtectedError exceptions and return a reasonable response error to the user.
    """

    def destroy(self, request, *args, **kwargs):
        try:
            return super(ProtectedModelViewSetMixin, self).destroy(request, *args, **kwargs)
        except ProtectedError as exc:
            ref_obj = exc.protected_objects[0].__class__.__name__
            msg = "This object can not be deleted because it is referenced by {}".format(ref_obj)
            return Response(data={"error": msg}, status=status.HTTP_400_BAD_REQUEST)


def apply_logging(viewset_class, methods="__all__"):
    if "rest_framework_tracking" in settings.INSTALLED_APPS:
        from rest_framework_tracking.mixins import LoggingMixin
        return type(viewset_class.__name__, (LoggingMixin, viewset_class), {"logging_methods": methods})
    return viewset_class
