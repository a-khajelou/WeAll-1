from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
import main
import friends
from django.utils import timezone



@dajaxice_register
def new_post(request, newtext):
    try:
        p = User.objects.get(username = request.session['username'])
    except:
        return simplejson.dumps({'message':'user problem, logout & login to fix the problem'})
    try:
        post = main.models.Post.objects.create(user = p, date = timezone.now(), text = newtext)
        post.save()
        return simplejson.dumps({'message':'you posted your status successfully!'})
    except:
        return simplejson.dumps({'message':'post saving problem, try again...'})
    

    
@dajaxice_register
def update(request):
    try:
        p = User.objects.get(username = request.session['username'])
    except:
        return simplejson.dumps({'data':'user problem, logout & login to fix the problem'})
    li = friends.models.Friendship.objects.friends_for_user(p)
    friendslist = list()
    for i in li:
        friendslist.append(i['friend'])
    posts = list(main.models.Post.objects.all())
    posts = posts[-30:]
    html = ''
    now = timezone.now()
    time = ("%s" %now)
    time = time[:16]
    id = 0
    for i in reversed(posts) :
        if id == 20:
            break
        if ((i.user in friendslist) or (i.user == p)) :
            id += 1
            post_time = str(i.date)
            post_time = post_time[:16]
            html += '<fieldset style="background-color:#e5e4e2; border-radius:7px; width:90%; margin-left:3%; border:none;"><legend style="font-size:20px; text-align:left; margin-left:10px;">' + i.user.first_name + ' ' + i.user.last_name + '</legend><p class="info"><small color="Silver" style="text-align:left;">'+ post_time +'</small></p><br><p class="info">' + i.text + '</p><br></fieldset><br>'#'<p> #'+ str(id) +' <br>' + i.user.first_name + ' ' + i.user.last_name + ' updated status '  + ' : ' + "<br>" + i.text + "</P>" + time + " <hr width='33%'>"
    return simplejson.dumps({'data':html})
        
@dajaxice_register
def search_poeple(request, name):
    try:
        namelist = name.split()
        fname    = namelist[0]
        lname    = namelist[1]
        p = User.objects.get(first_name = fname, last_name = lname)
    except:
        return simplejson.dumps({'html':'search result did not match, try again...'})
    try:
        html = ''
        link = '  <a href="javascript:Dajaxice.main.add_friend(addfriend, {' + "'username' : " + "'" + str(p.username)+ "'" + '});"' + '>Add friend</a>'
        print link
        html += p.first_name + ' ' + p.last_name + link
        
        return simplejson.dumps({'html': html})
    except:
        return simplejson.dumps({'html':'html error'})

@dajaxice_register
def add_friend(request, username):
    try:
        fuser = User.objects.get(username = request.session['username'])
        tuser = User.objects.get(username = username)
    except:
        return simplejson.dumps({'html': "user finding error!"})
    
    try:
        print 1
        if not friends.models.Friendship.objects.are_friends(fuser, tuser):
            friendship = friends.models.Friendship(to_user = tuser, from_user = fuser)
            friendship.save()
            return simplejson.dumps({'html': "you're now friends "})
            # with %s %s" %(tuser.first_name, tuser.last_name)})
        else:
            return simplejson.dumps({'html': "Already friends!"})
    except:
        return simplejson.dumps({'html': "all error!"})

@dajaxice_register
def show_friend(request):
    try:
        p = User.objects.get(username = request.session['username'])
    except:
        return simplejson.dumps({'html':'user problem, logout & login to fix the problem'})
    
    li = friends.models.Friendship.objects.friends_for_user(p)
    html =''
    for i in li:
        html +='<p>' + i['friend'].first_name + ' ' +  i['friend'].last_name + '</p><br>'
    return simplejson.dumps({'html': html})
