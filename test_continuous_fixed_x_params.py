"""
	Copyright (c) 2013, Los Alamos National Security, LLC
	All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
	following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
	  disclaimer.
	* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
	  following disclaimer in the documentation and/or other materials provided with the distribution.
	* Neither the name of Los Alamos National Security, LLC nor the names of its contributors may be used to endorse or
	  promote products derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
	INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
	WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from objective_function_interface import ObjectiveFunctionInterface
from math import pow
import random
from multiprocessing import cpu_count

#define all input parameters
maximize = True #do we maximize or minimize?
max_imp = 50000 #maximum number of improvisations
hms = 100 #harmony memory size
hmcr = 0.75 #harmony memory considering rate
par = 0.5 #pitch adjusting rate
mpap = 0.25 #maximum pitch adjustment proportion (new parameter defined in pitch_adjustment()) - used for continuous variables only
mpai = 2 #maximum pitch adjustment index (also defined in pitch_adjustment()) - used for discrete variables only

num_processes = cpu_count() #use number of logical CPUs (on my i7, this is 8)
num_iterations = num_processes * 5 #each CPU does 5 iterations (on my machine, we do 40 total iterations)

class TestContinuousFixedXObjectiveFunction(ObjectiveFunctionInterface):
	"""
		This is a toy objective function that contains only continuous variables. Here, variable x is fixed at 0.5.

		Goal:

			maximize -(x^2 + (y+1)^2) + 4
			The maximum is 4 at (0, -1). However, when x is fixed at 0.5, the maximum is 3.75 at (0.5, -1).

		Note that since all variables are continuous, we don't actually need to implement get_index()
		and get_num_discrete_values().
	"""

	def __init__(self):
		self.lower_bounds = [-1000, -1000]
		self.upper_bounds = [1000, 1000]
		self.variable = [False, True]

	def fitness(self, vector):
		"""
			maximize -(x^2 + (y+1)^2) + 4
			The maximum is 3.75 at (0.5, -1) (remember that x is fixed at 0.5 here).
		"""
		return -(pow(vector[0], 2) + pow(vector[1] + 1, 2)) + 4

	def get_value(self, i, index=None):
		"""
			Values are returned uniformly at random in their entire range. Since both parameters are continuous, index can be ignored.

			Note that parameter x is fixed (i.e., self.variable[0] == False). We return 0.5 for that parameter.
		"""
		if i == 0:
			return 0.5
		return random.uniform(self.lower_bounds[i], self.upper_bounds[i])

	def lower_bound(self, i):
		return self.lower_bounds[i]
	
	def upper_bound(self, i):
		return self.upper_bounds[i]
	
	def is_variable(self, i):
		return self.variable[i]
	
	def is_discrete(self, i):
		#all variables are continuous
		return False
	
	def get_num_parameters(self):
		return len(self.lower_bounds)
