from interface import *

############ motor class #####################

class motor(object):
	static = 0
	max = 1
	static_thrust = 1
	thrust_at_max = 1

	"""
	def thrust(self,v):
		return self.static_thrust + (self.thrust_at_max-self.static_thrust)*(v-self.static)/self.max
	"""
	def thrust(self,v):
		return self.thrust_at_max*self.max/v

############### flight dynamics class ######################

class dynamic(avl):
	# aircraft characteristics
	weight = 1
	extra_drag = 0		# D/q
	motor = motor()
	alpha_max = 10
	rolling_mu = 0
	stall_safety = 1.1

	# freestream conditions
	speed = 1
	rho = 1.225
	mu = 18.27 * 10**-6
	g = 9.80665

	# numerical computation parameters
	dv = 1
	dt = 0.005
	vtol = 1
	roll_max = None

	# unit names for printing
	length = "m"
	mass = "kg"
	force = "N"
	time = "s"
	temperature = "K"

	@property
	def cd0(self):
		c = 0
		for k in self.surfaces.keys():
			c += self.surfaces[k].integrated_cd0
		c /= self.area
		c += self.extra_drag
		return c

	@property
	def thrust(self):
		return self.motor.thrust(self.speed)

	@property
	def climb_cl(self):
		a = 0.25* self.rho**2 * self.speed**4 * self.area**2/(math.pi*self.ar*self.e)**2
		b = 0.25*self.rho**2 * self.speed**4 *self.area**2 *(1 + 2*self.cd0/(math.pi*self.ar*self.e))
		b -= self.thrust*self.rho* self.speed**2 * self.area / (math.pi*self.ar*self.e)
		c = self.thrust**2 + 0.25*self.rho**2 * self.speed**4 * self.area**2 * self.cd0**2
		c -=  self.weight**2 + self.thrust*self.rho*self.speed**2 * self.area*self.cd0
		l = math.sqrt( (-b + math.sqrt(b**2 - 4*a*c)) / (2*a) ) # ignore the extraneous solution where cl**2 < 0
		return l

	@property
	def slope(self):
		return (self.thrust - 0.5*self.rho*self.speed**2 *self.area * (self.cdi + self.cd0))/self.weight
	@property
	def roc(self):
		return self.slope*self.speed
		

	def climb_plot(self):
		v = list(range(30,150))
		vs,cl,slope,rate = [],[],[],[]
		for s in v:
			try:
				print(self.e)
				self.speed = s
				l = self.climb_cl
				self.set_attitude(cl=l)
				l = self.climb_cl
				print("cdi form",l**2/(math.pi*self.ar*self.e))
				self.set_attitude(cl=l)
				sl = self.slope
				print("cdi",self.cdi)
				print("cd0",self.cd0)
				slope.append(sl)
				rate.append(sl*self.speed)
				cl.append(l)
				vs.append(s)
			except:
				pass
		print(cl)
		print(vs)
		plt.plot(vs,cl,label="cl")
		plt.plot(vs,slope,label="slope")
		plt.plot(vs,rate,label="rate")
		plt.legend()

	def optimize_roc(self,fast=False,plot=False):
		"""
		Note to programmer: speed this up by only set_attitude 
		once per loop execution
		"""
		v0 = 0
		vs,rates=[],[]
		self.speed = self.v_stall
		self.set_attitude(alpha=0)
		while abs(self.speed - v0) > self.vtol:
			self.set_attitude(cl=self.climb_cl)
			if fast:
				slope = (self.thrust - 0.5*self.rho*self.speed**2 *self.area * (self.climb_cl**2/(math.pi*self.ar*self.e)+ self.cd0))/self.weight
				r0 = slope*self.speed
			else:
				r0 = self.roc
			v0 = self.speed
			self.speed += self.dv
			if fast:
				slope = (self.thrust - 0.5*self.rho*self.speed**2 *self.area * (self.climb_cl**2/(math.pi*self.ar*self.e)+ self.cd0))/self.weight
				r1 = slope*self.speed
			else:
				self.set_attitude(cl=self.climb_cl)
				r1 = self.roc
			v1 = self.speed
			self.speed += self.dv
			if fast:
				slope = (self.thrust - 0.5*self.rho*self.speed**2 *self.area * (self.climb_cl**2/(math.pi*self.ar*self.e)+ self.cd0))/self.weight
				r2 = slope*self.speed
			else:
				self.set_attitude(cl=self.climb_cl)
				r2 = self.roc
			v2 = self.speed
			coefs = np.polyfit([v0,v1,v2],[r0,r1,r2],2)
			if plot:
				vs.append(v0)
				rates.append(r0)
				testv = np.linspace(0,100,100)
				testr = testv**2*coefs[0] + testv*coefs[1] + coefs[2]
				plt.plot(testv,testr)
			self.speed = -0.5*coefs[1]/coefs[0]
		self.set_attitude(cl=self.climb_cl)
		if plot:
			plt.scatter(vs+[self.speed],rates+[self.roc])

	def climb_rate_analytic(self,iterations=1):
		self.speed = self.motor.max
		for n in range(iterations):
			self.set_attitude()
			P = self.thrust*self.speed
			e = self.e
			v = math.sqrt(2*self.weight/(self.rho*self.area*math.sqrt(math.pi*self.ar*e*3*self.cd0)))
			self.speed = v
			print(self.speed,self.alpha,self.slope)
		return P/self.weight - v*(0.5*self.rho*v**2*self.area*self.cd0/self.weight + self.weight*2/(self.area*self.rho*v**2*math.pi*self.ar*e))

	def set_attitude(self,cl=None,alpha=None,load_factor=1):
		if cl==None and (alpha==None):
			self.set_attitude(cl = math.sqrt(2*self.weight*load_factor/(self.rho*self.area*self.speed**2)))
		else:
			super().set_attitude(cl=cl,alpha=alpha)

	@property
	def v_stall(self):
		self.set_attitude(alpha=self.alpha_max)
		return math.sqrt(2*self.weight/(self.rho*self.cl*self.area))

	def takeoff_distance_analytic(self,alpha=0,lame=False):
		"""
		Normal mode tested against www.dept.aoe.vt.edu/~lutze/AOE3104/takeoff&landing.pdf, p6
		"""
		e = self.pitch_trim
		self.pitch_trim = None
		vto = self.v_stall*self.stall_safety
		self.set_attitude(alpha=alpha)
		self.speed = vto/math.sqrt(2)
		t = self.thrust
		if lame:
			return 0.5*vto**2/(self.g* (t/self.weight - self.rolling_mu - 0.25*self.rho*vto**2 /self.weight*self.area*(self.cd0 + self.cdi - self.rolling_mu*self.cl)) )
		a = self.g*(t/self.weight-self.rolling_mu)
		b = self.g/self.weight*(0.5*self.rho*self.area*(self.cd0 + self.cdi - self.rolling_mu*self.cl))
		self.pitch_trim = e
		try:
			return 0.5/b*math.log(a/(a - b*vto**2))
		except ValueError:
			return "Computation Failed -- probably insufficient thrust"

	def takeoff_distance(self,cl=None,alpha=0):
		v_to = self.v_stall*self.stall_safety
		e = self.pitch_trim
		self.pitch_trim = None
		if cl != None:
			self.set_attitude(cl=cl)
		elif alpha != None:
			self.set_attitude(alpha=alpha)
		self.speed = v_to
		if self.weight*self.rolling_mu > self.motor.static_thrust:
			return "Aircraft cannot roll -- insufficient thrust"
		if self.weight*(self.rolling_mu) + 0.5*self.rho*self.area*self.speed**2 * (self.cd0 + self.cdi - self.rolling_mu*self.cl) >= self.thrust:
			return "Aircraft cannot takeoff -- insufficient thrust at takeoff speed"
		self.speed = 0
		roll = 0
		while self.speed < v_to:
			roll += self.speed*self.dt
			force = (self.thrust - 0.5*self.rho*self.speed**2*self.area*(self.cd0 + self.cdi - self.rolling_mu*self.cl) - self.rolling_mu*self.weight)
			self.speed += force*self.g/self.weight*self.dt
			if (self.roll_max != None) and (roll > self.roll_max):
				return "Aircraft cannot takoff within {}".format(self.roll_max)
		self.pitch_trim = e
		return roll

	@property
	def v_max(self,plot=False):
		vs,excess_thrusts=[],[]
		self.speed = self.v_stall
		v0 = 0
		while abs(self.speed - v0) > self.vtol:
			self.set_attitude(cl=self.weight/(0.5*self.rho*self.area*self.speed**2))
			e = self.e
			cdi = self.weight**2/(math.pi*self.ar*self.e * (0.5*self.rho*self.speed**2*self.area)**2)
			excess_thrust0 = self.thrust - 0.5*self.rho*self.speed**2*self.area*(self.cd0 + cdi)
			v0 = self.speed
			self.speed += self.dv
			cdi = self.weight**2/(math.pi*self.ar*self.e * (0.5*self.rho*self.speed**2*self.area)**2)
			excess_thrust1 = self.thrust - 0.5*self.rho*self.speed**2*self.area*(self.cd0 + cdi)
			v1 = self.speed
			self.speed += self.dv
			cdi = self.weight**2/(math.pi*self.ar*self.e * (0.5*self.rho*self.speed**2*self.area)**2)
			excess_thrust2 = self.thrust - 0.5*self.rho*self.speed**2*self.area*(self.cd0 + cdi)
			v2 = self.speed
			coefs = np.polyfit([v0,v1,v2],[excess_thrust0,excess_thrust1,excess_thrust2],2)
			self.speed = (-coefs[1] - math.sqrt(coefs[1]**2 - 4*coefs[0]*coefs[2]))/(2*coefs[0])
			if plot:
				vs.append(v0)
				excess_thrusts.append(excess_thrust0)
				testv = np.linspace(0,200,100)
				testt = testv**2*coefs[0] + testv*coefs[1] + coefs[2]
				plt.plot(testv,testt)
		cdi = self.weight**2/(math.pi*self.ar*self.e * (0.5*self.rho*self.speed**2*self.area)**2)
		excess_thrust = self.thrust - 0.5*self.rho*self.speed**2*self.area*(self.cd0 + cdi)
		self.set_attitude(cl=self.weight/(0.5*self.rho*self.area*self.speed**2))
		if plot:
			plt.scatter(vs+[self.speed],excess_thrusts+[excess_thrust])
		return self.speed

	def print(self):
		print("Stall Speed:  {} {} / {}".format(self.v_stall,self.length,self.time))
		"""
		print("Top Speed:  {} {} / {}".format(self.v_max,self.length,self.time))
		print("Takeoff Roll Distance Analytic:  {} {}".format(self.takeoff_distance_analytic(),self.length))
		print("Takeoff Roll Distance:  {} {}".format(self.takeoff_distance(),self.length))
		"""
		print("Climb Rate Analytic: {} {} / {}".format(self.climb_rate_analytic(iterations=3),self.length,self.time))
		self.optimize_roc()
		print(self.speed,self.alpha,self.slope)
		print("Climb Rate:  {} {} / {}".format(self.roc,self.length,self.time))

