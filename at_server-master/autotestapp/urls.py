from django.urls import path, include
from . import views_report
from . import parse, views_runner
from . import views_chart
from . import views_project
from . import views_factor
urlpatterns = [
    path('project/<int:id>/report/status/', views_report.AutoTestReportObject.as_view()),
    path('report/save/', views_report.AutoTestReportSaveObject.as_view()),
    path('report/change/<int:id>/', views_report.AutoTestReportModifyParamObject.as_view()),
    path('project/report/', views_report.AutoTestReportListObject.as_view()),
    path('project/TJ/<int:id>', views_report.AutoTestReportTJObject.as_view()),
    path('project/<int:project_id>/parsesuite/', parse.parseSuite.as_view()),
    path('rfrunner/<int:project_id>/', views_runner.Rfrunner.as_view()),
    path('getsuitename/', parse.getSuiteName.as_view()),
    path('getcasename/', parse.getCaseName.as_view()),
    path('<int:id>/overview/', views_chart.ChatrsInfoObject.as_view()),
    path('project/', views_project.ProjectObject.as_view()),
    path('project/initFactorCase/',views_factor.FactorCaseSaveObject.as_view()),
    path('project/factorList/', views_factor.FactorCaseListObject.as_view()),
    path('factor/runner/', views_factor.FactorCaseRunObject.as_view()),
    path('project/factorTypeList/', views_factor.FactorCaseTypeListObject.as_view()),
]
