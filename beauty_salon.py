# -*- coding: utf-8 -*-
"""beauty_salon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/aseleznevus/959078bf2c784b28d52a9be11ca5b7ef/beauty_salon.ipynb

#Анализ эффективности маркетинга салона красоты

## 0. Задание

### 1. Основное задание

В данной задаче в рамках тестового задания необходимо построить сквозную аналитику для салона красоты. У салона есть реклама в онлайне и сайт, через который можно оставить заявку на услугу. 

При помощи сквозной аналитики нужно проследить путь от клика по рекламному объявлению до покупки и, таким образом, оценить эффективность маркетинга. 

Клик по рекламе трансформируется в лид (заявку), а лид превращается в клиента, который уже может совершить некоторое количество покупок.

Необходимо подготовить данные для отчета по сквозной аналитике. Для решения можно использовать на выбор: SQL или Python (Pandas). 

Данные поступают на вход в виде 3 csv файлов:

- ads.csv
- leads.csv
- purchases.csv

[Скачать данные можно здесь](https://drive.google.com/drive/folders/1MjYyPUqfqqLBPwf2GIDhUEa0Qdbk7gIS?usp=sharing)

### Связи

Связь между рекламой и заявкой определяется через utm метки - если набор меток из рекламного объявления совпадает с тем набором, который есть в заявке, то мы можем определить сколько денег было потрачено на привлечение этого лида 

Связь между лидом и продажами определяется через client_id.

[https://drawsql.app/teams/xo/diagrams/1/embed](https://drawsql.app/teams/xo/diagrams/1/embed)

**Атрибуция лид - покупка**

Каждому лиду “в зачет” идут только те покупки, которые клиент сделал в первые 15 дней после создания заявки. Из-за особенности бизнеса соотношение лидов и продаж - многие ко многим. Существующий клиент может купить услугу повторно через заведение новой заявки, а может создать две заявки подряд и после этого сделать покупку. 

**Чтобы однозначно атрибутировать продажи к лидам мы подготовили примеры:**

1. У клиента несколько лидов подряд, а затем продажа. Продажа засчитывается последнему лиду, который был создан не позже, чем 15 дней до. 

![Mind Map.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f4be5e84-25bb-4a23-b9a0-a9f0ca39f8a9/Mind_Map.jpg)

1. У клиента несколько лидов подряд, а затем продажа. Продажа не засчитывается ни одному лиду, тк была создана позже 15 дней после последнего лида.

![Mind Map (1).jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bbe06478-446f-4bc5-b6b1-588494815d3a/Mind_Map_(1).jpg)

2. У клиента несколько лидов подряд, а затем продажа. Продажа засчитывается последнему лиду, который был создан не позже, чем 15 дней до. 

![Mind Map (2).jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f1368141-9f66-48ce-b0dd-20b3e308b60d/Mind_Map_(2).jpg)

1. У клиента несколько лидов и продаж вперемешку. Каждая продажа засчитывается ближайшему по времени лиду.
    
    ![Mind Map (3).jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/befc0260-48b3-48c0-8162-00308b12678d/Mind_Map_(3).jpg)
    
** ! Обратите внимание**

- Постарайтесь не использовать циклы, если вы пишете на pandas. В 99% случаев они вам не нужны.
- В данных могут быть дубли, а также логические несоответствия. В случае выявления подобного - очистите данные по своему усмотрению и укажите это в Комментарии.
- Не для каждого рекламного показа может быть заведена заявка, даже если деньги на нее потрачены.
- Оформляйте код так, чтобы его было легко читать, масштабировать и переиспользовать (ООП)

### 2. Дополнительные задания

- [ ]  Вывести результат в Looker Studio. В этом случае метрики CPL и ROAS создайте в виде вычисляемых полей.
    - Для референса можно использовать:
        
        ![d;lkmdsa;dlk.PNG](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6de0c729-b2c3-497d-ac79-29b5c2a120ea/dlkmdsadlk.png)
        
- [ ]  Покрыть пайплайн тестами и проверками на Data quality.
- [ ]  Поднять БД PostgreSQL, залить сырые данные и построить пайплайн так, чтобы читать и записывать данные из/в БД.

---

### Итоговый результат

1. Готовый отчет необходимо выгрузить в Google Spreadsheet и предоставить ссылку на него. 
    
    **Набор полей в отчете**:
    
    **Dimensions**
    
    - Дата
    - UTM source
    - UTM medium
    - UTM campaign
        
        **Metrics**
        
    - Количество кликов
    - Расходы на рекламу
    - Количество лидов
    - Количество покупок
    - Выручка от продаж
    - CPL  - Расходы/Количество лидов
    - ROAS - Выручка/Расходы

1. Код построения пайплайна необходимо выгрузить в Git репозиторий в виде .py файла и предоставить ссылку на репозиторий. Вы можете приложить решение в notebook, но это опционально. 

1. Результат по дополнительным заданиям (опционально): 
    - Приложите ссылку на отчет в Data Looker
    - Опишите, какие проверки интегрировали в скрипт
    - Приложите скрины из БД PostgreSQL с select запросами к сырым данным и отчету (4 скрина)

## 1. Предобработка данных

### 1.1. Вводные данные

В работу взяты данные о рекламных компаниях, лидах и продажах для салона красоты. 
Есть реклама в онлайне и сайт, через который можно оставить заявку на услугу. 

Клик по рекламе трансформируется в лид (заявку), а лид превращается в клиента, который может совершить некоторое количество покупок.

Период в течение которого лид должен становиться покупкой - 15 дней. Более длительные продажи не учитываются

**Задача анализа:** оценить эффективность рекламных кампаний салона красоты.

### 1.2. Подготовка данных
"""

