from bs4 import BeautifulSoup
import pandas as pd
import re
import os


class Share(object):
    def __init__(self, **kwargs):
        self.code = ''
        self.name = ''
        self.amount = ''
        self.point = 0
        self.PB = 0
        self.ROE = 0
        self.stocks = []
        self.code_list = []
        self.doc = kwargs.get('doc_html')
        if os.path.exists(r'./moyu100.csv'):
            file_path = kwargs.get('file_csv')
            self.df = pd.read_csv(file_path, encoding='gbk', dtype={'股票代码': str})
        else:
            self.df = pd.DataFrame()

    def main(self):
        soup = BeautifulSoup(open(self.doc, encoding='utf-8'), features='lxml')
        if self.df.empty:
            self.stocks = [name.string.strip() for name in
                           soup.find_all('div', 'name___3jt4_')]  # <div class="name___3jt4_">
            self.code_list = [code.string.strip() for code in
                              soup.find_all('div', 'code___1acmC')]  # <div class="code___1acmC">

            self.df = pd.DataFrame({'股票代码': self.code_list, '股票名称': self.stocks})
        soup_card = soup.find_all('div', id='card')[0].div
        card = soup_card.find_all('div', string=re.compile('(\d+)'))
        if len(card) == 5:
            card_string = [c.string.strip() for c in card]
            self.code = re.sub(r'\D', "",
                               card_string[0])  # re.sub(pattern, repl, string, count=0, flags=0) ## 删除非数字(-)的字符串
            self.name = re.search('\w+', card_string[0]).group()
            card_paPR = list(map(lambda x: {x.split("：")[0]: x.split("：")[1]},
                                 card_string[1:]))  # map(a, b) ## a 是函数，用来处理 b 参数 ## b 是可迭代对象
            self.point = card_paPR[0].get('摸鱼得分')
            self.amount = card_paPR[1].get('市值')
            self.PB = card_paPR[2].get('PB')
            self.ROE = card_paPR[3].get('ROE')
            self.df.loc[self.df['股票代码'] == self.code, '摸鱼得分'] = self.point
            self.df.loc[self.df['股票代码'] == self.code, '市值'] = self.amount
            self.df.loc[self.df['股票代码'] == self.code, 'PB'] = self.PB
            self.df.loc[self.df['股票代码'] == self.code, 'ROE'] = self.ROE
            self.df.to_csv(r'moyu100.csv', encoding='gbk', index=False)
            print(self.df[self.df['PB'].isna()]['股票名称'])
            print(self.df.count())
            return self.df


if __name__ == '__main__':
    share = Share(doc_html='a1.html', file_csv='moyu100.csv')
    share.main()
