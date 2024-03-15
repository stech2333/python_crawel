import requests
from bs4 import BeautifulSoup as bs

def get_HTML(url):
        try:
            head = {"user-agent":"MOzilla/5.0"}
            usi = requests.get(url,timeout = 30,headers = head)
            usi.encoding = usi.apparent_encoding
            return usi.text
        except:
               return 0
        
def main():
       url = "https://www.shanghairanking.cn/rankings/bcur/2023"
       html = get_HTML(url)
       demo = bs(html,'html.parser')
# 使用find_all方法查找所有class值为name-cn的a标签
       a_tags = demo.find_all('a', class_='name-cn')
       m_tags = demo.find_all('a', class_='name-en')

# 遍历a标签,m标签并返回其值
       x = 0
       print("{:^10}\t{:^6}".format("排名","学校"))
       for a,m in zip(a_tags,m_tags):
            print("{:^10}\t{:^6}\t{:^10}".format(x+1,a.text,m.text))
            x+=1

if __name__ == "__main__":
      main()