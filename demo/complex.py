class complex:
    """A toy partial complex number implementation. Uses method and
    operator overloading and multiple dispatch."""

    def __init__(self, float re, im=0):
        self.re = re
        self.im = im

    def __init__(self, complex n):
        self.__init__(n.re, n.im)

    def __str__(self):
        if self.im >= 0:
            return "({} + {}j)".format(self.re, self.im)
        else:
            return "({} - {}j)".format(self.re, -self.im)

    # Use multiple dispath for __eq__.

    def __eq__(self, n): # Default __eq__ overload
        return False

    def __eq__(self, complex n):
        return self.re == c.re and self.im == c.im

    def __eq__(self, float n):
        return self.re == n and self.im == 0

    def __hash__(self):
        if self.im:
            return hash((self.re, self.im))
        else:
            return hash(self.re)            

    def __add__(self, complex n):
        return complex(self.re + n.re, self.im + n.im)
    
    def __add__(self, float n):
        return self + complex(n)

    def __mul__(self, complex n):
        return complex(self.re * n.re - self.im * n.im,
                       self.im * n.re + self.re * n.im)

    def __mul__(self, float n):
        return self * complex(n)
