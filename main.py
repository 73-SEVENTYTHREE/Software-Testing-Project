from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

if __name__ == '__main__':
    columns = (
        "债券全称", "债券代码", "发行日期", "计划发行量（亿元）", "实际发行量（亿元）", "付息方式", "付息频率", "票面利率（%）", "基本利差（%）", "当期基础利率", "首次划款日",
        "发行日期",
        "发行开始日", "上市流通日", "发行手续费率（%）", "兑付手续费率（%）", "发行价格（元）", "参考收益率（%）", "选择权类别", "下一次赎回日", "债券评级机构", "债券期限",
        "债券信用评级",
        "主体信用评级", "主体评级机构", "ISIN码", " ", "浮动利率基准", "发行人简称", "剩余本金值", "债券简称", "起息日", "发行截止日", "选择权类别", "备注")

    df = pd.DataFrame(columns=columns)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0'
                             '.2704.63 Safari/537.36'}
    part1 = "https://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber="
    page_number = 1
    count_row = 0
    part2 = "&queryType=0&sType=2&zqdm=&zqjc=&zqxz" \
            "=00&eYear2=0000&bigPageNumber="
    bigPageNumber = 1
    is_First_page = 1
    part3 = "&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1" \
            "&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=&wsYear=&weYear=&eWhere=&sEnd=0" \
            "&fxksr=-00-00&fxjsr=-00-00&fxStart=-00-00&fxEnd=-00-00&dfStart=-00-00&dfEnd=-00-00&start=0&zqfxr=&fuxfs=&faxfs" \
            "=00&zqxs=00&bzbh=&sYear=&sMonth=00&sDay=00&eYear=&eMonth=00&eDay=00&fxStartYear=&fxStartMonth=00&fxStartDay=00" \
            "&fxEndYear=&fxEndMonth=00&fxEndDay=00&dfStartYear=&dfStartMonth=00&dfStartDay=00&dfEndYear=&dfEndMonth=00" \
            "&dfEndDay=00&col=28%2C2%2C5%2C33%2C7%2C21%2C11%2C12%2C23%2C25%2C0%2C3%2C31%2C32%2C6%2C8%2C9%2C10%2C13%2C14" \
            "%2C15%2C16%2C17%2C19%2C22%2C24%2C26%2C27%2C29%2C20 "
    while page_number < 1209:
        url = part1 + str(page_number) + part2 + str(bigPageNumber) + part3
        res = requests.get(url, headers=headers)  # Get该网页从而获取该html内容
        # print(res.text)
        page_number += 25
        bigPageNumber += 1
        soup = BeautifulSoup(res.text, 'html.parser')
        js = soup.select("body script")
        result_str = str(js[62])
        begin = "'"
        end = "'"
        sentence = begin + "(.+)" + end
        sentence1 = "''"
        result_str = re.sub(sentence1, "' '", result_str)
        pattern = re.compile(sentence)
        info_list = pattern.findall(result_str)
        result_list = []
        count = 0
        stop_flag = 0
        if is_First_page == 1:
            index = 34
            is_First_page = 0
        else:
            index = 0
        while count < 35 and index < len(info_list):
            result_list.append(info_list[index])
            index += 1
            count += 1
            if count == 35:
                print(result_list)
                df.loc[count_row] = result_list
                count_row += 1
                result_list.clear()
                count = 0
    df.to_excel('output.xlsx', index=False)