class imperial_dynamic(dynamic):
	rho = 0.0023769
	mu = 0.3766*10**-6
	g = 32.17405

	length = "ft"
	mass = "slug"
	force = "lb"
	temperature = "R"

############ lifting line class ##########

class LiftingLine(object):

	def __init__(self,n=100, chord='elipse',scale=0.1,x=0,y = 'cos',z=0):

		if np.array_equal(y,'uniform'):
			selfy = np.linspace(0.5/n,1-0.5/n,n)
			self.elip = 2*np.sqrt(0.25-(selfy-0.5)**2)
		elif np.array_equal(y,'cos'):
			theta = np.linspace(0,math.pi,n+1)
			yvec = -np.cos(theta)/2
			self.elip = np.sin(np.linspace(0,math.pi,n))
			selfy = 0.5*(yvec[1:] + yvec[:-1]) + 0.5
		else:
			selfy = y
			self.elip = 2*np.sqrt(0.25-(selfy-0.5)**2)
			n = len(y)

		selfx = np.zeros(n) + x
		selfz = np.zeros(n) + z
		self.r = np.array([selfx,selfy,selfz])

		self.kappa = np.zeros(n)
		self.upwash= np.zeros(n)

		if np.array_equal(chord,'uniform'):
			self.chord = np.zeros(n) + scale
		elif np.array_equal(chord,'elipse'):
			self.chord = scale*np.sqrt(1-(2*self.r[1]-1)**2)
		else:
			self.chord = chord
		self.set_mesh()

	def set_mesh(self):
		r0,r1 = 2*self.r[:,-1] - self.r[:,-2], 2*self.r[:,0] - self.r[:,1]
		self.r_minus = (np.concatenate([np.array([r1]).transpose(), self.r[:,:-1]],1) + self.r)/2
		self.r_plus = (np.concatenate([self.r[:,1:], np.array([r0]).transpose()],1) + self.r)/2
		diff = self.r_plus - self.r_minus
		self.space = diff[1]
		self.arcspace = np.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)
		self.arclen = self.arcspace.sum()

	@property
	def ar(self):
		return 1/sum(self.chord*self.space)
	@property
	def area(self):
		return sum(self.chord*self.space)
	@property
	def cl(self):
		return -2*sum(self.kappa*self.space)/sum(self.chord*self.space)
	@property
	def cdi(self):
		return 2*sum(self.kappa*self.upwash*self.space)/sum(self.chord*self.space)
	@property
	def L(self):
		return -sum(self.kappa*self.space)
	@property
	def D(self):
		return sum(self.kappa*self.upwash*self.space)
	@property
	def e(self):
		return (self.cl**2)/(math.pi*self.ar*self.cdi)
	@property
	def lengthwise_e(self):
		return (2*self.L**2)/(math.pi*self.D*self.arclen**2)

	def vcoef(self,x,y,z):
		delta_y_plus,delta_z_plus = self.r_plus[1,:]-y,self.r_plus[2,:]-z
		delta_y_minus,delta_z_minus = self.r_minus[1,:]-y,self.r_minus[2,:]-z
		lat_dist_plus = np.sqrt(delta_y_plus**2 + delta_z_plus**2)
		lat_dist_minus = np.sqrt(delta_y_minus**2 + delta_z_minus**2)
		sweep_effect_plus = 2/math.pi*np.arctan( (x-self.r_plus[0,:])/lat_dist_plus) + 1
		sweep_effect_minus = 2/math.pi*np.arctan( (x-self.r_minus[0,:])/lat_dist_minus) + 1
		return (sweep_effect_plus*delta_y_plus/lat_dist_plus**2 - sweep_effect_minus*delta_y_minus/lat_dist_minus**2)/(4*math.pi)

	def solve(self,alpha):
		b = np.zeros(len(self.r[0]))+alpha
		x,y,z = np.array([self.r[0]]).transpose(),np.array([self.r[1]]).transpose(),np.array([self.r[2]]).transpose()
		vcoef = self.vcoef(x,y,z)
		eqns = -vcoef - np.identity(len(y))/(math.pi*self.chord)
		self.kappa = np.linalg.solve(eqns,b).flatten()
		self.upwash = np.dot( vcoef ,self.kappa)
	def solve_no_wash(self,alpha):
		b = np.zeros(len(self.r[0]))+alpha
		eqns = -np.identity(len(self.r[0]))/(math.pi*self.chord)
		self.kappa = np.linalg.solve(eqns,b).flatten()
		self.upwash *= 0

	def plot(self):
		n = len(self.space)
		plt.plot(self.r[1],self.kappa)
		elip = -self.elip*max(abs(self.kappa))
		plt.plot(self.r[1],elip)
		plt.plot(self.r[1],self.upwash)

	def plot_circ(self):
		circ = self.kappa/self.kappa.mean()
		plt.plot(self.y,circ)

	def plot_wash(self):
		wash = self.upwash/self.upwash.min()
		plt.plot(self.y,wash)

	def plot_planform(self):
		plt.axis('equal')
		plt.scatter(self.r[0],self.r[1],color='k')
		plt.scatter(self.r_plus[0],self.r_plus[1],color='r')
		plt.scatter(self.r_minus[0],self.r_minus[1],color='r')
		plt.plot(self.r[0]+0.75*self.chord,self.r[1],color='b')
		plt.plot(self.r[0]-0.25*self.chord,self.r[1],color='b')

	def print(self):
		n = len(self.space)
		print("cl",self.cl,"cdi",self.cdi)
		print("ar",self.ar)
		print("e",self.e)
		print()
		wash = self.upwash[int(n/2)]
		print("wash",wash,'alpha',2*math.pi/180,"cdi/cl",self.cdi/self.cl)
		alpha500 = 2*math.pi/180 + wash
		print("correct",math.pi*self.chord[50]*alpha500, "actual", self.kappa[int(n/2)] )

