from django.urls import path, include
from . import view_desired
from . import version_overview
from . import view_designstage
from . import view_analyze
from . import view_myinfos
from . import view_project
from . import views_dev


urlpatterns = [
    path('storyplans/zentao/sync/', view_desired.SyncDesired.as_view()),
    path('storyplans/', view_desired.GetStory.as_view()),
    path('storyplans/<int:id>/storys/', view_desired.GetPlanStory.as_view()),
    path('storyplans/<int:id>/', view_desired.EditStory.as_view()),
    path('version/history/<int:id>/', version_overview.GetVersionChangeHistory.as_view()),
    path('versions/<int:id>/', version_overview.GetVersion.as_view()),
    path('versions/', version_overview.Versions.as_view()),
    path('version/updatestage/<int:id>/', version_overview.UpdateVersionStage.as_view()),
    path('versions/<int:id>/designs/', view_designstage.GetVersionDesignsStageFiles.as_view()),#设计阶段获取文档列表
    path('versions/<int:id>/schedules/', view_designstage.GetVersionScheduleFiles.as_view()),#开发测试计划-排期文档列表
    path('versions/<int:id>/testcases/', view_designstage.GetVersionTestcaseFiles.as_view()),#测试用例文档列表
    path('files/upload/', view_designstage.FileUploadObject.as_view()),# 设计阶段上传文档
    path('files/<int:id>/download/', view_designstage.FileDownloadObject.as_view()),# 设计阶段下载文档
    path('files/<int:id>/delete/', view_designstage.FileDeleteObject.as_view()),  # 设计阶段删除文档
    path('versions/designcontent', view_designstage.VersionAddStageContentObject.as_view()),# 设计阶段增加内容
    path('versions/designcontent/<int:id>/', view_designstage.VersionHandleStageContentObject.as_view()), # 设计阶段删改内容
    path('analyze/demand', view_analyze.Demand.as_view()),
    path('analyze/version', view_analyze.Versions.as_view()),
    path('analyze/standard', view_analyze.Standard.as_view()),
    path('analyze/demandYear', view_analyze.DemandYear.as_view()),
    path('myinfos/query/', view_myinfos.MyInfosQuery.as_view()),#我的信息查询
    path('projects', view_project.Projects.as_view()),
    path('start/sonar/', views_dev.StartSonar.as_view()),
    path('start/server/', views_dev.StartServer.as_view()),
    path('sonarcode/', views_dev.SonarCode.as_view()),
    path('createserver/', views_dev.CreateServerQL.as_view()),
    path('develop/<int:version_id>', views_dev.DevelopInfo.as_view()),
    path('codereview/', views_dev.CodeReview.as_view()),
    path('delserver/', views_dev.DelServer.as_view()),
]

