import cfscrape
from lxml import etree


def sensitive_sync_function(searchParam, pageSize, pageNumber):
    result_dict = {}
    # 实例化一个create_scraper对象,请求报错，可以加上时延
    scraper = cfscrape.create_scraper(delay=10)
    # 获取网页源代码
    web_data = scraper.get(
        f"https://www.win-source.net/search?q={searchParam}&pagesize={pageSize}&pagenumber={pageNumber}").text
    # print(web_data)
    tree = etree.HTML(web_data)

    # pager_list = tree.xpath('//div[@class="pager"]/ul/li/a/@href')

    try:
        current_pager = tree.xpath('//div[@class="pager"]/ul/li[@class="current-page"]/span/text()')[0]
    except:
        current_pager = None

    try:
        last_pager = tree.xpath('//div[@class="pager"]/ul/li[@class="last-page"]/a/text()')[0]
    except:
        last_pager = None

    # print(current_pager,last_pager)

    try:
        preview_pager = int(current_pager) - 1 if int(current_pager) > 1 else None
    except:
        preview_pager = None

    try:
        next_pager = int(current_pager) + 1 if int(current_pager) < int(last_pager) else None
    except:
        next_pager = 2

    result_dict['pager_dict'] = {"preview_pager": preview_pager, "current_pager": current_pager,
                                 "next_pager": next_pager,
                                 "last_pager": last_pager}

    print(result_dict['pager_dict'])

    try:
        product_item = tree.xpath('//div[@class="item-grid"]/div[@class="item-box"]/div[@class="product-item"]')
        # print(product_item)
        data_list = []
        for item in product_item:
            picture = item.xpath('./div[@class="picture"]/a/img/@src')[0]
            if str(picture).endswith('147_125.jpeg') | str(picture).endswith('default-image_125.png'):
                # picture = "https://img2.baidu.com/it/u=169218525,969172668&fm=253&fmt=auto&app=138&f=JPEG?w=100&h=100"
                picture = "https://tse1-mm.cn.bing.net/th/id/R-C.b5e81f23c999e79f634a391f5696d75a?rik=TqlZmYxAqlqvQg&riu=http%3a%2f%2fbpic.588ku.com%2felement_pic%2f01%2f55%2f11%2f8757474f9d53b45.jpg&ehk=bRlcpyThLmrNIdjGr1a7YderIllOwO5WkDOBBvJmpTE%3d&risl=&pid=ImgRaw&r=0"
            item_detail = item.xpath('./div[@class="details"]')
            for item_d in item_detail:
                item_detail_title = item_d.xpath('./h2/a/@title')[0]
                item_detail_href = item_d.xpath('./h2/a/@href')[0]
                item_detail_manufacturer_title = item_d.xpath('./div[@class="manufacturer"]/a/@title')[0]
                item_detail_manufacturer_href = item_d.xpath('./div[@class="manufacturer"]/a/@href')[0]
                item_detail_addinfo = item_d.xpath('./div[@class="add-info"]/a/div/text()')
            item_availablity = item.xpath('./div[@class="availablity"]')
            for item_a in item_availablity:
                item_availablity_text = item_a.xpath('./div[@class="product-title"]/text()')
                item_availablity_price = item_a.xpath('./span/text()')
                item_availablity_env = item_a.xpath('./span[2]/span/img/@src')
                item_availablity_pdf = item_a.xpath('./span[2]/a/@href')

            # print(item_detail_title, item_detail_href, item_detail_manufacturer_title, item_detail_manufacturer_href,
            #       item_availablity_text, item_availablity_price, picture)

            data_list.append({
                'item_detail_title': item_detail_title,
                'item_detail_href': item_detail_href,
                'item_detail_manufacturer_title': item_detail_manufacturer_title,
                'item_detail_manufacturer_href': item_detail_manufacturer_href,
                'item_detail_addinfo': None if str(item_detail_addinfo[0]) == "\n" else item_detail_addinfo[0],
                'item_availablity_text': item_availablity_text[0].replace("pieces","") if item_availablity_text else None,
                'item_availablity_price': item_availablity_price[0] if item_availablity_price else None,
                'item_availablity_env': item_availablity_env[0] if item_availablity_env else None,
                'item_availablity_pdf': item_availablity_pdf[0] if item_availablity_pdf else None,
                'picture': picture
            })
        result_dict['data_list'] = data_list
    except:
        result_dict['data_list'] = []

    print(result_dict)
    return result_dict


# if __name__ == "__main__":
    # print(sensitive_sync_function())
