<header>
  <h1>🏦 Banking Data Handler</h1>
  <p><strong>Интеллектуальная система для комплексного анализа, фильтрации, конвертации, парсинга и логирования банковских транзакций.</strong></p>
  <p>Разработано в рамках профильного курса по бэкенд-разработке от <b>Skypro</b>.</p>
</header>

<hr />

<section>
  <h2>🛠️ Технологический стек</h2>

  <table>
    <thead>
      <tr>
        <th>Категория</th>
        <th>Инструменты и библиотеки</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Язык программирования</b></td>
        <td>Python 3.12+</td>
      </tr>
      <tr>
        <td><b>Пакетный менеджер</b></td>
        <td>Poetry</td>
      </tr>
      <tr>
        <td><b>Тестирование</b></td>
        <td>Pytest, Pytest-Mock, Pytest-Cov</td>
      </tr>
      <tr>
        <td><b>Аналитика и парсинг</b></td>
        <td>Pandas, OpenPyXL, CSV</td>
      </tr>
      <tr>
        <td><b>Работа со строками и API</b></td>
        <td>Regular Expressions (<code>re</code>), Requests, Python-Dotenv</td>
      </tr>
      <tr>
        <td><b>Качество кода</b></td>
        <td>Flake8, Black, Isort, Mypy</td>
      </tr>
    </tbody>
  </table>
</section>

<hr />

<section>
  <h2>🚀 Архитектура и функциональные модули</h2>

  <h3>🛡️ 1. Маскирование и виджеты (<code>src/masks.py</code>, <code>src/widget.py</code>)</h3>
  <p>Обеспечивает защиту конфиденциальных платежных реквизитов клиента и форматирование дат:</p>
  <ul>
    <li><code>get_mask_card_number</code> — маскирует номер банковской карты в формате <code>XXXX XX** **** XXXX</code>.</li>
    <li><code>get_mask_account_number</code> — скрывает номер банковского счета до формата <code>**XXXX</code>.</li>
    <li><code>mask_account_card</code> — автоматически распознает тип реквизита (карта или счет) и применяет нужную маску.</li>
    <li><code>get_date</code> — преобразует дату и время из ISO-формата в читаемый вид <code>ДД.ММ.ГГГГ</code>.</li>
  </ul>

  <h3>⚙️ 2. Фильтрация, сортировка и статистика (<code>src/processing.py</code>, <code>src/regular_expressions.py</code>, <code>src/counting_categories.py</code>)</h3>
  <ul>
    <li><code>filter_by_state</code> — отбирает банковские операции по статусу (<code>EXECUTED</code>, <code>CANCELED</code>, <code>PENDING</code>).</li>
    <li><code>sort_by_date</code> — упорядочивает транзакции по дате (по возрастанию или убыванию).</li>
    <li><code>filter_operations_by_description</code> — регистронезависимый поиск операций по ключевым словам с экранированием спецсимволов (<code>re</code>).</li>
    <li><code>count_operations_by_category</code> — подсчет количества транзакций по заданным категориям на базе <code>collections.Counter</code>.</li>
  </ul>

  <h3>🔍 3. Потоковая обработка и генераторы (<code>src/generators.py</code>)</h3>
  <p>Оптимизированный инструмент для работы с большими массивами финансовых данных без перегрузки оперативной памяти:</p>
  <ul>
    <li><code>filter_by_currency</code> — ленивый итератор, динамически фильтрующий транзакции по коду валюты (<code>USD</code>, <code>RUB</code>, <code>EUR</code>).</li>
    <li><code>transaction_descriptions</code> — генератор текстовых описаний для каждой банковской операции.</li>
    <li><code>card_number_generator</code> — генератор номеров карт в заданном диапазоне в формате <code>XXXX XXXX XXXX XXXX</code>.</li>
  </ul>

  <h3>📊 4. Загрузка данных и конвертация валют (<code>src/utils.py</code>, <code>src/pandas_library.py</code>, <code>src/external_api.py</code>)</h3>
  <ul>
    <li><b>JSON-парсер:</b> безопасное чтение и валидация транзакций из <code>.json</code> с записью событий в <code>logs/utils.log</code>.</li>
    <li><b>CSV и Excel парсеры:</b> считывание реестров операций из таблиц <code>.csv</code> и <code>.xlsx</code> с помощью <b>Pandas</b>.</li>
    <li><b>Конвертер валют:</b> перевод сумм из <code>USD</code> и <code>EUR</code> в рубли (<code>RUB</code>) по актуальному курсу через Exchangerates Data API.</li>
  </ul>

  <h3>📝 5. Декоратор автоматического контроля (<code>src/decorators.py</code>)</h3>
  <ul>
    <li><code>@log</code> — параметризованный декоратор для трекинга работы функций. Фиксирует успешное выполнение или тип возникшей ошибки вместе с переданными аргументами.</li>
    <li><b>Гибкий вывод:</b> поддерживает запись как в консоль (<code>stdout</code>), так и в локальный файл при передаче параметра <code>filename</code>.</li>
  </ul>
</section>

<hr />

<section>
  <h2>🧪 Тестирование и контроль качества кода</h2>
  <p>Проект покрыт модульными тестами с использованием фикстур, параметризации и мок-объектов (<code>unittest.mock</code>, <code>pytest-mock</code>).</p>

  <pre><code class="language-bash"># Запуск всех тестов с отчетом о покрытии кода
poetry run pytest --cov=src --cov-report=term-missing

# Проверка стиля кода (PEP 8) и строгой типизации
poetry run flake8
poetry run mypy src tests

# Автоматическое форматирование кода и импортов
poetry run isort .
poetry run black .</code></pre>
</section>

<hr />

<section>
  <h2>💻 Инструкция по развертыванию и запуску</h2>

  <h3>1. Клонирование репозитория</h3>
  <pre><code class="language-bash">git clone https://github.com
cd banking-data-handler</code></pre>

  <h3>2. Установка зависимостей через Poetry</h3>
  <pre><code class="language-bash">poetry install</code></pre>

  <h3>3. Настройка переменных окружения</h3>
  <p>Создайте файл <code>.env</code> в корне проекта (по образцу <code>.env.example</code>) и укажите ваш API-ключ для конвертации валют:</p>
  <pre><code class="language-env">EXCHANGE_API_KEY=ваш_ключ_от_apilayer</code></pre>

  <h3>4. Запуск приложения</h3>
  <pre><code class="language-bash">poetry run python src/main.py</code></pre>
</section>

<hr />

<footer>
  <p>💡 <i>Проект выполнен в соответствии с техническим заданием и учебными стандартами Skypro.</i></p>
</footer>
