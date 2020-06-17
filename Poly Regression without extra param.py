#this code does all these:
#   
#   1)  finds coefficients for the regression curve z = b1 * y * e^(-b2 * x) + b0 : 
#           where b0,b1,b2 are the coefficients of regression line
#           and x,y,z are the 3 random variables
#       precision set to 5 decimal places (adjustable to any value 'n' by using 10^n wherever 10^5 used)
#
#   2)  displays the 3d scatter plot of 3 variables by extracting the data from the specified excel file
#try to keep azimuth = 31 deg, elevation = 11 deg
#
#   3)  simulates -from observed values- the estimated model of relation between x,y and z where they are related as
#       z = b1 * y * e^(-b2 * x) + b0 : 
#           where b0,b1,b2 are the coefficients of regression line
#           and x,y,z are the 3 random variables
#       precision set to 5 decimal places (adjustable to any value 'n' by using 10^n wherever 10^5 used)

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import xlrd
import numpy as np
import scipy.stats as st

#location of excel file:
#  'r' is prefixed to the location string to pass it as a 'Raw String'
#       this is because single backward-slashes aren't processed properly by regular strings
#       to avoid replacing every single backward-slash with double backward-slash (\ => \\) we prefix the string with 'r'
loc=(r"D:\User\Desktop\Suja\AIRGLOW-MAY-2020\AG-WORK-SHIVA.xls")


#values to be input before running:
sheet_pos=12                                      #sheet position number
n_min=0000                                       #suspected b2 lower bound * 10^5   
n_max=10000                                       #suspected b2 upper bound * 10^5

sa_colindex=11                                   #column no. zero index of Sun Angle
sf_colindex=12                                   #column no. zero index of Solar Flux
ca_colindex=13                                   #column no. zero index of FUV_TEC_MIN



#importing values from excel file:
wb=xlrd.open_workbook(loc)
sheet=wb.sheet_by_index(sheet_pos-1)             #change index as sheet_position - 1
sheet.cell_value(0,0)

all_sheet_names=wb.sheet_names()                 #an array of all sheet names
sheet_name=all_sheet_names[sheet_pos-1]          #returns the name of the sheet currently chosen using sheet_pos

##
i_min=1
i_max=sheet.nrows-1


X=[]
Y=[]
Z=[]
CA=[]

for i in range(i_min,i_max):                     #change range values as (start_row - 1, end_row - 1)
    itemx=sheet.cell_value(i,sa_colindex)                 #here 11,12,13 corresponds to Column_Name_as_number - 1
    itemy=sheet.cell_value(i,sf_colindex)
    itemz=sheet.cell_value(i,ca_colindex)
    X.append(itemx)
    Y.append(itemy)
    Z.append(itemz)
   

#   finding coefficients for non-linear regression:
#       b0=l
#       b1=m
#       b2=n
#   can also obtain these values from the second last "Running..." output line
a=0
b=0
c=0
d=0
e=0
f=0
g=0
h=0
i=0
sse=0                                            
sseb=0

b0=0
b1=0
b2=0

for n in range(n_min,n_max):                     #change range values as (b2_suspected_lower_extreme * 10^5, b2_suspected_upper_extreme * 10^5)
    k=n/100000
    sse=0
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0
    h=0
    i=0
    for j in range(0,i_max-i_min):               #change range values as (0, i_max - i_min)
        a+=1
        b+=Y[j]*np.exp(-k*X[j])
        c+=Z[j]
        d+=Y[j]*np.exp(-k*X[j])
        e+=pow(Y[j]*np.exp(-k*X[j]),2)
        f+=Y[j]*Z[j]*np.exp(-k*X[j])
        g+=Y[j]*X[j]*np.exp(-k*X[j])
        h+=X[j]*pow(Y[j]*np.exp(-k*X[j]),2)
        i+=X[j]*Y[j]*Z[j]*np.exp(-k*X[j])
    l=(e*c-b*f)/(a*e-d*b)
    m=(a*f-d*c)/(a*e-d*b)
    sse=l*g+m*h-i                                #This is the expression to be brought to zero to obtain the best-fit for our regression curve
    print("running",l,m,k,sse,sseb)              #also functions as a manual result verification technique
    if n == n_min:                               #checking for first iteration condition
        sseb=sse
    if abs(sseb)<abs(sse):                       #if minimum of sse (i.e. 0) has already passed
        print(n-1)
        break
    if abs(sseb)>abs(sse) and n!=n_min :         #update expression if minimum of sse (i.e. 0) hasn't occured yet
        sseb=sse
        b0=l                                     #new prospective values for the coefficients stored only if min
        b1=m                                     #  hasn't reached yet
        b2=k

#   final values of b0, b1, and b2
print("\n\nb0 = ", b0, "\nb1 = ", b1, "\nb2 = ", b2)

#   to find correlation coefficient and p-value of our estimated relation:
for i in range(i_min,i_max):                     #change range values as (start_row - 1, end_row - 1)
    itemca=b1*sheet.cell_value(i,sf_colindex)*np.exp(-b2*sheet.cell_value(i,sa_colindex))+b0  
    CA.append(itemca)                            #here 11,12,13 corresponds to Column_Name_as_number - 1

r, p=st.pearsonr(np.array(CA),np.array(Z))
print("\n\n\nCorrelation Coefficient = ", r, "\nP-Value \t\t= ",p)


#   to display scatter plot
fig=plt.figure(1)
ax=plt.axes(projection='3d')
ax.scatter3D(X, Y, Z, c=Z,cmap='inferno')
ax.set_title(sheet_name+" Observations")
ax.set_xlabel("Sun Angle")
ax.set_ylabel("Solar Flux")
ax.set_zlabel("Constant Airglow");
ax.view_init(11,31)                              #first param is elevation, then azimuth for a fixed view

#   Model Simulation code:
#       interpolation function uses the non-linear regression curve which was found earlier
#       sf => solar flux
#       sa => solar angle
def f(sf, sa):
    return b1*sf*np.exp(-b2*sa)+b0

#   interpolating code:
#       change 30 according to the desired model resolution
x = np.linspace(min(X), max(X), 30)
y = np.linspace(min(Y), max(Y), 30)

A, B = np.meshgrid(x, y)
C = f(B, A)

#multiline strings can be used as multiline comments if it isnt assigned to anything
"""                                                                     

#   surface plotting code:
fig=plt.figure(2)
ax=plt.axes(projection='3d')
ax.plot_surface(A, B, C, rstride=1, cstride=1, cmap='inferno', edgecolor='none')
ax.set_title(sheet_name+" Simulation")
ax.set_xlabel("Sun Angle")
ax.set_ylabel("Solar Flux")
ax.set_zlabel("Constant Airglow");

"""

#   superimpose observation and simulation:
fig=plt.figure(3)
ax=plt.axes(projection='3d')
ax.scatter3D(X, Y, Z, c=Z,cmap='cool')
ax.plot_surface(A, B, C, rstride=1, cstride=1, cmap='inferno', edgecolor='none')
ax.set_title(sheet_name+" Observations v/s Simulation")
ax.set_xlabel("Sun Angle")
ax.set_ylabel("Solar Flux")
ax.set_zlabel("Constant Airglow");
ax.view_init(11,31)                              #first param is elevation, then azimuth for a fixed view

plt.show()
plt.close('all')
