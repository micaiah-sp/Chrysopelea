import math
import numpy as np
import matplotlib.pyplot as plt

class preliminary(object):

	e = 1
	rho = 0.0023769
	g = 32.17405

	ar = 8.7
	e = 0.8
	cd0 = 0.06
	mu = 0.025
	stall_safety = 1.1
	cl_max = 1.6

	v_max = None
	to = None
	roc = None

	constraints = []

	wing_loading = np.linspace(0,6,200)
	power_limit = 30

	def size(self,to_watt=True):

		v_stall = np.sqrt(2*self.wing_loading/(self.rho*self.cl_max))
	
		if to_watt:
			f = 1/0.74
			plt.ylabel("Power per Unit Weight: Watt / lb")
		else:
			f = 1
			plt.ylabel("Power per Unit Weight: ft / s")
		if self.v_max != None:
			pow_vmax = 0.5*self.rho*self.v_max**3/self.wing_loading
			pow_vmax *= self.cd0 + self.wing_loading**2/(math.pi*self.ar*self.e*(0.5*self.rho*self.v_max**2)**2)
			pow_vmax *= f
			plt.plot(self.wing_loading,pow_vmax,label='V_max = {}'.format(self.v_max))
			self.constraints.append(pow_vmax)

		if self.to != None:
			vto = self.stall_safety*v_stall
			vbar = vto/math.sqrt(2)
			#pow_to = (vto**2/(2*self.g*self.to) + self.mu + 0.5*self.rho*vbar**2*self.cd0)*vbar
			pow_to = vto**2/(2*self.g*self.to)*vbar
			pow_to *= f
			plt.plot(self.wing_loading,pow_to,label='TO Distance = {}'.format(self.to))
			self.constraints.append(pow_to)

		if self.roc != None:
			v_climb_opt = np.sqrt(2*self.wing_loading/self.rho/np.sqrt(3*self.cd0*math.pi*self.ar*self.e))
			v_climb = np.max(np.array([v_climb_opt,v_stall*self.stall_safety]),0)
			pow_roc = self.roc + 0.5*self.rho*v_climb**3/self.wing_loading*self.cd0 + self.wing_loading/(math.pi*self.ar*self.e*0.5*self.rho*v_climb)
			pow_roc *= f
			plt.plot(self.wing_loading,pow_roc,label='ROC = {}'.format(self.roc))
			self.constraints.append(pow_roc)

		bound = np.max(np.array(self.constraints),0)
		m = np.nanmin(bound)
		ind = (bound==m).nonzero()

		plt.ylim(0,self.power_limit)
		plt.xlabel("Wing Loading: lb / ft^2")
		plt.legend()
		plt.title("Energy-Based Constraint Diagram")

		plt.scatter(self.wing_loading[ind],m,color="r")
		return self.wing_loading[ind],m

	def speed(self):
			v_climb = np.sqrt(2*self.wing_loading/self.rho/np.sqrt(3*self.cd0*math.pi*self.ar*self.e))
			plt.plot(self.wing_loading,v_climb,label="v_climb")
			v_stall = np.sqrt(2*self.wing_loading/(self.rho*self.cl_max))
			plt.plot(self.wing_loading,v_stall,label="v_stall")
			vto = self.stall_safety*v_stall
			plt.plot(self.wing_loading,vto,label="vto")
			plt.legend()
			plt.show()


