# Surface-tension-app

Qt-приложение для вычислений в области поверхностного натяжения жидкостей

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)

***

## Чтобы запустить на Windows, введите в Terminal

```bash
python -m venv venv
```

```bash
call venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

***

### Картинки используемых моделей

Пипетка с каплей

![Пипетка](images/пипетка.jpg)

Тело в форме спички, плавающее на поверхности жидкости

![Спичка](images/спичка.jpg)

Отрыв кольца

![Кольцо](images/кольцо.jpg)

Вертикальный капилляр с полностью смачиваемой жидкостью

![Капилляр](images/капилляр.jpg)

***

## Команды линтеров

```bash
black --exclude venv .
```

```bash
flake8 --exclude venv .
```
