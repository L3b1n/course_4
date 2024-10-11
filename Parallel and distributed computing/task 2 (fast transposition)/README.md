# Problem Быстрое транспонирование
Input file name: standard input  
Output file name: standard output  
Time limit: 4 s  
Memory limit: 512 MB

В этой задаче вам потребуется выполнить несколько операций транспонирования квадратной подматрицы данной матрицы A. Матрицу A будет представлять линейным массивом d, т.е. $A_{i,j} = d_{i·n + j}$. Индексация строк и столбцов матрицы A начинается с 0.

Так как наша цель быстро выполнять именно операцию транспонирования, то входную матрицу нужно сгенерировать следующим генератором:
```cpp
vector<int> generate_input(int n, int seed) {
    vector<int> d(n * n);
    for (size_t i = 0; i < d.size(); ++i) {
        d[i] = seed; 
        seed = ((long long) seed * 197 + 2017) & 987654;
    }
    return d;
}
```

Кроме этого выводить в результате саму матрицу не требуется, а нужно вывести только результат работы следующей функции:

```cpp
long long get_hash(const vector<int>& d) {
    const long long MOD = 987654321054321LL;
    const long long MUL = 179;
    
    long long result_value = 0;
    for (size_t i = 0; i < d.size(); ++i)
        result_value = (result_value * MUL + d[i]) & MOD;
    return result_value;
}
```

# Входные данные
В первой строке входных данных записаны два целых числа n и seed $(1 \le n, seed \le 10000)$.

Вторая строка содержит число k $(1 \le k \le 10)$ — количество операций транспонирования.

Каждая из последующих k строк содержит описание подматрицы, которую нужно транспонировать: $i_{min}, j_{min} и side (0 \le i_{min}, j_{min} \lt n, 1 \le size \le n - max\{i_{min}, j_{min}\})$.

# Выходные данные
Выведите только результат вызова функции get_hash с параметром d равным результату транспонирования исходной матрицы k раз.

# Примеры
<table>
    <thead>
        <tr>
            <th align="center">входные данные</th>
            <th align="center">выходные данные</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>3 10<br>
                1<br>
                0 0 3
            </td>
            <td valign="top">537985024
            </td>
        </tr>
    </tbody>
    <tbody>
        <tr>
            <td>3 1<br>
                3<br>
                0 0 3<br>
                0 1 2<br>
                1 0 2
            </td>
            <td valign="top">5570561
            </td>
        </tr>
    </tbody>
    <tbody>
        <tr>
            <td>1111 111<br>
                1<br>
                11 1 111
            </td>
            <td valign="top">985162958569569
            </td>
        </tr>
    </tbody>
</table>

# Примечание
Ограничение по времени выставлено не менее чем с 20% запасом относительно авторского.