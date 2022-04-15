import smt_switch as ss


from pysmt import shortcuts
from pysmt.shortcuts import Symbol,And,LE,INT,Int,BVType,BV,BVULE
from pysmt.walkers import TreeWalker

varA=Symbol("A")
print(varA.symbol_name())

bv3 = BVType(3)
varB=Symbol("B",bv3)
print(varA==varB)
f = And(varA,BVULE(varB,BV(3,3)))
x = f.get_free_variables()

print(x)
