from django.urls import path
from direct.views import inbox, people_we_can_message, new_conversation, directs, send_direct, load_more, user_search, broadcast

urlpatterns = [
    path('', inbox, name='inbox'),
    path('start/', people_we_can_message, name='people-we-can-message'),
    path('broadcast/', broadcast, name='broadcast'),
    path('new/<username>', new_conversation, name='new-conversation'),
    path('directs/<username>', directs, name='directs'),
    path('send/', send_direct, name='send-direct'),
    path('loadmore/', load_more, name='loadmore'),
    path('search/', user_search, name='user-search'),

]