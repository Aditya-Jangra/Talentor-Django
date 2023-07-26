from django.urls import path
from .api.auth import login,change_password,view_profile,ManagePeopleView
from .api.linkedinprofile import get_linkedin_profiles
from app.api.recruiterprofile import get_recruiter_profiles,update_recruiter_profiles,post_recruiter_profile,update_recruitment_project,post_recruitment_project_profile,delete_recruiter_profile,get_recruitment_project_by_profile,post_recruitment_project,get_recruitment_project

from .api.pdfconverter.pdfconverter import PDFConverterAPI
# from .api.pdfconverter.pdfconverter import DOCConverterAPI


urlpatterns = [
    path('login/',login.LoginView.as_view()),
    path('change-password/',change_password.ChangePasswordView.as_view()),
    path('view-profile/',view_profile.ProfileView.as_view()),
    path('manage-people/', ManagePeopleView.ManagePeopleView.as_view()),
    path('manage-linkedin/', get_linkedin_profiles.ManageLinkedInProfileView.as_view()),
    
    # Using For Storing Recruiter Project Profile Information (RecruiterProjectLinkedinProfile) From Admin Panel
    path('manage-recruiter/', get_recruiter_profiles.ManageRecruiterProfileView.as_view()), 
    path('manage-recruiter/delete', delete_recruiter_profile.DeleteRecruiterProfileView.as_view()), 
    path('recruiter-profile/', update_recruiter_profiles.ManageRecruiterProfileView.as_view()),
    path('manage-recruiter-new/', post_recruiter_profile.ManageRecruiterProfileView2.as_view()),

    # Extension API 
    path('recruitment-project/',post_recruitment_project.PostRecruitmentProjectView.as_view()),
    path('get-recruitment-projects/',get_recruitment_project.RecruitmentProjectsViews.as_view()),
    path('get-recruitment-projects/<str:profile_slug>/',get_recruitment_project_by_profile.GetRecruitmentProjectsByProfile.as_view()),
    path('recruitment-project-profile/',post_recruitment_project_profile.RecruitmentProjectProfileView.as_view()),
    path('update-recruitment-project/',update_recruitment_project.RecruitmentProjectSelectionView.as_view()),
    path('pdf-converter/', PDFConverterAPI ),
    # path('doc-converter/', DOCConverterAPI)
]


