class complex:
    """A toy partial complex number implementation. Uses method and
    operator overloading and multiple dispatch."""

    void __init__(self, float re, float im=0):
        self.re = re
        self.im = im

    void __init__(self, complex n):
        self.__init__(n.re, n.im)

    str __str__(self):
        if self.im >= 0:
            return "({} + {}j)".format(self.re, self.im)
        else:
            return "({} - {}j)".format(self.re, -self.im)

    # Use multiple dispath for __eq__.

    bool __eq__(self, object n): # Default __eq__ overload
        return False

    bool __eq__(self, complex n):
        return self.re == c.re and self.im == c.im

    bool __eq__(self, float n):
        return self.re == n and self.im == 0

    int __hash__(self):
        if self.im:
            return hash((self.re, self.im))
        else:
            return hash(self.re)            

    complex __add__(self, complex n):
        return complex(self.re + n.re, self.im + n.im)
    
    complex __add__(self, float n):
        return self + complex(n)

    complex __mul__(self, complex n):
        return complex(self.re * n.re - self.im * n.im,
                       self.im * n.re + self.re * n.im)

    complex __mul__(self, float n):
        return self * complex(n)
