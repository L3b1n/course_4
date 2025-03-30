# Lab 7

1) Генерируем файл .txt  
1. Название рецептора ( подготовленная мишень без ингибитора см. лаб. 5 )  
2. Координаты коробки для докинга (определяется через Chimera см лаб.6 )  
3. Размер коробки для докинга (определяется через Chimera см лаб.6 )  
4. Охват* ( мы будем использовать 20 ) это величина которая определяет, насколько всеобъемлющим будет поиск. Чем больше полнота, тем меньше вероятность упустить хороший результат.  
5. CPU  
```
receptor = RECEPTOR_ABL_mut/3cs9.receptor.pdbqt

center_x = 18
center_y = 8
center_z = 6

size_x = 31
size_y = 23
size_z = 23

exhaustiveness = 20

cpu = 1
```
2) Запустил докинг для 65 лигандов. Вот пример одного из выводного лога  
```
Reading input ... done.
Setting up the scoring function ... done.
Analyzing the binding site ... done.
Using random seed: 443085632
Performing search ... done.
Refining results ... done.

mode |   affinity | dist from best mode
     | (kcal/mol) | rmsd l.b.| rmsd u.b.
-----+------------+----------+----------
   1         -7.7      0.000      0.000
   2         -7.5      2.202      3.725
   3         -7.3      6.670      9.774
   4         -7.2      4.573      7.401
   5         -7.1     17.142     21.641
   6         -6.9      4.042     11.395
   7         -6.9      3.245      9.924
   8         -6.8      9.009     14.777
   9         -6.8     17.814     22.325
Writing output ... done.
```