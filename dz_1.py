
#==========================================================
# Разобрать че делает каждая функция перед отправкой дз!!!
# Из Gemini -> Помощь с кодом из Colab
# p - степень (ключ), c - коэффицент (значение)
#==========================================================

class Polynomial:
    def _clean_zeros(self):
        # проходим по всем элементам словаря и собираем в список
        # ключи-степени p, где коэффициент c равен 0
        zeros = [p for p,c in self._coeffs.items() if c == 0]
        # перебираем все степени с нулевыми коэффициентами и удаляем их
        for p in zeros:
            del self._coeffs[p]


    def degree(self):
        # очищаем словарь от случайных нулей перед вычислением
        self._clean_zeros()
        # если есть степени, возвращаем максимальный ключ, иначе - степень 0
        return max(self._coeffs.keys()) if self._coeffs else 0


    def __init__(self, *coefficients):
        self._coeffs = {} # {степень: коэффицент} (принцип)
        # если пусто, то ничего не возвращаем
        if not coefficients: return
        # случай, если дан 1 коэфф-т
        if len(coefficients) == 1:
            arg = coefficients[0] # достаем его
            if isinstance(arg, Polynomial):
                self._coeffs = arg._coeffs.copy() # просто копируем словарь
            elif isinstance(arg, dict):
                # Проходим по парам (p, c) в переданном словаре
                for p,c in arg.items():
                    # записываем ненулевые коэфф-ы
                    if c!= 0: self._coeffs[p] = c
            elif isinstance(arg, (list,tuple)):
                for p,c in enumerate(arg):
                    if c!=0: self._coeffs[p] = c
            elif isinstance(arg, (int,float)):
                if arg!=0: self._coeffs[0] = arg # просто записываем коэфф-т
            else:
                raise TypeError("Несуществующий тип данных")
        # случай, если записаны через запятую коэфф-ы
        else:
            for p,c in enumerate(coefficients):
                if c!=0: self._coeffs[p] = c
        self._clean_zeros()

    def __repr__(self):
        self._clean_zeros()
        if not self._coeffs: return "Polynomial []"
        deg = self.degree()
        # образуем список со всеми степенями
        dense_list = [self._coeffs.get(i, 0) for i in range(deg+1)]
        return f"Polynomial {dense_list}"
        # dense_list - здесь хранятся все коэфф-ы, в том числе нулевые коэфф-ы.

    def __str__(self):
        self._clean_zeros()
        if not self._coeffs: return "0"

        terms=[] # для слагаемых
        # сортировка от большего к меньшему
        for p in sorted(self._coeffs.keys(), reverse=True):
            c = self._coeffs[p]
            # определеяем знак перед числом
            sign = " - " if c < 0 else " + "
            abs_c = abs(c)
            # если с=1 и степень не ноль, то коэфф-т пустой
            coeff_str = "" if abs_c == 1 and p!=0 else str(abs_c)

            if p==0: var_str = ""
            elif p==1: var_str = "x"
            else: var_str = f"x^{p}"
            # объединяем
            terms.append((sign, coeff_str + var_str))

        first_sign, first_val = terms[0]
        # у первого коэфф-а + уходит
        res = ("-" if first_sign == " - " else "") + first_val
        # ост-ые коэфф-ы со знаками
        for sign,val in terms[1:]:
            res += sign + val

        return res

    # проверяем на равенство
    def __eq__(self, other):
        self._clean_zeros()
        if isinstance(other,(int,float)):
            other = Polynomial(other)
        elif not isinstance(other,Polynomial):
            return False
        other._clean_zeros()
        return self._coeffs == other._coeffs


    def __add__(self,other):
        if isinstance(other,(int,float)):
            other = Polynomial(other)
        elif not isinstance(other,Polynomial):
            return NotImplemented

        res = Polynomial(self)
        for p,c in other._coeffs.items():
            # прибавляем коэфф-т с к имеющемуся коэфф-у той же степени в res
            res._coeffs[p] = res._coeffs.get(p,0) + c
        res._clean_zeros()
        return res

    def __radd__(self,other):
        # коммутативность, поэтому нечего тут расписывать (вспомнил дискру, окак)
        return self.__add__(other)

    # просто добавляем противоположные знаки к коэфф-ам
    def __neg__(self):
        res = Polynomial()
        for p in res._coeffs:
            res._coeffs[p] = -res._coeffs[p]
        return res


    def __sub__(self,other):
        if isinstance(other,(int,float)):
            other = Polynomial(other)
        elif not isinstance(other,Polynomial):
            return NotImplemented
        return self + (-other)  # так в принципе можно, чтобы не ломать мозги
                                # над новой функцией вычитания


    def __rsub__(self,other):
        return (-self) + other


    def __mul__(self,other):
        if isinstance(other,(int,float)):
            res = Polynomial()
            for p,c in self._coeffs.items():
                res._coeffs[p] = c * other    # коэфф-т умножаем на число int/float
            res._clean_zeros()
            return res

        if isinstance(other,Polynomial):
            res = Polynomial()
            for p1,c1 in self._coeffs.items():
                for p2,c2 in other._coeffs.items():
                    # степени при умножении суммируются, а коэфф-ы перемножаются
                    res._coeffs[p1 + p2] = res._coeffs.get(p1 + p2,0) + c1 * c2
            res._clean_zeros()
            return res

        return NotImplemented


    def __rmul__(self,other):
        return self.__mul__(other)

    # подставляем значение для подсчета
    def __call__(self,x):
        return sum(c*(x**p) for p,c in self._coeffs.items())


    def der(self,d=1):
        if d<0: raise ValueError("Порядок производной не может быть отрицательным")
        res = Polynomial(self)
        for i in range(d):
            new_coeffs={}    # для временных коэфф-ов производной
            for p,c in self._coeffs.items():
                if p>0:
                    new_coeffs[p-1] = c*p    # тема производная 11 класс :)
            res._coeffs = new_coeffs # обновляем коэфф-ы
            res._clean_zeros()
        return res


    def __iter__(self):
        self._clean_zeros()
        self._iter_pairs = sorted(self._coeffs.items())    #по возрастанию сортируем
        self._iter_idx = 0 #чтобы итерировалось с начала
        return self


    def __next__(self):
        if self._iter_idx >= len(self._iter_pairs): # если все перебрали, стопаемся
            raise StopIteration
        val = self._iter_pairs[self._iter_idx]
        self._iter_idx += 1
        return val

