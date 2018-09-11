from django.shortcuts import render
from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect
import random
import string
import datetime
# Create your views here.


#def index(request):
#    return HttpResponse("Hello,world!")

class HomeView(View):
    def get(self,request): #get请求返回base.html
        return render(request,"base.html",{})


    def post(self, request):  # post请求
        if request.FILES:  # 如果有文件，向下执行，没有文件的情况,前端已经处理好。
            file = request.FILES.get("file")  # 获取文件
            name = file.name  # 获取文件名
            size = int(file.size)  # 获取文件大小
            with open('static/file/' + name, 'wb')as f:  # 写文件到static/files
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8))  # 生成随机八位的code
            u = Upload(
                path='static/file/' + name,
                name=name,
                Filesize=size,
                code=code,
                PCIP=str(request.META['REMOTE_ADDR']),  # 获取上传文件的用户ip
            )
            u.save()  # 存储数据库
            return HttpResponsePermanentRedirect("/s/" + code)
            # 使用 HttpResponsePermanentRedirect 重定向到展示文件的页面.这里的 code 唯一标示一个文件。

class DisplayView(View): #展示文件的视图类
    def get(self,request,code):  #支持get请求,并且可以接受一个参数，这里的 code 需要和 配置路由的code保持一致
        u = Upload.objects.filter(code=str(code)) #ORM 模型的查找
        if u: #如果u 有内容，u的访问次数+1.否则返回前端的内容为空
            for i in u :
                i.DownloadDocount +=1 #每次访问，访问次数+1
                i.save() #保存结果
        return render(request,'content.html',{"content":u}) #返回页面，其中content是 传给前端页面的内容
        
        #content.html在template文件夹中

class MyView(View): #用户管理类
    def get(self,request):
        IP = request.META['REMOTE_ADDR'] #获取用户IP
        u = Upload.objects.filter(PCMAC=str(IP))  #查找数据
        for i in u:
            i.DownloadDocount +=1 #访问量
            i.save()
        return render(request,'content.html',{"content":u}) #返回数据给前端

class SearchView(View):
    def get(self,request):
        code = request.GET.get("kw") #获取请求中的kw值，即搜索内容
        u = Upload.objects.filter(name=str(code))
        data = {}
        if u :
            for i in  range(len(u)):
                u[i].DownloadDocount +=1
                u[i].save()
                data[i]={}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = u[i].str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M')) #格式化时间
                data[i]['key'] = u[i].code
        return HttpResponse(json.dumps(data),content_type="application/json")
        #使用 HttpResponse 返回的是 json  ，content_type是标准写法
