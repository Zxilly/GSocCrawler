import requests
from bs4 import BeautifulSoup

proxies = {
    'http': 'http://127.0.0.1:10676',
    'https': 'http://127.0.0.1:10676',
}

proxySession = requests.session()
proxySession.proxies = proxies

baseURL = 'https://summerofcode.withgoogle.com'
targetURL = baseURL + "/archive/2020/organizations/"

GSocMainPage = proxySession.get(targetURL).content

GSocMainBS = BeautifulSoup(GSocMainPage, 'lxml')

GSocOrganizationsBS = GSocMainBS.find(class_='organization-list-container')

GSocOrganizationNumber = len(GSocOrganizationsBS.find_all('li'))

print("Find %d organization." % GSocOrganizationNumber)

OrganizationPointer = 1

GSocOrganizationsInfoList = []
CrawlerErrorList = []

for mainPageOneOrganizationBS in GSocOrganizationsBS.find_all('li'):

    oneOrganizationURL = baseURL + mainPageOneOrganizationBS.a['href']
    oneOrganizationPage = proxySession.get(oneOrganizationURL).content
    oneOrganizationBS = BeautifulSoup(oneOrganizationPage, 'lxml')

    title = str(oneOrganizationBS.find(class_='banner__title').string)

    print('Handling %d / %d Organization, %s' % (OrganizationPointer, GSocOrganizationNumber, title))
    OrganizationPointer += 1

    # print(oneOrganizationBS.prettify())
    metasBS = oneOrganizationBS.find(class_='org__meta')
    # print(metasBS.prettify())
    if metasBS is None:
        print('%s meet error, continue' % title)
        CrawlerErrorList.append({
            'title': title,
            'url': oneOrganizationURL
        })
        continue
    idealistURL = metasBS.find(class_='org__button-container').find('md-button')['href']
    technologyList = []
    for oneTechnologyBS in metasBS.find_all(class_='organization__tag--technology'):
        technologyList.append(str(oneTechnologyBS.string))
    category = metasBS.find(class_='organization__tag--category')
    topicsList = []
    for oneTopicBS in metasBS.find_all(class_='organization__tag--topic'):
        topicsList.append(str(oneTopicBS.string))

    GSocOrganizationsInfoList.append({
        'title': title,
        'url': oneOrganizationURL,
        'category': category,
        'idealistURL': idealistURL,
        'technologyList': technologyList,
        'topicsList': topicsList
    })

print(GSocOrganizationsInfoList)
