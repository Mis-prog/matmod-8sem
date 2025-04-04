Лабораторные по математическому моделированию за 8 семестр 
----------------

### Cборка 1 ЛР
```
mkdir build && cd build
cmake .. 
cmake --build . --config Release -t lab1_misha_v2
./lab1/misha/lab1_misha_v2
```

### Cборка 3 ЛР
```
mkdir build && cd build
cmake .. 
cmake --build . --config Release -t lab3_misha
./lab3/misha/lab3_misha
```

### Сборка 4 ЛР
Первое задание
```
mkdir build && cd build
cmake .. 
cmake --build . --config Release -t lab4_misha
./lab4/misha/lab4_misha
```
Второе задание 
```
cd lab4/misha/
source bin/Scripts/activate
pip install -r requirements.txt
python main_part3.py
```

### Информация
Подробно проект описан в Wiki