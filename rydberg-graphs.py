from calendar import c
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi as π
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat

d = 1/(78.8*1000)                               # When using the slit grating of 80 lines per mm
titleFont = {'fontname':'CMU Serif', 'size':12}
axesFont = {'fontname':'CMU Serif','size':9}
table = []
def functionLinear(try_x,try_m,try_c):          # Curve fit to linear function
    return try_m*try_x + try_c

         ## RED GRAPHS (n=3)

m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_red.csv", unpack=True, delimiter = ',')
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Red Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=θErrorMin,mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("RED GRAPH",pfit,", σ=",np.sqrt(cov[0][0]))

          ## CYAN GRAPHS (n=4)

m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_cyan.csv", unpack=True, delimiter = ',')
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Cyan Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=θErrorMin,mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("CYAN GRAPH",pfit,", σ=",np.sqrt(cov[0][0]))

            ## VIOLET GRAPHS (n=5)

m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_blue.csv", unpack=True, delimiter = ',') 
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Violet Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=θErrorMin,mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("VIOLET GRAPH",pfit,", σ=",np.sqrt(cov[0][0]))

            ## FINAL GRAPHS

## Error Propagation
gradient_red = ufloat(table[0][0],table[0][1])
gradient_cyan = ufloat(table[1][0],table[1][1])
gradient_violet = ufloat(table[2][0],table[2][1])
unc_red,unc_cyan,unc_violet = (d*gradient_red),(d*gradient_cyan),(d*gradient_violet)
sigma_red,sigma_cyan,sigma_violet = 1/(d*gradient_red),1/(d*gradient_cyan),1/(d*gradient_violet)
sigmaError = [sigma_red.s,sigma_cyan.s,sigma_violet.s]
print("\nRed λ:",unc_red,"; Cyan λ:",unc_cyan,"; Violet λ:",unc_violet)
print("Errors (σ) in 1/λ respectively:",sigmaError)

gradient_red = table[2][0]              # Remove ufloat integers, with attached uncertainties to work normally
gradient_cyan = table[1][0]
gradient_violet = table[0][0]
red = 1/(d*gradient_red)
cyan = 1/(d*gradient_cyan)
violet = 1/(d*gradient_violet)
x,y = [1/9 - 1/4, 1/16 - 1/4, 1/25 - 1/4],[red,cyan,violet]

## Using Polyfit Method
fit,cov=np.polyfit(x,y,1,cov=1,w=sigmaError)
pfit=np.poly1d(fit)

plt.xlabel("x", **axesFont)
plt.ylabel("1/λ E6 / metres¯¹", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Rydberg Constant", **titleFont) 
plt.errorbar(x,y,ls='',yerr=sigmaError,mew=1,ms=3,capsize=3)
plt.plot(x,pfit(x),'r')
plt.show()

print("\nUSING POLYFIT METHOD:")
print("Covariance Matrix: \n",cov)
print('Rydberg Constant: ',-fit[0],'; σ=',np.sqrt(cov[0,0]))

## CURVE FIT
curvefit,cov_curvefit = curve_fit(functionLinear,x,y,sigma=sigmaError,absolute_sigma=True)

print("USING CURVE_FIT METHOD:")
print("Covariance Matrix: \n",cov_curvefit)
print("Rydberg Constant: ",-curvefit[0],"; σ=",np.sqrt(cov_curvefit[0,0]))

print("End")

#     ** CODE Graveyard **
''' 
gradient_red = ufloat(table[0][0],table[0][1])
gradient_cyan = ufloat(table[1][0],table[1][1])
gradient_violet = ufloat(table[2][0],table[2][1])
red = 1/(d*gradient_red)
cyan = 3/(d*gradient_cyan)
violet = 1/(d*gradient_violet) 
sigmaError = [4542.05644134825,6897.9944017060925,1275.546898533985]
inv = [1/4542.05644134825,1/6897.9944017060925,1/1275.546898533985]
functionLinear(*x,curvefit[0],curvefit[1]),'r')

""" for i in range(len(θErrorMin)):
    errorbarsRed.append([θErrorMin[i],θErrorMax[i]]) """
'''





""" ## Comparison with old method [DEPRECATED]
print("\nUSING POLYFIT METHOD:")

## RED GRAPHS (n=3)
# Input Rydberg Data in 4 columns of a CSV: (m) - Minima Order; (θ) - sin(Angle) / radians; 
# (θmin/θmax) - absolute differences between sin(min) and sin(max from sin(mean)
m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_red.csv", unpack=True, delimiter = ',')
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

errorbarsRed.append([*θErrorMin])
errorbarsRed.append([*θErrorMax])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Red Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=errorbarsRed,mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("RED GRAPH",pfit,", σ=",np.sqrt(cov[0][0]))

## CYAN GRAPHS (n=4)
m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_cyan.csv", unpack=True, delimiter = ',')
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Cyan Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=[θErrorMin,θErrorMax],mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("CYAN GRAPH",pfit,", σ=",np.sqrt(cov[0][0]))

## VIOLET GRAPHS (n=5)
m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/rydberg_violet.csv", unpack=True, delimiter = ',') 
fit,cov=np.polyfit(m,θ,1,cov=1)
pfit=np.poly1d(fit)
table.append([fit[0],np.sqrt(cov[0,0])])

plt.xlabel("Order of maxima (m)", **axesFont)
plt.ylabel("sin(θ)", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.title("Violet Fringe Data", **titleFont) 
plt.errorbar(m,θ,yerr=[θErrorMin,θErrorMax],mew=1,ms=3,capsize=3)
plt.plot(m,pfit(m),'r')
plt.show()

print("VIOLET GRAPH",pfit,", σ=",np.sqrt(cov[0][0])) """




##VERSION 2022.01.21
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi as π
from scipy.optimize import curve_fit
import uncertainties as unc
from uncertainties import umath
from uncertainties import ufloat
def functionLinear(try_x,try_m,try_c):              # Curve fit to linear function
    return try_m*try_x + try_c
                                                    ## ADJUST PARAMETERS
d = 1/(78.8*1000)                                   # When using the slit grating of 80 lines per mm
# Adjust your font settings
titleFont = {'fontname':'CMU Bright','size':13,'fontweight':'bold'}
axesFont = {'fontname':'CMU Sans Serif','size':10}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5}
table,errorbarsRed,errorbarsCyan,errorbarsViolet = [],[],[],[]
filePaths = ["rydberg_red_corrected.csv","rydberg_cyan_corrected.csv","rydberg_violet_corrected.csv"]
colourNames = ["Red","Cyan","Violet"]

