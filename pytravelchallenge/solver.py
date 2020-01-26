"""This module contains the classes of some common Optimization solvers.
There are all instances of the abstract class `AbstractSolver', so that
they have the same interface.

Author: Arnold N'GORAN (arnoldngoran at gmail.com)
Date:   24/01/2020
"""
#import gurobipy as grb
import numpy as np
import pyscipopt as scip

from .abstract_solver import AbstractSolver


"""
class GRB(AbstractSolver):
    "The Gurobi solver"
    name = 'Gurobi'
    PLUS_INFINITY = grb.GRB.INFINITY
    MINUS_INFINITY = -grb.GRB.INFINITY
    BINARY = grb.GRB.BINARY
    MAX = grb.GRB.MAXIMIZE
    MIN = grb.GRB.MINIMIZE
    CLS = grb
    STATUS = grb.GRB.Status
    STATUS_INF_OR_UNBD = grb.GRB.Status.INF_OR_UNBD

    def __init__(self, problem_name='lp_prob'):
        self.nodecount = None
        self.objval = None
        self.isMIP = None
        self.m = GRB.CLS.Model(problem_name)
    
    def optimize(self):
        self.m.optimize()
        self.isMIP = self.m.IsMIP

    def add_constr(self, constr, **params):
        self.m.addConstr(constr, **params)

    def add_var(self, **params):
        return self.m.addVar(**params)

    def set_objective(self, func, sense='max', **params):
        if sense == 'max':
            sense = self.MAX
        elif sense == 'min':
            sense = self.MIN
        else:
            raise Exception('GUROBI:: Invalid optimization SENSE !!')
        self.m.setObjective(func, sense)

    def get_var_by_name(self, name):
        return self.m.getVarByName(name).X

    def get_vars(self):
        return self.m.getVars()

    def get_optimum_value(self):
        self.objval = self.m.objval
        return self.objval

    def get_param(self, name):
        return self.m.__getattribute__(name)

    def set_param(self, name, value):
        self.m.setParam(name, value)

    def get_status(self):
        return self.m.status

    def quicksum(self, expr):
        return GRB.CLS.quicksum(expr)

    def update(self):
        self.m.update()     
"""

class SCIP(AbstractSolver):
    """The SCIP solver"""
    name = 'SCIP'
    PLUS_INFINITY = MINUS_INFINITY = None
    BINARY = 'B'
    CONTINOUS = 'C'
    INTEGER = 'I'
    MIN = 'minimize'
    MAX = 'maximize'
    CLS = scip
    STATUS = scip.scip.PY_SCIP_STATUS
    STATUS_INF_OR_UNBD = scip.scip.PY_SCIP_STATUS.INFORUNBD

    def __init__(self, problem_name='lp_prob'):
        self.objval = None
        self.isMIP = None
        self.nodecount = None
        self.opt_vars = None
        self.m = self.CLS.Model(problem_name)

    def add_constr(self, constr, **params):
        self.m.addCons(constr, **params)

    def add_var(self, **params):
        return self.m.addVar(**params)

    def set_objective(self, func, sense='max', **params):
        if sense == 'max':
            sense = self.MAX
        elif sense == 'min':
            sense = self.MIN
        else:
            raise Exception('SCIP:: Invalid optimization SENSE !!')
        self.m.setObjective(func, sense)

    def optimize(self):
        self.m.optimize()
        self.isMIP = None   # To be defined
        ## Necessary because SCIP does not a function to retrieve
        # variables by their `name'. This is quite strange that SCIP does not provide a better interface
        self.opt_vars = {str(v):v for v in self.m.getVars()}

    def get_optimum_value(self):
        self.objval = self.m.objVal
        return self.objval

    def get_var_by_name(self, name):
        return self.m.getVal(self.opt_vars[name])

    def get_vars(self):
        return self.m.getVars()

    def get_param(self, name):
        return self.m.__getattribute__(name)

    def set_param(self, name, value):
        self.m.setParam(name, value)

    def get_status(self):
        return self.m.getStatus()

    def quicksum(self,expr):
        return SCIP.CLS.quicksum(expr)
        #return np.sum(expr)

    def update(self):
        print('**** WARNING: Function UPDATE not implemented.')
        pass
