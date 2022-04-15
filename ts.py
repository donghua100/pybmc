from pysmt.shortcuts import Symbol,TRUE,And,Equals
from pysmt.shortcuts import BVType,Ite,LT,Plus,Int,BV,BVULT,BVAdd,Equals

class TransitionSystem:
    def __init__(self):
        self.init_ = TRUE()
        self.trans_ = TRUE()
        self.statevars_ = set()
        self.next_statevars_ = set()
        self.inputvars_ = set()

        self.state_update_ = dict()
        self.next_map_ = dict()
        self.curr_map_ = dict()

    def make_inputvar(self,name,sort):
        inputvar = Symbol(name,sort)
        if inputvar in self.statevars_ or inputvar in self.inputvars_ or inputvar in self.next_statevars_:
            print("Cannot reuse an existing variable as an input variable") 
        self.inputvars_.add(inputvar)
        return inputvar

    def make_statevar(self,name,sort):
        state = Symbol(name,sort)
        next_state = Symbol(name+'.next',sort)
        if state in self.statevars_:
            raise Exception("Cannot redeclare a state variable")
        
        if next_state in self.next_statevars_:
            raise Exception("Cantnot redeclare a next state variable")

        if state in self.next_statevars_:
            raise Exception("Cannot reuse a next state variable as state")

        if next_state in self.statevars_:
            raise Exception("Cannot reuse a state variable as next state")

        if state in self.inputvars_:
            self.inputvars_.remove(state)
        
        if next_state in self.inputvars_:
            self.inputvars_.remove(state)

        self.statevars_.add(state)
        self.next_statevars_.add(next_state)
        self.next_map_[state] = next_state
        self.curr_map_[next_state] = state
        return state
    

    def assign_next(self,state,val):

        if state not in self.statevars_:
            raise Exception("the state is unkoown")

        self.state_update_[state] = val
        self.trans_ = And(self.trans_,Equals(self.next_map_[state],val))


    def next(self,term):
        if  term in self.next_map_:
            return self.next_map_[term]
        else:
            raise Exception('the term has no next')

    def set_init(self,init):
        self.init_ = init    

        
if __name__ == '__main__':
    ts = TransitionSystem()
    width = 3
    bv3 = BVType(width)
    in_ = ts.make_inputvar("in",bv3)
    internal = ts.make_statevar("internal",bv3)
    val = Ite(BVULT(internal,BV(2**width-1,width)),BVAdd(internal,BV(1,width)),BV(0,width))
    ts.assign_next(internal,val)
    ts.set_init(Equals(internal,BV(0,width)))
    print(ts.init_)
    print(ts.trans_)


