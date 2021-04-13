import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.constants as const
from scipy.stats import sem
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)

a1, b1             = np.genfromtxt('Reflexion.dat', unpack=True)
a2, b2             = np.genfromtxt('Brechung1.dat', unpack=True)
a3, b3             = np.genfromtxt('Brechung2.dat', unpack=True)
a4g, b4g, a4r, a4r = np.genfromtxt('Prisma.dat', unpack=True)

############################################################################################################
#Aufgabe1
plt.figure()
x=np.linspace(np.min(a1), np.max(a1))
params,covariance_matrix=np.polyfit(a1, b1, deg=1, cov=True)
plt.plot(x, gerade(x, *params), "k", label="Regression")
plt.plot(a1 ,b1, '.', label='Messdaten')
plt.xlabel(r"$\alpha_1$")
plt.ylabel(r"$\alpha_2$")
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('plot1.pdf')

i         = 0
h         = ufloat(0,0)
paramserr1 = np.array([h, h])
errors    = np.sqrt(np.diag(covariance_matrix))
for name, value, error in zip('ab', params, errors):
    paramserr1[i]=ufloat(value, error)
    print(f'{name} = {value:.8f} ± {error:.8f}')
    i     = i+1

############################################################################################################
#Aufgabe2
n   =  np.sin(a2)/np.sin(b2) #n berechnen
nm  =  np.mean(n)
nf  =  np.sem(n)
nu  =  ufloat(nf,nf)
nit =  1.4931 #vergleichen mit Literatur
p   =  100*(nid-n)/nid

plt.figure() #Plot von n
x=np.linspace(np.min(a2), np.max(a2))
params,covariance_matrix=np.polyfit(a2, n, deg=1, cov=True)
plt.plot(x, gerade(x, *params), "k", label="Regression")
plt.plot(a2, n, '.', label='Messdaten')
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$n$")
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('plot2.pdf')

i         = 0 #Ausgeben der Parameter
h         = ufloat(0,0)
paramserr2 = np.array([h, h])
errors    = np.sqrt(np.diag(covariance_matrix))
for name, value, error in zip('ab', params, errors):
    paramserr2[i]=ufloat(value, error)
    print(f'{name} = {value:.8f} ± {error:.8f}')
    i     = i+1

c   = 2.9979*10^8 #berechnen der Lichtgeschwindigkeit
v   = c/nu

############################################################################################################
#Aufgabe3
d   = 5.85*10**(-3)
s1  = d*np.sin(a3-b3)/np.cos(b3) #Strahlenversatz Methode 1
b31 = np.arcsin(np.sin(a3)/nu) #Strahlenversatz Methode 2
s2  = d*np.sin(a3-b3)/np.cos(b3)
p   = 100*(s1-s2)/s1 #vergleichen
plt.plot(a,b, '.', label='Messdaten')#grün
k1g    = np.arcsin(np.sin(a4g)/nkron) #in Prismaskizze: beta1=k1
deltag = (a4g+b4g)-(2*k1g-g)
#rot
k1r    = np.arcsin(np.sin(a4r)/nkron) #in Prismaskizze: beta1=k1
deltar = (a4r+b4r)-(2*k1r-g)

plt.figure() #Plot von Ablenkung
x=np.linspace(np.min(a4), np.max(a4))
paramsg,covariance_matrixg   =   np.polyfit(a4g, deltag, deg=1, cov=True)
paramsr,covariance_matrixr   =   np.polyfit(a4r, deltar, deg=1, cov=True)
plt.plot(x, gerade(x, *paramsg), color='green',   label='Regression grün')
plt.plot(x, gerade(x, *paramsr), color='red',     label='Regression rot')
plt.plot(a4g, deltag, '.',       color='orange',  label='Messdaten grün')
plt.plot(a4r, deltar, '.',       color='blue',    label='Messdaten rot')
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$\delta$")
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('plot4.pdf')

#Ausgeben der Parameter
i          = 0
h          = ufloat(0,0)
paramserrg = np.array([h, h])
errors     = np.sqrt(np.diag(covariance_matrixg))
for name, value, error in zip('ab', paramsg, errors):
    paramserrg[i]=ufloat(value, error)
    print(f'{name} = {value:.8f} ± {error:.8f}')
    i      = i+1 

i          = 0
h          = ufloat(0,0)
paramserrr = np.array([h, h])
errors     = np.sqrt(np.diag(covariance_matrixr))
for name, value, error in zip('ab', paramsr, errors):
    paramserrr[i]=ufloat(value, error)
    print(f'{name} = {value:.8f} ± {error:.8f}')
    i      = i+1
############################################################################################################s
#Aufgabe5