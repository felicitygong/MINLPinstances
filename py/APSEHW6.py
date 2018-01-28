from pyomo.environ import *

model = m = ConcreteModel()

m.x1 = Var(within=Reals, bounds=(0,4), initialize=0)
m.x2 = Var(within=Reals, bounds=(0,4), initialize=0)
m.y1 = Var(within=Binary, bounds=(0,1), initialize=1)
m.y2 = Var(within=Binary, bounds=(0,1), initialize=1)
m.y3 = Var(within=Binary, bounds=(0,1), initialize=1)

m.obj = Objective(expr= m.y1 + 1.5 * m.y2 + 0.5 * m.y3 + m.x1**2 + m.x2**2)

m.c1 = Constraint(expr=    (m.x1 - 2)**2 - m.x2 <= 0)
m.c2 = Constraint(expr=    m.x1 - 2*m.y1 >= 0)
m.c3 = Constraint(expr=    m.x1 - m.x2 - 4*(1 - m.y2) <= 0)
m.c4 = Constraint(expr=    m.x1 - (1-m.y1) >= 0)
m.c5 = Constraint(expr=    m.x2 - m.y2 >= 0)
m.c6 = Constraint(expr=    m.x1 + m.x2 >= 3*m.y3)
m.c7 = Constraint(expr=    m.y1 + m.y2 + m.y3 >= 1)