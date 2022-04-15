from pysmt.shortcuts import Symbol,substitute


class Unroller:
    def __init__(self,ts):
        self.ts_ = ts
        self.time_cache_ = []
        self.time_var_map_ = []
        self.untime_cache_ = {}
        self.var_times_ = {}
    

    def at_time(self,term,t):
        cache = self.var_cache_at_time(t)
        if term in cache:
            return cache[term]
        return substitute(term,cache)

    def var_cache_at_time(self,k):
        while len(self.time_cache_) <= k:
            self.time_cache_.append({})
            subset = self.time_cache_[-1]
            t = len(self.time_cache_) - 1
            for v in self.ts_.statevars_:
                vn = self.ts_.next(v)
                new_v = self.var_at_time(v,t)
                new_vn = self.var_at_time(v,t+1)
                subset[v] = new_v
                subset[vn] = new_vn
            
            for v in self.ts_.inputvars_:
                new_v = self.var_at_time(v,t)
                subset[v] = new_v
        return self.time_cache_[k]

    def var_at_time(self,v,k):
        while len(self.time_var_map_) <= k:
            self.time_var_map_.append({})
        cache = self.time_var_map_[k]
        if v in cache:
            return cache[v]
        
        name = v.symbol_name() + '@' + str(k)
        tv = Symbol(name,v.symbol_type())
        cache[v] = tv
        self.untime_cache_[tv] = v
        self.var_times_[tv] = k

        return tv
         