#Используемые библиотеки
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

#Прогрузим данные
#ads
! gdown --id 1KKA88zHcg9NLfrjMp9gWzYnj8MbI6NZP

#leads
! gdown --id 1b2I7GHfv09eck1LBK4dmNBOLemRuUTf-

#purchases
! gdown --id 1OIrLxvrngEb2qewCa7r4Uy4ZbK5vsZUG

ads = pd.read_csv('/content/ads.csv')
leads = pd.read_csv('/content/leads.csv')
purchases = pd.read_csv('/content/purchases.csv')

"""### 1.3. Проверка данных"""

#Проверим корректность предоставленных данных и внесем правки при необходимости.
 ads.head(5)

ads.info()

leads.head()

leads.info()

purchases.head()

purchases.info()

"""Названия столбцов корректны, есть отсутствующие значения.
Требуется замена типов столбцов для дат
"""

#приведем типы столбцов в соответствие
ads['created_at'] = pd.to_datetime(ads['created_at'])
leads['lead_created_at'] = pd.to_datetime(leads['lead_created_at'])
purchases['purchase_created_at'] = pd.to_datetime(purchases['purchase_created_at'])

ads['d_utm_campaign'] = ads['d_utm_campaign'].astype('str')

#проверим данные на дубликаты
ads.duplicated().sum()

leads.duplicated().sum()

purchases.duplicated().sum()

#Изучим пропуски в столбцах и определим на что их можно заменить.
ads.isna().sum().sort_values(ascending=False)

"""Метка utm_term - не заполнена для всего датасета ads.
Данный столбец можно исключить.
"""

ads = ads.drop('d_utm_term', axis=1)

leads.isna().sum().sort_values(ascending=False)

#определим долю пропусков дл каждого из столбцов
pd.DataFrame(round(leads.isna().mean()*100,).sort_values(ascending=False)).style.background_gradient('coolwarm')

#удалим практически полностью отсутствующие столбцы
leads = leads.drop(['d_lead_utm_term'], axis=1)

leads = leads.drop(['d_lead_utm_content'], axis=1)

purchases.isna().sum().sort_values(ascending=False)

#удалим отсутствующие значение. Использовать данные без привязки к ID клиента некорректно
purchases['client_id'] = purchases['client_id'].dropna()

