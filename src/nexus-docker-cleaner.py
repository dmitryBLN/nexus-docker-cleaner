import requests
import argparse
import os
from dotenv import load_dotenv

parser = argparse.ArgumentParser(
    prog="nexus-docker-cleaner.py",
    description="""Скрипт чистит docker репозиторий в Nexus от образов, с учетом установленной квоты.
                   Квота - кол-во образов для каждого тега, которые будут оставлены.""")
# Обработка параметра --no-interactive, отключающего интерактивный режим
parser.add_argument('--no-interactive', action='store_true', help='Отключает интерактивный режим, скрипт выполнит все задачи автоматически')
args = parser.parse_args()
noInteractiveMode=args.no_interactive

load_dotenv()
NEXUS_URL = str(os.environ.get('NEXUS_URL'))
REPOSITORY = str(os.environ.get('REPOSITORY'))
CLEAN_TASK_ID = str(os.environ.get('CLEAN_TASK_ID'))
USER_LOGIN = str(os.environ.get('USER_LOGIN'))
USER_PSW = str(os.environ.get('USER_PSW'))
SEARCH_REPOS = os.environ.get("SEARCH_REPOS").split(" ")
SEARCH_TAGS = os.environ.get("SEARCH_TAGS").split(" ")
SAVE_QUOTA = int(os.environ.get('SAVE_QUOTA'))

def UserConfirmation(question=""):
    if question != "":
        print(question)
    while True:
        response = input("Введите 'y' для согласия или 'n' для отказа: ")
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print("Некорректный ввод. Пожалуйста, введите 'y' или 'n'")

session = requests.Session()
session.auth = (USER_LOGIN, USER_PSW)

# Вывод информации о запущенной конфигурации скрипта
if noInteractiveMode:
    print("""
          Интерактивный режим отключен!
    Все задачи будут выполнены автоматически.""")
print(f"\nКонфигурация:"
      f"\n   Address Nexus: {NEXUS_URL}"
      f"\n   Docker Repository: {REPOSITORY}"
      f"\n   Cleaning Task ID: {CLEAN_TASK_ID}"
      f"\n   Search Images: {SEARCH_REPOS}"
      f"\n   Search Tags: {SEARCH_TAGS}"
      f"\n   Save Quota: {SAVE_QUOTA}"
      f"\n----")
# Подтвердждение о продолжении от пользователя
if noInteractiveMode or UserConfirmation("Продолжаем работу с такой конфигурацией? Чтобы её изменить задайте переменные окружения или отредактируйте файл .env"):
    print("Старт сбора образов для удаление...")
else:
    print("Работа завершена!")
    exit(0)

# Формирование списка образов на удаление
filteredImages = []
# Получаем список всех компонентов в репозитории
resp = requests.get(f"{NEXUS_URL}/repository/{REPOSITORY}/v2/_catalog")
js = resp.json()
allComponentsList = js['repositories']

# Каждый компонент из общего списка фильтруем по SEARCH_REPOS получаем список тегов и фильтруем по SEARCH_TAGS
for component in allComponentsList:
    if any(component.startswith(searchRepo) for searchRepo in SEARCH_REPOS):
        resp = requests.get(f"{NEXUS_URL}/repository/{REPOSITORY}/v2/{component}/tags/list")
        js = resp.json()
        tags = js['tags']
        filteredTagsCurrentComponent = []
        # Каждый тег перебираем и оставляем количество последних образов в соответствии с SAVE_QUOTA
        for searchTag in SEARCH_TAGS:
            filteredTagsCurrentSearchTag = [item for item in tags if item.startswith(f"{searchTag}")]
            if len(filteredTagsCurrentSearchTag) - SAVE_QUOTA > 0:
                filteredTagsCurrentSearchTag = filteredTagsCurrentSearchTag[:-SAVE_QUOTA]
                filteredTagsCurrentComponent+=filteredTagsCurrentSearchTag
        # формируем массив отфильтрованных копонентов и тегов
        if len(filteredTagsCurrentComponent):
            filteredImages.append({"name": component, "tags": filteredTagsCurrentComponent})

# Вывод информации об найденных удаляемых образах
if len(filteredImages):
    coutImages=0
    print("Будут удалены:")
    for image in filteredImages:
        coutImages+=len(image["tags"])
        lineIndent=len(image["name"])+4
        print("  {}:".format(image["name"]), end=" ")
        for i in range(0, len(image["tags"]), 10):
            print(" " * lineIndent * (1 if i !=0 else 0), image["tags"][i:i+10])
        print()
    print(f"Всего образов подлежащих удалению: {coutImages}.")

    # Удаление образов из репозитория
    if noInteractiveMode or UserConfirmation("Удаляем найденные образы?"):
        for image in filteredImages:
            for tag in image["tags"]:
                # Получение id для каждого образа
                resp = session.get("{}/service/rest/v1/search?repository={}&format=docker&name={}&version={}".format(NEXUS_URL, REPOSITORY, image["name"], tag))
                js = (resp.json())["items"][0]
                # Запрос на удаление образа по id
                session.delete(url=f"{NEXUS_URL}/service/rest/v1/components/{js['id']}")
        print("Все образы удалены!")

        # Запуск задачи на очистку блоба от неиспользуемых манифестов
        if CLEAN_TASK_ID != "":
            print ("\nЗапуск задачи по очистке не используемых манифестов в репозитории")
            if noInteractiveMode or UserConfirmation("Запускаем задачу?"):
                session.post(f"{NEXUS_URL}/service/rest/v1/tasks/{CLEAN_TASK_ID}/run")
                print("Задача запущена...")
        else:
            print ("\nID задачи по очистке от не используемых манифестов не задан, потребуется запустить её вручную:"
                   f"\n{NEXUS_URL}/#admin/system/tasks"
                   "\n\nЕсли данной задачи не существует - её необходимо создать и запустить.\n")
    else:
        print("Ничего не удалено.")
else:
    print("Не найдено ни одного образа подлежащего удалению!")
print("\nРабота завершена!")