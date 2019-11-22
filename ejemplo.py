import numpy as np
import matplotlib.pyplot as plt
import math
from numpy.linalg import inv
from tkinter import *

def print_table(XY_values, table_name):
	root = Tk()
	root.title(table_name)

	entry = Entry(root)
	entry.grid(row=0, column=0)
	entry.insert(0, "T")

	entry = Entry(root)
	entry.grid(row=0, column=1)
	entry.insert(0, "X")

	entry = Entry(root)
	entry.grid(row=0, column=2)
	entry.insert(0, "Y")

	entry = Entry(root)
	entry.grid(row=0, column=3)
	entry.insert(0, "X'")

	entry = Entry(root)
	entry.grid(row=0, column=4)
	entry.insert(0, "Y'")

	for i in range(len(XY_values)):
		for j in range(5):
			entry = Entry(root)
			entry.grid(row=i+1, column=j)
			if j == 0:
				entry.insert(0, str(i+1))
			if j == 1:
				entry.insert(0, str(XY_values[i][0]))
			if j == 2:
				entry.insert(0, str(XY_values[i][1]))
			if j == 3:
				 entry.insert(0, str(XY_values[i][2]))
			if j == 4:
				 entry.insert(0, str(XY_values[i][3]))

t=25
Pred=[]
Real=[]
Filt=[]
EspX=[]
EspY=[]
mu=0
x=10
y=10
vxInit=1
vyInit=1
sigmaV=100
sigmaP=100

"""------------------------------------------------"""
"""W es manual Q np.random.normal
	v es manual R np.random.normal
	I es matriz identidad
	repetir N veces"""
W=np.array(
	[
		[np.random.normal(mu,sigmaP)],
		[np.random.normal(mu,sigmaP)],
		[np.random.normal(mu,sigmaV)],
		[np.random.normal(mu,sigmaV)]
	]
)
V=np.array(
	[
		[np.random.normal(mu,sigmaV)],
		[np.random.normal(mu,sigmaV)]
	]
) # Ya
Xr=np.array(
	[
		[x],
		[y],
		[vxInit],
		[vyInit]
	]
)

"""
Faltantes ----------------------------------------------------------------------------
"""
X=np.array([[x],[y],[vxInit],[vyInit]])+W
Q=np.array([[sigmaP**2,0,0,0],[0,sigmaP**2,0,0],[0,0,sigmaV**2,0],[0,0,0,sigmaV**2]])
P=np.array([[sigmaP,0,0,0],[0,sigmaP,0,0],[0,0,sigmaV,0],[0,0,0,sigmaV]])

"""
--------------------------------------------------------------------------------------
"""

F=np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]) # YA

Ft=np.transpose(F) # Ya
I=np.array(
	[
		[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]
	]
) # Ya

H=np.array(
	[
		[1,0,0,0],
		[0,1,0,0]
	]
) # Ya
R=np.array([[sigmaP*1.2,0],[0,sigmaP*1.2]]) # Ya

"""------------------------------------------------"""
xReal=[]
yReal=[]
xReal.append(x)
yReal.append(y)
for x in range(t):
	xReal.append(xReal[-1]+vxInit)
	yReal.append(yReal[-1]+vyInit)
for x in range(t):
	W=np.array([[np.random.normal(mu,sigmaP)],[np.random.normal(mu,sigmaP)],[np.random.normal(mu,sigmaV)],[np.random.normal(mu,sigmaV)]])
	V=np.array([[np.random.normal(mu,sigmaV)],[np.random.normal(mu,sigmaV)]])
	Xr=np.dot(F,Xr)+W
	EspX.append(Xr)
	Z=np.dot(H,Xr)+V    
	X=np.dot(F,X)
	Pred.append(X)      
	P=np.dot(F,np.dot(P,Ft))+Q
	K=np.dot(P,np.dot(np.transpose(H),inv(np.dot(H,np.dot(P,np.transpose(H)))+R)))
	Y=Z-np.dot(H,X)
	X=X+np.dot(K,Y)
	Filt.append(X)
	P=np.dot(P,(I-np.dot(K,H)))  

x=[]
y=[]
x2=[]
y2=[]
for i in range(len(EspX)):
	print(EspX[i][0],"-",EspX[i][0])
	x2.append(EspX[i][0])
	y2.append(EspX[i][1])
print("-----------------------------------------")
for i in range(len(Pred)):
	print(Pred[i][0],"-",Pred[i][1],"-",Pred[i][2],"-",Pred[i][3])
	x.append(Pred[i][0])
	y.append(Pred[i][1])
print("-----------------------------------------")
x1=[]
y1=[]
for i in range(len(Filt)):
	print(Filt[i][0],"-",Filt[i][1],"-",Filt[i][2],"-",Filt[i][3])
	x1.append(Filt[i][0])
	y1.append(Filt[i][1])
plt.plot(xReal,yReal,"-",label="Esperada")	# Esta es la linea perfecta
plt.plot(x2,y2,"-",label="Real")	# Esta es la linea que ocurre en la vida real
plt.plot(x,y,"-", label="Predicha")	# Es una preducción pero muy alejada de la real
plt.plot(x1,y1,"-", label="Filtrada")	# Esta tambien es una prediccion pero más cercana
# print_table(EspX, 'Real')
# print_table(Pred, 'Predicha')
# print_table(Filt, 'Filtrada')
plt.legend()
plt.show()


