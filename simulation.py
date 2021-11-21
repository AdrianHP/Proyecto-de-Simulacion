from queue import Queue

class Simulation:
    def __init__(self, agen, sushitimegen, sandwichtimegen, typegen, duration, maxn, working):
        self.agen = agen 
        self.sushitimegen = sushitimegen 
        self.sandwichtimegen = sandwichtimegen 
        self.typegen = typegen 
        self.working = working 
        self.maxn = maxn 

        self.ta = agen() 
        self.th = [duration + self.ta] * self.maxn
        self.oth = [False] * self.maxn
        self.t = 0
        self.T = duration 
        
        self.queue = Queue() 
        
        self.Na = 0
        self.Nd = 0 

        self.late_n = 0

    def gen_order_time(self):
        return self.sushitimegen() if self.typegen() else self.sandwichtimegen()

    def advance(self):
        event = min(self.ta, *self.th)
        self.time = event
        current_workers = self.working(self.time)
        assert current_workers <= self.maxn, "No pueden trabajar mas empleados que la cantidad maxima"
        if event == self.ta: 
            if event <= self.T:
                self.Na += 1
                self.ta = self.time + self.agen()
                for i in range(current_workers):
                    if not self.oth[i]: 
                        self.th[i] = self.time + self.gen_order_time()
                        self.oth[i] = True
                        return True
             
                self.queue.put_nowait(event)
                return True
            else:
                self.ta = max(*self.th) + 1
                return any(self.oth) 
        for i in range(self.maxn):
            if event == self.th[i]: 
                self.Na -= 1
                self.Nd += 1    
                if not self.queue.empty() and i < current_workers: 
                    arrival = self.queue.get_nowait()
                    elapsed = event - arrival
                    self.late_n += (1 if elapsed > 5 else 0)
                    self.th[i] = self.time + self.gen_order_time()
                else: 
                    self.th[i] = self.T + self.ta 
                    self.oth[i] = False
                return True
        return False 