# PLOT YOUR GRAPHS [NEW METHOD]:
# Input Rydberg Data in 4 columns of a CSV: (m) - Minima Order; (θ) - sin(Angle) / radians; 
# (θmin/θmax) - absolute differences between sin(min) and sin(max from sin(mean)
for i in range(3):
    errorbars,absoluteError = [],[]
    m,θ,θErrorMin,θErrorMax = np.loadtxt(r"Lab/Term 2/2022.01.20 Rydberg Constant - Computing/" + filePaths[i], unpack=True, delimiter = ',')
    errorbars.append([*θErrorMin])
    errorbars.append([*θErrorMax])
    for j in range(len(θErrorMin)):
        absoluteError.append((θErrorMin[j]+θErrorMax[j])/2)
    #fit,cov=np.polyfit(m,θ,1,cov=1)
    curvefit,cov_curvefit = curve_fit(functionLinear,m,θ,sigma=absoluteError,absolute_sigma=True)
    #pfit=np.poly1d(fit)
    plt.xlabel("Order of maxima, m", **axesFont)
    plt.ylabel("sin(θ)", **axesFont)
    plt.xticks(**axesFont)
    plt.yticks(**axesFont)
    plt.title("Data for " + colourNames[i] +" Light", **titleFont) 
    plt.errorbar(m,θ,yerr=errorbars,**errorStyle)
    plt.plot(m,θ,'x',**pointStyle)
    plt.plot(m,functionLinear(m,*curvefit),'r',**lineStyle)
    #plt.plot(m,pfit(m),'r')
    plt.show()
    
    print(colourNames[i]+" GRAPH")
    #print("USING POLYFIT METHOD:",pfit,", σ=",np.sqrt(cov[0][0]))
    #table.append([fit[0],np.sqrt(cov[0,0])])

    print("USING CURVE_FIT METHOD:")
    print("Covariance Matrix: \n",cov_curvefit)
    print(curvefit[0],"; σ=",np.sqrt(cov_curvefit[0,0]))
    table.append([curvefit[0],np.sqrt(cov_curvefit[0,0])])    

## FINAL GRAPHS
## Error Propagation
gradient_red,gradient_cyan,gradient_violet = ufloat(table[0][0],table[0][1]),ufloat(table[1][0],table[1][1]),ufloat(table[2][0],table[2][1])
unc_red,unc_cyan,unc_violet = (d*gradient_red),(d*gradient_cyan),(d*gradient_violet)
sigma_red,sigma_cyan,sigma_violet = 1/(d*gradient_red),1/(d*gradient_cyan),1/(d*gradient_violet)
sigmaError = [sigma_red.s,sigma_cyan.s,sigma_violet.s]

print("\nRed λ:",unc_red,"; Cyan λ:",unc_cyan,"; Violet λ:",unc_violet)
print("Errors (σ) in 1/λ respectively:",sigmaError)

red,cyan,violet = 1/(d*gradient_red._nominal_value),1/(d*gradient_cyan._nominal_value),1/(d*gradient_violet._nominal_value)
x,y = [1/9 - 1/4, 1/16 - 1/4, 1/25 - 1/4],[red,cyan,violet]
s = np.poly1d(x)

curvefit,cov_curvefit = curve_fit(functionLinear,x,y,sigma=sigmaError,absolute_sigma=True)
fit,cov=np.polyfit(x,y,1,cov=1,w=sigmaError)
pfit=np.poly1d(fit)

plt.xlabel("x, 1/n² - 1/p² / dimensionless", **axesFont)
plt.ylabel("1/λ / m¯¹", **axesFont)
plt.xticks(**axesFont)
plt.yticks(**axesFont)
plt.ticklabel_format(style='plain')
plt.title("Rydberg Constant, Determination Graph", **titleFont) 
plt.errorbar(x,y,yerr=sigmaError,**errorStyle)
plt.plot(x,y,'x',**pointStyle)
plt.plot(s,curvefit[0]*s+curvefit[1],'r',**lineStyle)
#plt.plot(x,pfit(x),'r',**lineStyle)
plt.show()
#print("\nUSING POLYFIT METHOD:")
#print("Covariance Matrix: \n",cov)
#print('Rydberg Constant: ',-fit[0],'; σ=',np.sqrt(cov[0,0]))
## Using Curvefit Method (for the actual values)
print("USING CURVE_FIT METHOD:")
print("Covariance Matrix: \n",cov_curvefit)
print("Rydberg Constant: ",-curvefit[0],"; σ=",np.sqrt(cov_curvefit[0,0]))
print("End")
"""