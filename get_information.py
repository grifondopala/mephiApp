from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def authorization(login, password): #авторизация на сайт
    driver.get("https://home.mephi.ru/")
    driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/form/button").submit() #первая кнопка входа
    driver.find_element(By.XPATH, "//*[@id=\"username\"]").send_keys(login) #ввод логина
    driver.find_element(By.XPATH, "//*[@id=\"password\"]").send_keys(password) #ввод пароля
    driver.find_element(By.XPATH, "//*[@id=\"login-form\"]/div[3]/button").submit()  # вторая кнопка входа
    return get_schedule(driver.current_url)

def get_schedule(user_href): #получить расписание
    lesson_classes = ['lesson lesson-att', 'lesson lesson-test', 'lesson lesson-practice', 'lesson', 'lesson lesson-lecture']
    useless = ['1','2','3','4','5','6','7','8','9','0','В']
    for i in range(-5, 6):
        if i != 0:
            driver.get(f'{user_href}?offset={i}')
        else:
            driver.get(user_href)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for lesson in soup.find_all("div", class_="list-group-item"):
            time = lesson.find("div", class_="lesson-time").get_text()
            for lesson_class in lesson_classes:
                if(lesson.find("div", class_=lesson_class) is not None):
                    lesson_div = lesson.find("div", class_=lesson_class)
                    info = list(filter(lambda a: a != '', lesson_div.get_text().split('\n')))
                    if info[2] in useless:
                        info.pop(2)
                    type = info[1]
                    lesson_name = info[2]
                    audience = lesson_div.find("div", class_="pull-right").find("a", class_="text-nowrap").get_text()
                    teacher = lesson_div.find("span", class_="text-nowrap").find("a", class_="text-nowrap").get_text()
                    skype = lesson_div.find("span", class_="text-nowrap").find("a", class_="text-skype").get("href")
                    break
            print(time, lesson_name, type, audience, teacher, skype)
        print("-----------------")



authorization("ggg003","grig1001")