from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# import time
import json

class ZhihuCrawler:
    def __init__(self,config_file="config.json"):
        # 读取config.json
        self.config=self._load_config(config_file)
        # url可以替换为其他知乎问题，直接复制网址即可
        self.URL="https://www.zhihu.com/question/292623424"
        
        # 设置浏览器选项
        options=Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={self.config['User-Agent']}")

        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        
        # 先访问主页注入cookies
        self.driver.get("https://www.zhihu.com")
        self._add_cookies(self.config["Cookie"])

        # 再对目标网页进行爬取
        self.driver.get(self.URL)
    
    def _load_config(self, config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _add_cookies(self,cookie_str):
        cookies=cookie_str.split("; ")
        for c in cookies:
            if "=" in c:
                k,v=c.split("=",1)
                self.driver.add_cookie({"name":k,"value":v})

    def _scroll_to_bottom(self):
        # 模拟下拉滑动,触发知乎动态加载
        while True:
            self.driver.execute_script("window.scrollBy(0, -10);")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if self.driver.find_elements(By.XPATH,"/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[4]/button"):
                print("没有更多内容了")
                break

    
    def _parse_question_title(self):
        """获取问题标题"""
        try:
            title_element = self.driver.find_element(By.CSS_SELECTOR, "h1.QuestionHeader-title")
            return title_element.text.strip()
        except:
            return "未知标题"
    def _parse_answers(self):
        """获取所有回答"""
        answer_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.RichContent-inner")
        answers = []
        for el in answer_elements:
            text = el.text.strip()
            if text:
                answers.append(text)
        return answers

    def _save_to_file(self, data, filename="zhihu_content.txt"):
        """保存到文件"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== 问题标题 ===\n")
            f.write(f"{data['title']}\n\n")

            if data['answers']:
                for i, ans in enumerate(data['answers'], 1):
                    f.write(f"=== 回答 {i} ===\n")
                    f.write(f"{ans}\n\n")
                f.write(f"总共找到 {len(data['answers'])} 个回答\n")
            else:
                f.write("未找到任何回答\n")

    def get_all_answers(self):
        """主流程"""
        self._scroll_to_bottom()
        
        title = self._parse_question_title()
        answers = self._parse_answers()

        data = {"title": title, "answers": answers}
        self._save_to_file(data)
        return data

    def close(self):
        self.driver.quit()




if __name__ == "__main__":
    crawler = ZhihuCrawler()
    data = crawler.get_all_answers()
    print(f"爬取完成，共 {len(data['answers'])} 个回答")
    crawler.close()