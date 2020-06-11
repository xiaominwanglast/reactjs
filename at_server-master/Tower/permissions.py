from rest_framework import permissions
import userapp,autotestapp,projectapp
import wxwork


class CustomerPermission(permissions.BasePermission):
    """
    自定义权限只允许对象的所有者编辑它。
    """

    def has_object_permission(self, request, view, obj):
        return True
        # 读取权限允许任何请求，
        # 所以我们总是允许GET，HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只有该snippet的所有者才允许写权限。
        return False
        return obj.owner == request.user

    def has_permission(self, request, view):

        if request.method in ("HEAD", "OPTIONS"):
            return True

        if isinstance(view, userapp.views.UserAuth) or isinstance(view, wxwork.views.WXMessageObject):
            if request.method in ('POST'):
                return True
        if isinstance(view, userapp.views.UserCross):
            if request.method in ('GET'):
                return True
        if request.session.get('user'):
            return True
        if isinstance(view, autotestapp.parse.parseSuite) or isinstance(view, autotestapp.views_report.AutoTestReportSaveObject) :
            if request.method in ('POST'):
                return True
        if isinstance(view, projectapp.view_desired.SyncDesired):
            if request.method in ('POST'):
                return True
        if isinstance(view, projectapp.views_dev.SonarCode):
            if request.method in ('POST'):
                return True
        if isinstance(view, autotestapp.views_report.AutoTestReportModifyParamObject):
            if request.method in ('PUT'):
                return True
        else:
            return False
