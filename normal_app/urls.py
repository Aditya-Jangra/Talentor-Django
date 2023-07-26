from django.urls import path
from .api.recruitmentproject import get_recruitment_project_by_profile,update_recruitment_project,post_recruitment_project_profile

urlpatterns = [
    path('get-recruitment-projects/<str:profile_slug>/',get_recruitment_project_by_profile.GetRecruitmentProjectsByProfile.as_view()),
    path('recruitment-project-profile/',post_recruitment_project_profile.RecruitmentProjectProfileView.as_view()),
    path('update-recruitment-project/',update_recruitment_project.RecruitmentProjectSelectionView.as_view()),
]

