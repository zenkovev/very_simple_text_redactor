# Простой текстовый редактор, созданный под влиянием блокнота и Vim'а.

Для запуска необходимо:
- Установить библиотеку Tkinter
> Здесь есть подробная инструкция:
> https://www.geeksforgeeks.org/how-to-install-tkinter-on-linux/
- Добавить файлу main.py права на исполнение
> $ chmod +x main.py
- Запустить файл из терминала
> $ ./main.py

В открывшемся окне можно писать и редактировать текст.
С помощью "Save to" этот текст можно сохранить в конкретный выбранный файл,
если файла не существует, он будет создан.
Также в текущее окно можно загрузить текст из конкретного файла, используя "Open".
При этом текст в текущем окне будет перезаписан.
На случай, если эта кнопка была нажата случайно, будут предупреждения в отдельных окнах.
"Save" позволяет сохранить результат в тот файл, который был открыт с помощью "Open".
Если такого файла не было, он аналогичен "Save to".
При этом также будут предупреждения о возможности потерять какие-либо данные.
Интерфейс всех этих операций достаточно интуитивный.
Exit выходит из программы.

Есть простые операции дла работы с текстом.
"Cut", "Copy", "Paste" и соответствующие им стандартные сочетания клавиш.
С помощью "Select all"/Ctrl+a можно выделить весь текст в окне.

Есть также сочетания клавиш для редактирования:
- Ctrl+p удаляет одно слово
- Ctrl+d удаляет одну строку
- Ctrl+r удаляет 10 строк или меньше,
если до конца документа менее 10 строк

С помощью Ctrl+Left и Ctrl+Right можно перемещаться по словам.
С помощью Ctrl+Up и Ctrl+Down можно перемещаться по строкам.
