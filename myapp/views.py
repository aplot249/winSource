# @author: sareeliu
# @date: 2022/3/13 19:20
import time

from django.shortcuts import render
from django.views import View
from django_filters.views import FilterView

from tools.emailSend import sendmail
from tools.win_source import *
from winSource.settings import BASE_DIR, Domain
# filters.py定义了用哪些字段对模型进行过滤
from .filters import ProductFilter
from .models import Product


class Index(View):
    def get(self, request):
        return render(request, template_name='myapp/index.html')


class Table(View):
    def get(self, request):
        return render(request, template_name="myapp/table.html")

    def post(self, request):
        # print(dict(request.POST))
        if request.POST.get("type") == "rfq":
            data = {
                'firstName': request.POST.get("firstName"),
                'lastName': request.POST.get("lastName"),
                'email': request.POST.get("email"),
                'phone': request.POST.get("phone"),
                'partNumber': request.POST.get("partNumber"),
                'manufacturer': request.POST.get("manufacturer"),
                'quantity': request.POST.get("quantity"),
                'targetPrice': request.POST.get("targetPrice"),
                'Datecode': request.POST.get("Datecode"),
                'additionalInformation': request.POST.get("additionalInformation")
            }
            html = f'''
                <h2>用户【{data['firstName']} {data['lastName']}】在网站进行了 Request For Quote：</h2>
                <p>邮箱号是：{data['email']}</p>
                <p>电话号是：{data['phone']}</p>
                <p>partNumber是：{data['partNumber']}</p>
                <p>manufacturer是：{data['manufacturer']} </p>
                <p>quantity是：{data['quantity']}</p>
                <p>targetPrice是：{data['targetPrice']}</p>
                <p>Datecode是：{data['Datecode']}</p>
                <p>补充信息是：{data['additionalInformation']}</p>
            '''
        else:
            file = request.FILES.get("file")
            file_name = f"{time.time()}-{str(file.name).replace(' ', '')}"
            tmp_path = BASE_DIR.joinpath("upload").joinpath(file_name)
            f = open(tmp_path, 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
            data = {
                'firstName': request.POST.get("firstName"),
                'lastName': request.POST.get("lastName"),
                'email': request.POST.get("email"),
                'phone': request.POST.get("phone"),
                'message': request.POST.get("message"),
                'file': Domain + 'media/' + file_name,
            }
            html = f'''
                <h2>用户【{data['firstName']} {data['firstName']}】在网站上传了 Bill of Materials (BOM) ：</h2>
                <p>邮箱号是：{data['email']} </p>
                <p>电话号是：{data['phone']} </p>
                <p>message是：{data['message']} </p>
                <p>提交的文件访问地址是：{data['file']}"</p>
            '''

        # 给他人时候这个发邮件的需要开启
        sendmail(html)
        print(data)
        # return HttpResponse(data)
        return render(request, 'myapp/upload_result.html', context={"data": data})


class AboutUs(View):
    def get(self, request):
        return render(request, template_name='myapp/about_us.html')


class UploadAndQuote(View):
    def get(self, request):
        return render(request, template_name='myapp/upload_and_quote.html')


def handleSearch(request):
    searchParam = request.GET.get("q")
    pageSize = request.GET.get("pagesize", 20)
    pageNumber = request.GET.get('pagenumber', 1)
    res = sensitive_sync_function(searchParam, pageSize=pageSize, pageNumber=pageNumber)
    # return JsonResponse(res)
    return render(request, template_name='myapp/index.html', context={'q': searchParam, 'res': res})


import pprint

mypprint = pprint.PrettyPrinter(indent=4)


class ProductView(FilterView):
    filter = None
    model = Product
    filter_class = ProductFilter
    template_name = 'myapp/product.html'
    paginate_by = 20  # 每页20条

    # 获取过滤后的查询集
    def get_queryset(self, **kwargs):
        qs = Product.objects.all().order_by('-id')
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        # mypprint.pprint(self.filter.qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_range'] = context['paginator'].get_elided_page_range(context['page_obj'].number, on_each_side=3,
                                                                           on_ends=2)
        context['q'] = self.request.GET['q']
        # mypprint.pprint(context)
        return context
