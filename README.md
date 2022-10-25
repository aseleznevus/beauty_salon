
## Анализ эффективности маркетинга салона красоты

В данной задаче в рамках тестового задания необходимо построить сквозную аналитику для салона красоты. У салона есть реклама в онлайне и сайт, через который можно оставить заявку на услугу. 

При помощи сквозной аналитики нужно проследить путь от клика по рекламному объявлению до покупки и, таким образом, оценить эффективность маркетинга. 

Клик по рекламе трансформируется в лид (заявку), а лид превращается в клиента, который уже может совершить некоторое количество покупок.

Необходимо подготовить данные для отчета по сквозной аналитике. Для решения можно использовать на выбор: SQL или Python (Pandas). 

### Связи

Связь между рекламой и заявкой определяется через utm метки - если набор меток из рекламного объявления совпадает с тем набором, который есть в заявке, то мы можем определить сколько денег было потрачено на привлечение этого лида 

Связь между лидом и продажами определяется через client_id.

### Атрибуция лид - покупка

Каждому лиду “в зачет” идут только те покупки, которые клиент сделал в первые 15 дней после создания заявки. Из-за особенности бизнеса соотношение лидов и продаж - многие ко многим. Существующий клиент может купить услугу повторно через заведение новой заявки, а может создать две заявки подряд и после этого сделать покупку. 

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
