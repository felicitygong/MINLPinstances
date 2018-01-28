from pyomo.environ import *

model = m = ConcreteModel()

m.x1 = Var(within=NonNegativeReals,bounds=(0,2),initialize=0)
m.x2 = Var(within=NonNegativeReals,bounds=(0,2),initialize=0)
m.x3 = Var(within=NonNegativeReals,bounds=(0,1),initialize=0)
m.x4 = Var(within=NonNegativeReals,bounds=(0,100),initialize=0)
m.y1 = Var(within=Binary,bounds=(0,1),initialize=0)
m.y2 = Var(within=Binary,bounds=(0,1),initialize=0)
m.y3 = Var(within=Binary,bounds=(0,1),initialize=0)

m.obj = Objective(expr=m.x4 + 5*m.y1 + 6*m.y2 + 8*m.y3, sense=minimize)

m.c1 = Constraint(expr=   -m.x1 + m.x2 <= 0)

m.c2 = Constraint(expr=   m.x3 - 2*m.y1 <= 0)

m.c3 = Constraint(expr=   m.x1 - 2*m.y2 <= 0)

m.c4 = Constraint(expr=   m.y1 + m.y2 <= 1)

m.c5 = Constraint(expr=   -0.8*log(m.x2 + 1) - 0.9*log(m.x1 - m.x2 + 1) + 0.8*m.x3 <= 0)

m.c6 = Constraint(expr=   -log(m.x2 + 1) - 1.2*log(m.x1 - m.x2 + 1) + m.x3 + 2*m.y3 - 2 <= 0)

m.c7 = Constraint(expr=   10*m.x1 - 7*m.x3 - 18*log(m.x2 + 1) - 19.2*log(m.x1 - m.x2 + 1) + 10 - m.x4 <= 0)