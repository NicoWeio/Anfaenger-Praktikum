import matplotlib.pyplot as plt
import numpy as np
import sympy
from sympy import *

t, T1, p1, T2, p2, N = np.genfromtxt('Waermepumpe.txt', unpack=True)

#Umrechung in SI
t=t*60
p1=(p1+1)*(10)**5
p2=(p2+1)*(10)**5
T1=T1+273.15
T2=T2+273.15
########################################################################################

#a,b) Temperaturverläufe als Diagramm

#Parameter für Regression
params1, covariance_matrix1 = np.polyfit(t, T1, deg=2, cov=True)
params2, covariance_matrix2 = np.polyfit(t, T2, deg=2, cov=True)

#Unsicherheit der Regression
errors1 = np.sqrt(np.diag(covariance_matrix1))
errors2 = np.sqrt(np.diag(covariance_matrix2))
print("Die Parameter der Regression für T1: \n")
for name, value, error in zip('abc', params1, errors1):
    print(f'{name} = {value:.8f} ± {error:.8f}')
print("\n")
print("Die Parameter der Regression für T2: \n")
for name, value, error in zip('abc', params2, errors2):
    print(f'{name} = {value:.8f} ± {error:.8f}')
print("\n")

#Plotten der Regression
x_plot = np.linspace(0, 2100)
plt.plot(
    x_plot,
    params1[0] * (x_plot)**2 + params1[1] * x_plot + params1[2],
    label='Regression T1',
    linewidth=3,
)
x_plot = np.linspace(0, 2100)
plt.plot(
    x_plot,
    params2[0] * (x_plot)**2 + params2[1] * x_plot + params2[2],
    label='Regression T2',
    linewidth=3,
)
#Plotten der Messwerte
plt.plot(t, T1, '.', label='T1')
plt.plot(t, T2, '.', label='T2')

plt.xlabel(r"$t/s$")
plt.ylabel(r"$T/K$")
plt.legend(loc="best")
plt.savefig('Temperaturverlaeufe.pdf')

############################################################################################
#c, d) Differentailquotient und Güteziffer

#Berechnung von dT/dt
x = sympy.var('x')
funkT1=params1[0] * (x)**2 + params1[1] * x + params1[2]
funkT2=params2[0] * (x)**2 + params2[1] * x + params2[2]
difT1=funkT1.diff(x) #dT1/dt
difT2=funkT2.diff(x) #dT2/dt

#Berechnung der Güteziffern
i=1
a1=4*4183
a2=750
print("Berechnet mit T1 \n\n")
while(i<40): #4 unterschiedliche Zeiten mit 10s Abstand
    vid=T1[i]/(T1[i]-T2[i]) #ideale Güte
    vreal1=((a1+a2)*difT1.subs(x, i))/N[i] #Reale Güte
    p=(vid-vreal1)/vid #Berechnet die Abweichung zwischen vreal und vid in %
    print(f"die reale  Güte nach t={t[i]} Sekunden {vreal1:.5f}")
    print(f"die ideale Güte nach t={t[i]} Sekunden {vid:.5f}")
    print(f"die Abweichung beträgt {p*100:.2f}% vom Idealwert")
    print("\n")
    i=i+10
i=1
print("Berechnet mit T2 \n\n") #!!!!!!!!!!nochmal überprüfen!!!!!!!!!
while(i<40): #4 unterschiedliche Zeiten mit 10s Abstand
    vid=-T2[i]/(T2[i]-T1[i]) #ideale Güte
    vreal2=-((a1+a2)*difT2.subs(x, i))/N[i] #Reale Güte
    p=(vid-vreal2)/vid #Berechnet die Abweichung zwischen vreal und vid in %
    print(f"die reale  Güte nach t={t[i]} Sekunden {vreal2:.5f}")
    print(f"die ideale Güte nach t={t[i]} Sekunden {vid:.5f}")
    print(f"die Abweichung beträgt {p*100:.2f}% vom Idealwert")
    print("\n")
    i=i+10
############################################################################################################

#e) Massendurchsatz, Verdampfungswärme, Dampfdruckkurve
# aus V203-"Verdampfungswärme" ist begkannt:
# ln(p/p0)=_-L/(R*T)+c
# aus V203-"Verdampfungswärme" ist begkannt:
# ln(p)= -L/(R*T)+c
# aus V203-"Verdampfungswärme" ist bekannt:
# ln(p)=_-L/(R*T)+c
# p=p0*exp(-L/(R*T))
# dabei ist R=ideale-Gaskonst., p=gemessener Druck, p0=Umgebungs-Druck, T=Temperatur, L=Verdampfungswärme, c=const.
# daher wählen wir
# x = 1/T
# y = ln(p/p0)
# Dann erhalten wir die Gerade: y=-(L/R)*x+c
# => L=-m*R mit m=Steigung der Regressionsgeraden