# здесь прогнал через ИИшку (print-ы)
# 1. Проверка создания разными способами
p_list = Polynomial([1, 2, 3])  # Список коэффициентов [c0, c1, c2]
p_dict = Polynomial({0: -3, 2: 1, 5: 4})  # Словарь {степень: коэффициент}
p_copy = Polynomial(p_dict)  # Копия существующего многочлена
p_args = Polynomial(0, 2, 0, 5)  # Через запятую: c0, c1, c2, c3
p_num = Polynomial(7)  # Одно число (константа)

# 2. Проверка отображения (__str__ и __repr__)
print("--- Проверка вывода ---")
print("str(p_list):", p_list)  # Ожидается: 3x^2 + 2x + 1
print("str(p_dict):", p_dict)  # Ожидается: 4x^5 + x^2 - 3
print("str(p_args):", p_args)  # Ожидается: 5x^3 + 2x
print(
    "repr:", repr(Polynomial(1, 2, 3, 0, 0, 0, 5, 0, 0))
)  # Ожидается: Polynomial [1, 2, 3, 0, 0, 0, 5]

# 3. Проверка арифметики (+, -, *) и работы с числами
print("\n--- Арифметика ---")
p1 = Polynomial([1, 2])  # 2x + 1
p2 = Polynomial([3, 1])  # x + 3

print("p1 + p2 =", p1 + p2)  # 3x + 4
print("p1 + 5  =", p1 + 5)  # 2x + 6
print("5 + p1  =", 5 + p1)  # 2x + 6
print("p1 - 1  =", p1 - 1)  # 2x
print("10 - p1 =", 10 - p1)  # -2x + 9
print("p1 * 2  =", p1 * 2)  # 4x + 2
print("p1 * p2 =", p1 * p2)  # (2x + 1)(x + 3) = 2x^2 + 7x + 3

# 4. Проверка вызова в точке __call__
print("\n--- Вычисление в точке ---")
poly = Polynomial(1, 2, 3)  # 3x^2 + 2x + 1
print("poly(1) =", poly(1))  # 3*(1^2) + 2*(1) + 1 = 6
print("poly(0) =", poly(0))  # 1

# 5. Проверка степени и производной
print("\n--- Степень и производная ---")
print("Степень poly:", poly.degree())  # 2
print("Первая производная:", poly.der(1))  # (3x^2 + 2x + 1)' = 6x + 2
print("Вторая производная:", poly.der(2))  # (6x + 2)' = 6

# 6. Проверка итератора
print("\n--- Итератор (степень, коэффициент) ---")
for power, coeff in poly:
  print(f"Степень: {power}, Коэффициент: {coeff}")