from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def authorization(login, password, my_range): #авторизация на сайт
    driver.get("https://home.mephi.ru/")
    driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/form/button").submit() #первая кнопка входаl
    driver.find_element(By.XPATH, "//*[@id=\"username\"]").send_keys(login) #ввод логина
    driver.find_element(By.XPATH, "//*[@id=\"password\"]").send_keys(password) #ввод пароля
    driver.find_element(By.XPATH, "//*[@id=\"login-form\"]/div[3]/button").submit()  # вторая кнопка входа
    if driver.current_url == "https://auth.mephi.ru/login":
        return "Неверный логин или пароль"
    else:
        return get_schedule(driver.current_url, my_range)

def get_schedule(user_href, my_range): #получить расписание
    lesson_classes = ['lesson lesson-att', 'lesson lesson-test', 'lesson lesson-practice', 'lesson', 'lesson lesson-lecture']
    useless = ['1','2','3','4','5','6','7','8','9','0','В']
    days_shedule = []
    for i in my_range:
        if i != 0:
            driver.get(f'{user_href}?offset={i}')
        else:
            driver.get(user_href)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        day_shedule = []
        for index, lesson in enumerate(soup.find_all("div", class_="list-group-item")):
            time = lesson.find("div", class_="lesson-time").get_text().replace("\xa0"," ")
            lesson_was = lesson.find_all("div", class_="lesson-was")
            for item in lesson_was:
                for lesson_class in lesson_classes:
                    if (item.find("div", class_=lesson_class) is not None):
                        lesson_div = item.find("div", class_=lesson_class)
                        info = list(filter(lambda a: a != '', lesson_div.get_text().split('\n')))
                        if info[2] in useless:
                            info.pop(2)
                        type = info[1]
                        lesson_name = info[2]
                        audience = lesson_div.find("div", class_="pull-right").find("a", class_="text-nowrap").get_text()
                        teachers = []
                        for teacher in lesson_div.find_all("span", class_="text-nowrap"):
                            skypes = []
                            skypes.append(teacher.find("a", class_="text-nowrap").get_text().replace("\xa0", " "))
                            for item in teacher.find_all("a", class_="text-skype"):
                                skypes.append(item.get("href"))
                            teachers.append(skypes)
                        day_shedule.append([index, time, type, lesson_name, teachers, audience])
                        break
        days_shedule.append(day_shedule)
    return days_shedule