plt.figure("""first figure""")
p0=100300

plt.subplot(2,1,1) #Plot für die Messdaten 1

#Parameter für Regression
params3, covariance_matrix3 = np.polyfit(1/T1, np.log(p1/p0), deg=1, cov=True)

#Unsicherheit der Regression
errors = np.sqrt(np.diag(covariance_matrix3))
print("Die Parameter der Regression für p1:")
print('a1 = {:.3f} ± {:.4f}'.format(params3[0], errors[0]))
print('b1 = {:.3f} ± {:.4f}'.format(params3[1], errors[1]))
print("\n")

#Plotten der Regression
x_plot = np.linspace(np.min(1/T1), np.max(1/T1))
plt.plot(
    x_plot,
    params3[0]*x_plot+params3[1],
    'b-',
    label='Ausgleichsgerade'
    )
#Plotten der Messdaten
plt.plot(1/T1, np.log(p1/p0), 'r.', label='Messdaten')

plt.xlabel(r'$1/T_1 [K^{-1}]$') #nochmal überprüfen
plt.ylabel(r'$ln(p_1/p_0)$')
plt.legend(loc='best')



plt.subplot(2,1,2) #Plot für die Messdaten 2

#Parameter für Regression
params4, covariance_matrix4 = np.polyfit(1/T2, np.log(p2/p0), deg=1, cov=True)

#Unsicherheit für Regression
errors = np.sqrt(np.diag(covariance_matrix4))
print("Die Parameter der Regression für p2:")
print('a2 = {:.3f} ± {:.4f}'.format(params4[0], errors[0]))
print('b2 = {:.3f} ± {:.4f}'.format(params4[1], errors[1]))
print("\n")

#Plotten der Regression
x_plot = np.linspace(np.min(1/T2), np.max(1/T2))
plt.plot(
    x_plot,
    params4[0]*x_plot+params4[1],
    'b-',
    label='Ausgleichsgerade'
    )

#Plotten der Messdaten
plt.plot(1/T2, np.log(p2/p0), 'r.', label='Messdaten')

plt.xlabel(r'$1/T_2 [K^{-1}]$') #nochmal überprüfen
plt.ylabel(r'$ln(p_2/p_0)$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Druckverlaeufe.pdf')

#Berechnung der Verdampfungswärme
L1=-params3[0]*8.3144621 #hier am besten R einfügen
L2=-params4[0]*8.3144621 #Einheit: [R]=J/(K*mol)
print(f"Aus Messreihe 1 folgt: \n L={L1} \n")
print(f"Aus Messreihe 2 folgt: \n L={L2}\n\n")

#Brechnung des Massendurchsatzes
# dQ/dt=L*dm/dt
#=> dm/dt=(1/L)(dQ2/dt)=(N*v/L)

#Einheiten:
#[L]=J/mol, [dm/dt]=mol/s
molmass=120.91 #g/mol
i=1
while(i<40):
    massdu=-((a1+a2)*difT2.subs(x, i))/L1 #difQ2 #!!!warum difT2 und L2???
    print(f"Der Massendruchsatz nach t={i}s ist: dm/dt={massdu:.5f}mol/s={massdu*molmass:.5f}g/s")
    i=i+10
print("\n")
#################################################################################


#f) Die mechanische Leistung des Kompressors

i=1
k=1.14
rho0=5.51 * 10**3 #g/m^3
T0=273.15 #K

while(i<40):
    rho=(rho0*T0*p1[i])/(T2[i]*p0) #g/m^3
    Nmech1=(1/(k-1))
    Nmech2=Nmech1*(p2[i]*(p1[i]/p2[i])**(1/k)-p1[i]) #pa
    Nmech3=Nmech2*(1/rho) #pa*m^3/g
    Nmech4=Nmech3*((a1+a2)/L1)*difT1.subs(x, i)*molmass #W
    #print(rho*10**(-3))#kg/m^3
    print(f"die mechanische Leistung nach t={t[i]} Sekunden: Nmech={Nmech4:.5f}W")
    i=i+10