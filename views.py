from django.shortcuts import render
from .models import GradeSummary, FilmComments, PersonSummary 
from .db import save_from_json 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib.auth.decorators import login_required
import requests, logging, os
import subprocess, pypinyin
from django.conf import settings

# Create your views here.
def index(request):
    context = {}
    context['user'] = request.user.username
    result_sets = GradeSummary.objects.all().order_by('-high_recommend').values()
    paginator = Paginator(result_sets, 20)

    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context['film_grade_list'] = contacts
    return render(request, 'douban/index.html', context)

def persons(request):
    context = {}
    context['user'] = request.user.username
    context['film_grade_list'] = PersonSummary.objects.all().order_by('-sum').values()
    #result_sets = PersonSummary.objects.filter(sum__gt = 1).order_by('-sum').values()
    result_sets = PersonSummary.objects.order_by('-sum').values()
    paginator = Paginator(result_sets, 20)

    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context['film_grade_list'] = contacts
    return render(request, 'douban/persons.html', context)


def detail(request, person, name, grade_info):
    context = {}
    context['user'] = request.user.username
    grade_dic = {
            'all':None,
            'high':'力荐',
            'recommend':'推荐',
            'general':'还行',
            'poor':'较差',
            'verypoor':'很差',
            }
    grade_flag = grade_dic[grade_info]
    if(person):
        result_sets = FilmComments.was_filtered_by(cname=name, gr=grade_flag)
    else:    
        result_sets = FilmComments.was_filtered_by(fname=name, gr=grade_flag)
    paginator = Paginator(result_sets, 25)

    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context['film_info'] = contacts
    return render(request, 'douban/detail.html', context)

@login_required(login_url='login.html') 
def update(request):
    context = {}
    context['user'] = request.user.username 
    douban = request.session['douban']
    city = request.session.get('city')
    py_city = pypinyin.lazy_pinyin(city)
    py_city.pop()
    url = 'https://movie.douban.com/cinema/nowplaying/{}/'.format("".join(py_city))
    if(request.method == 'POST'):
        movie_name = request.POST['movie_name']
        # transfer cookies to a string
        scrapy_cookies = []
        for key in douban.keys():
            scrapy_cookies.append(key)
            scrapy_cookies.append(douban[key])
        file_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'douban', 'tools', 'scrapy', 'film_comments')
        result_path = os.path.join(file_dir, 'result.json')
        if(os.path.isfile(result_path)):
            os.remove(result_path)
        child = subprocess.Popen("scrapy crawl douban -a FILM_NAME=\"{}\" -a COOKIES=\"{}\" -a START_URL=\"{}\" -o result.json".format(movie_name, '@'.join(scrapy_cookies), url), shell=True, cwd=file_dir)
        child.wait()
        save_from_json(result_path)
        if(movie_name.lower() == "all"):
            return HttpResponseRedirect('/douban')
        else:
            return HttpResponseRedirect('/douban/{}/all_comments.html'.format(movie_name))
    else:
        # all movies that is playing in cinema now
        response = requests.get(url, cookies=douban)
        soup = BeautifulSoup(response.text, 'lxml')
        context['city'] = city
        context['all_movies_names'] = []
        for movie in soup.find('div', id='nowplaying').find_all('li', class_='list-item'):
            context['all_movies_names'].append(movie['data-title'])
        return render(request, 'douban/update.html', context)            
 
@login_required(login_url='login.html') 
def logout(request):
    # logout in douban.com
    # get cookies given by douban.com, is a dict
    douban = request.session['douban']
    response = requests.get('https://movie.douban.com', cookies=douban)
    soup = BeautifulSoup(response.text, 'lxml')
    user_acct = soup.find('li', class_='nav-user-account')
    if(user_acct):
        # logout url in douban.com
        lgo_url = user_acct.find_all('a')[-1]['href']
        if(BeautifulSoup(requests.get(lgo_url, cookies=douban).text, 'lxml').find('form', id='lzform')):
            lgo(request)
            return HttpResponse("<span>你已成功登出。<a href='login.html'>重新登录</span>")
    else:
        # maybe already logout in douban.com
        lgo(request)
        return HttpResponse("<span>登出失败。可能是你在此期间，从豆瓣官网登出了。</span>")

def login(request):
    if(request.user.is_authenticated):
        return HttpResponse("<span>Hi <p>{}</p> 你已经登录过了。<a href='logout.html'>登出</span>".format(request.user.username))
    context = {}
    if(request.method == 'POST'):
        form = request.POST
        if(form):
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Connection":"keep-alive",
                "User-Agent":"'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'"
            }
            data={
                'source':'None',
                'redir':'https://movie.douban.com/',
                'form_email':form['username'],
                'form_password':form['password'],
                'login':'登录'
            }
            if('authcode' in form and 'authid' in form):
                data['captcha-solution'] = form['authcode'] 
                data['captcha-id'] = form['authid']
            # create a connect session with douban.com
            with requests.Session() as s:
                response = s.post('https://www.douban.com/accounts/login', headers=headers, data=data)
                cookies = s.cookies 
                soup = BeautifulSoup(response.text, 'lxml')
                error = soup.find('p', class_='error')
            if(error):
                # return error information if login douban.com failed
                context['error'] = error.get_text() 
                # captcha in need if login next time
                captcha = soup.find('div', class_='item item-captcha')
                if(captcha):
                    context['captcha'] = captcha
                    context['auth_img_src'] = captcha.img['src']
                    context['auth_id'] = captcha.find_all('input')[-1]['value']
                return render(request, 'douban/login.html', context)            
            else:
                # login douban.com successful
                # authenticate this user
                user = authenticate(username=form['username'], password=form['password'])
                if(user is None):
                    # user not exists, create
                    user = User.objects.create_user(username=form['username'], password=form['password'])
                    user.save()
                # authenticate pass, login system    
                if(user.is_active):
                    lgi(request, user)
                # save cookies from douban.com to session with a dict 
                request.session['douban'] = cookies.get_dict()
                # locate your city
                payload = {'ak':settings.BAIDU_AK}
                resp = requests.post('https://api.map.baidu.com/location/ip', data=payload).json()
                if(resp['status'] == 0):
                    # locate successful, save in sessions
                    request.session['city'] = resp['content']['address_detail']['city']
                else:
                    # default city is beijing
                    request.session['city'] = "北京市"
                if('next' in request.GET):
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect('/douban')
    else:
        soup = BeautifulSoup(requests.get('https://www.douban.com/accounts/login').text, 'lxml')
        captcha = soup.find('div', class_='item item-captcha')
        if(captcha):
            context['captcha'] = captcha
            context['auth_img_src'] = captcha.img['src'] 
            context['auth_id'] = captcha.find_all('input')[-1]['value']
        return render(request, 'douban/login.html', context)            
