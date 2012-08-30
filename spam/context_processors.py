from google.appengine.api import users
from models import UserSetting

def user(request):
    user = users.get_current_user()
    
    if user:
        usetting = UserSetting.gql('WHERE userid = :1', user.user_id())
        if usetting.count() == 0:
            usetting = UserSetting(userid=user.user_id(), is_contrib=False)
            usetting.put()
        userurl = users.create_logout_url(request.get_full_path())
    else:
        userurl = users.create_login_url(request.get_full_path())
        
    return {
        "user": user,
        "userurl": userurl
    }
