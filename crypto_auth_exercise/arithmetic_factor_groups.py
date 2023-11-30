from math import gcd
from matplotlib import pyplot as plt

# the class represents the multiplicative group of integers modulo n, i.e., (Z/nZ)^*
class ModNMultGroup:
    def __init__(self, modulus: int) -> None:
        self.modulus = modulus
        self.members = self.group_members()
        self.mult_table = self.multiplication_table()

    # calculates the members of (Z/nZ)^*
    def group_members(self) -> list[int]:
        return [x for x in range(1,self.modulus) if gcd(x,self.modulus) == 1]

    # calculates either a list of lists (one row and one column per element of the group, 
    # in row x, column y the product of x and y is written)
    # or (instead of the list of lists) a dictionary with the elements of the group as keys and the list
    # of products with the other elements as values
    def multiplication_table(self) -> dict[list[int]]:
        mult_table = {}
        for i in self.members:
            mults = []
            for j in self.members:
                mults.append((i*j)%self.modulus)
                mult_table[i] = mults

        return mult_table

    # look up in the multiplication table to calculate the product of x and y
    def fast_mult(self, x: int, y: int) -> int:
        if x%self.modulus not in self.members or y%self.modulus not in self.members:
            raise Exception("Elements not in group")
        x = x%self.modulus
        y = y%self.modulus
        right_index = self.members.index(y)
        return self.mult_table[x][right_index]

    # calculate phi(modulus)
    def eulerphi(self) -> int:
        return len(self.members)

    # calculate the inverse of x in (Z/nZ)^*
    def inverse(self, x: int) -> int:
        x = x%self.modulus
        if x not in self.members:
            raise Exception("Element not in group")
        right_index = self.mult_table[x].index(1)
        return self.members[right_index]

    # calculate g^n in (Z/nZ)^*
    def power(self, g: int, n: int) -> int:
        n = n%self.modulus
        if n<0:
            self.inverse(self.power(g,-n))
        if n == 0:
            return 1
        return self.fast_mult(self.power(g, n-1), g)

    # calculate all powers of x in (Z/nZ)^*
    def powers(self, g: int) -> list[int]:
        return [self.power(g,i) for i in range(0, self.eulerphi()+1)]

    # calculate all powers of all elements of (Z/nZ)^*
    def all_powers(self) -> dict[list[int]]:
        result = {}
        for g in self.members:
            values = self.powers(g)
            result[g] = values
        return result

    def is_primitive_root(self, g: int):
        return set(self.powers(g)) == set(self.members)
    
    def all_primitive_roots(self):
        return [x for x in self.members if self.is_primitive_root(x)]
    # do a scatter plot that shows all powers n^i in (Z/nZ)^* 
    def plot_powers(self, g: int):
        args = list(range(0,self.eulerphi()+1))
        values = self.powers(g)
        plt.scatter(args, values)
        plt.show()


if __name__ == '__main__':
    grp = ModNMultGroup(125)
    
    #print(grp.multiplication_table())
    #print(grp.power(3,5))
    #print(grp.eulerphi())
    prim_roots = grp.all_primitive_roots()
    print([x for x in grp.members if x not in prim_roots])
    grp.plot_powers(4)