"""### 1.4. Выводы

В работу было принято три массива данных.
Они были проверены на отсутствующие значения, дубликаты.
Столбцы приведены в соответствии с типом данных.

Можно приступать к анализу информации.

## Анализ метрик

### 2.1. Объединение таблиц

Присоединим таблицу с лидами к таблице с рекламой

Связь между рекламой и заявкой определяется через utm метки - если набор меток из рекламного объявления совпадает с тем набором, который есть в заявке, то мы можем определить сколько денег было потрачено на привлечение этого лида
"""

data = ads.merge(leads, left_on=('d_utm_source', 'd_utm_medium',  'd_utm_campaign'), right_on=('d_lead_utm_source', 'd_lead_utm_medium', 'd_lead_utm_campaign'), how='inner')

"""Добавим таблицу с продажами.

Атрибуция лид - покупка

Каждому лиду “в зачет” идут только те покупки, которые клиент сделал в первые 15 дней после создания заявки. Из-за особенности бизнеса соотношение лидов и продаж - многие ко многим. Существующий клиент может купить услугу повторно через заведение новой заявки, а может создать две заявки подряд и после этого сделать покупку.
"""

all_data = data.merge(purchases, left_on=('client_id'), right_on=('client_id'), how='inner')

need_data = all_data.loc[(all_data['purchase_created_at'] - all_data['lead_created_at']).dt.days <= 15]

#Посчитаем количество кликов и расходы для каждой из компаний
clicks = need_data.pivot_table(index=[('d_utm_campaign')], values=('m_clicks', 'm_cost'), aggfunc='sum')
clicks = clicks.reset_index()

#добавим количество лидов и покупок
ppl_count = need_data.pivot_table(index=[('d_utm_campaign')], values=('lead_id', 'purchase_id'), aggfunc='count')
ppl_count = ppl_count.reset_index()

#добавим выручку от продаж
purchase_sum = need_data.pivot_table(index=[('d_utm_campaign')], values=('m_purchase_amount'), aggfunc='sum')
purchase_sum = purchase_sum.reset_index()

#Соберем итоговую таблицу
total_data = need_data[['created_at', 'd_utm_source', 'd_utm_medium', 'd_utm_campaign']]

total_data = total_data.merge(clicks, left_on=('d_utm_campaign'), right_on=('d_utm_campaign'), how='inner')
total_data = total_data.merge(ppl_count, left_on=('d_utm_campaign'), right_on=('d_utm_campaign'), how='inner')
total_data = total_data.merge(purchase_sum, left_on=('d_utm_campaign'), right_on=('d_utm_campaign'), how='inner')

#добавим метрики CPL и ROAS
total_data['cpl'] = total_data['m_cost'] / total_data['lead_id']
total_data['roas'] = total_data['m_purchase_amount'] / total_data['m_cost']

#оставим только уникальные значения по кампаниям
total_data = total_data.drop_duplicates (subset=['d_utm_campaign'])

#переименуем столбцы удобно
total_data.columns = ['date', 'utm_source', 'utm_medium', 'utm_campaign', 'click_count', 'click_costs_sum', 'leads_count', 'purchases_count', 'purchases_sum', 'cpl', 'roas']

total_data.head()

total_data.to_excel("beauty_salon_analitics.xlsx")

"""### 2.2. Графики CPL и ROAS"""

#соотнесем расходы на лиды и окупаемость рекламы.
total_data.plot.bar(x='utm_campaign', y='cpl', figsize=(10,6))
plt.title('Анализ стоимости привлечения лидов для каждой из кампаний​')
plt.show()

total_data.plot.bar(x='utm_campaign', y='roas', figsize=(10,6))
plt.title('Анализ окупаемости рекламы для каждой из кампаний​')
plt.show()

cpl_roas = total_data.groupby('utm_campaign')['cpl', 'roas'].sum()
cpl_roas.plot(figsize=(15, 5), title=('Анализ стоимости привлечения лидов и окупаемости рекламы для каждой из кампаний')) 
plt.show()

