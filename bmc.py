from pysmt.shortcuts import And,is_sat,BVType,BV,Ite,BVULT,BVAdd,Equals,Not
from ts import TransitionSystem
from unroller import Unroller


class Bmc:
    def __init__(self,ts,unroller,bad):
        self.ts_ = ts
        self.unroller_ = unroller
        self.bad_ = bad
        self.reached_k = -1
        self.f = None

    def check_until(self,k):
        self.f = self.unroller_.at_time(self.ts_.init_,0)        
        for i in range(self.reached_k+1,k+1):
            if not self.step(i):
                return 0
        return -1
    
    def step(self,i):
        if i > 0:
            self.f = And(self.f,self.unroller_.at_time(self.ts_.trans_,i-1))
        print("Checking bmc at bound: {}".format(i))
        if is_sat(And(self.f,self.unroller_.at_time(self.bad_,i))):
            return False
        return True


if __name__ == '__main__':
    ts = TransitionSystem()
    width = 3
    bv3 = BVType(width)
    in_ = ts.make_inputvar("in",bv3)
    internal = ts.make_statevar("internal",bv3)
    val = Ite(BVULT(internal,BV(2**width-1,width)),BVAdd(internal,BV(1,width)),BV(0,width))
    ts.assign_next(internal,val)
    ts.set_init(Equals(internal,BV(0,width)))
    bad=Not(BVULT(internal,BV(5,width)))
    print(ts.init_)
    print(ts.trans_)

    unroller = Unroller(ts)

    bmc = Bmc(ts,unroller,bad)
    res = bmc.check_until(10)
    print(res)