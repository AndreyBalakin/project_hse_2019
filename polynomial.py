class Polynomial:
    def __init__(self, *coefficients):
        if isinstance(coefficients[0], Polynomial):
            self.coefficients = coefficients[0].coefficients
        else:
            if len(coefficients) > 1:
                coeff_iter = coefficients
            elif isinstance(coefficients[0], int):
                coeff_iter = [coefficients[0], ]
            elif isinstance(coefficients[0], dict):
                coeff_iter = [0] * (max(coefficients[0]) + 1)
                for deg in coefficients[0]:
                    coeff_iter[deg] = coefficients[0][deg]
            else:
                coeff_iter = coefficients[0]
            max_deg = 0
            for i in range(len(coeff_iter)):
                if coeff_iter[i] != 0:
                    max_deg = i
            self.coefficients = list(coeff_iter)[:max_deg + 1]
        self.counter = 0


    def __repr__(self):
        return 'Polynomial ' + str(self.coefficients)


    def __str__(self):
        deg = self.degree()
        answer = '-' * int(self.coefficients[deg] < 0) + \
                 str(abs(self.coefficients[deg])) * int(abs(self.coefficients[deg]) != 1 or deg == 0) + \
                 'x' * int(deg > 0) + ('^' + str(deg)) * int(deg > 1)
        for i in range(2, deg + 2):
            if self.coefficients[-i] > 0:
                answer += ' + ' + str(self.coefficients[-i]) * int(self.coefficients[-i] != 1 or i == deg + 1) + \
                        'x' * int(deg > i - 1) + ('^' + str(deg - i + 1)) * int(deg > i)
            elif self.coefficients[-i] < 0:
                answer += ' - ' + str(-self.coefficients[-i]) * int(self.coefficients[-i] != -1 or i == deg + 1) + \
                          'x' * int(deg > i - 1) + ('^' + str(deg - i + 1)) * int(deg > i)
        return answer


    def degree(self):
        return len(self.coefficients) - 1


    def __eq__(self, other):
        return self.coefficients == Polynomial(other).coefficients


    def __add__(self, other):
        a = self
        b = Polynomial(other)
        coeff_list = [0] * max(a.degree() + 1, b.degree() + 1)
        for i in range(len(coeff_list)):
            if i <= a.degree():
                coeff_list[i] += a.coefficients[i]
            if i <= b.degree():
                coeff_list[i] += b.coefficients[i]
        return Polynomial(coeff_list)


    __radd__ = __add__


    def __neg__(self):
        return Polynomial(list(map(lambda x: -x, self.coefficients)))


    def __sub__(self, other):
        a = self
        b = Polynomial(other)
        coeff_list = [0] * max(a.degree() + 1, b.degree() + 1)
        for i in range(len(coeff_list)):
            if i <= a.degree():
                coeff_list[i] += a.coefficients[i]
            if i <= b.degree():
                coeff_list[i] -= b.coefficients[i]
        return Polynomial(coeff_list)


    def __rsub__(self, other):
        b = self
        a = Polynomial(other)
        coeff_list = [0] * max(a.degree() + 1, b.degree() + 1)
        for i in range(len(coeff_list)):
            if i <= a.degree():
                coeff_list[i] += a.coefficients[i]
            if i <= b.degree():
                coeff_list[i] -= b.coefficients[i]
        return Polynomial(coeff_list)


    def __call__(self, arg):
        answer = 0
        for i in range(self.degree() + 1):
            answer += self.coefficients[i] * arg**i
        return answer


    def __mul__(self, other):
        a = self
        b = Polynomial(other)
        m = a.degree()
        n = b.degree()
        coeff_list = [0] * (m + n + 1)
        for i in range(m + n + 1):
            for j in range(i + 1):
                if j <= m and i - j <= n:
                    coeff_list[i] += a.coefficients[j] * b.coefficients[i - j]
        return Polynomial(coeff_list)


    __rmul__ = __mul__


    def __mod__(self, other):
        a = self
        b = Polynomial(other)
        while a.degree() >= b.degree():
            a = b.coefficients[-1] * a - a.coefficients[-1] * Polynomial({a.degree() - b.degree(): 1}) * b
            if a == 0:
                break
        return a

    def __rmod__(self, other):
        b = self
        a = Polynomial(other)
        while a.degree() >= b.degree():
            a = b.coefficients[-1] * a - a.coefficients[-1] * Polynomial({a.degree() - b.degree(): 1}) * b
            if a == 0:
                break
        return a


    def gcd(self, other):
        a = self
        b = Polynomial(other)
        while a != 0 and b != 0:
            if a.degree() >= b.degree():
                a = a % b
            else:
                b = b % a
        return a + b


    def __iter__(self):
        return self


    def __next__(self):
        if self.counter <= self.degree():
            self.counter += 1
            return self.counter - 1, self.coefficients[self.counter - 1]
        else:
            raise StopIteration



class RealPolynomial(Polynomial):
    def find_root(self):
        a = 2 * max(map(lambda x: abs(x), self.coefficients))
        b = -a
        if self(a) > 0:
            a, b = b, a
        while abs(b - a) > 1e-6:
            if self((a + b) / 2) < 0:
                a = (a + b) / 2
            elif self((a + b) / 2) > 0:
                b = (a + b) / 2
            else:
                return (a + b) / 2
        return a



class QuadraticPolynomial(Polynomial):
    def solve(self):
        a = self.coefficients[2]
        b = self.coefficients[1]
        c = self.coefficients[0]
        d = b**2 - 4 * a * c
        if d < 0:
            return []
        elif d == 0:
            return [-b / (2 * a)]
        else:
            return sorted([(-b - d**(1 / 2)) / (2 * a), (-b + d**(1 / 2)) / (2 * a)])
