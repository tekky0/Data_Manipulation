import numpy as np
import matplotlib.pyplot as plt
import eng1014 as eng

# load data
data = np.genfromtxt("C:\\Users\\Ezekiel Chang\\Downloads\\6063 alloy (1).txt", skip_header=1, encoding="utf-8", dtype=float,delimiter="\t");

# 6603 desc thick, width, length
# mat1 = np.array([1.5, 3.2, 25]);
# mat1 = input("Input[thickness, width, length](mm): ").split(",");
# try:
#     mat1 = [float(i.strip()) for i in mat1];
#     area = mat1[0]*mat1[1];
#     length = mat1[2];
# except ValueError:
#     print("wrong ahh input");

area = 14;
length = 25;
# seperate into load and extension N and mm i think idk
load = data[:,0];
ext = data[:,1];
sigmaboi = load/area;
strain = ext/length;

fig, axe = plt.subplots(1,2, figsize=(12,4));

axe[0].plot(ext,load, color="red", label="Load-Extension");
axe[0].set_title("Load-Extension Graph")
axe[0].set_ylabel("Load(N)");
axe[0].set_xlabel("Extension(mm)");
maxF = np.max(load);
inmaxF = np.argmax(load);


axe[0].plot(ext[inmaxF], maxF, marker="d", color="black", label=f"Maximum Force, Extension = {maxF} N, {ext[inmaxF]}mm");


axe[1].plot(strain, sigmaboi, color="blue", label="Stress-Strain");
axe[1].set_title("Stress-Strain Graph");
axe[1].set_xlabel("Strain(mm)");
axe[1].set_ylabel("Stress(MPa)");
maxStress = np.max(sigmaboi);
inmaxStress = np.argmax(sigmaboi);
axe[1].plot(strain[inmaxStress], maxStress, label=f"Max Stress = {maxStress} MPa");

axe[1].legend(loc="best");
axe[0].legend(loc="best");


# toughness
n = 1501
# Ustress = np.linspace(sigmaboi[0], sigmaboi[-1], n);
Ustrain = np.linspace(strain[0], strain[-1], n);
Ustress = np.interp(Ustrain, strain, sigmaboi);

print(maxStress*area);
print(eng.comp_simp13_vector(Ustrain,Ustress))



fig.tight_layout(pad=3.0);
plt.show(block=False);

# print(sigmaboi);
ylin = np.argmin(np.abs(sigmaboi[:np.shape(sigmaboi)[0]//2] - float(input("Stress where graph stops being linear: "))));
axe[1].plot(strain[:ylin], sigmaboi[:ylin], color="green", label="Linear Region");

# linear fit
# a1 is m and a0 is intercept
a0,a1,r2 = eng.linreg(strain[:ylin], sigmaboi[:ylin]);
y = a1*strain[:ylin] + a0;

axe[1].plot(strain[:ylin], y, color="orange", label=f"Linear fit of 'Linear' Region\ny = {a1:.2f}x + {a0:.2f}; r2 = {r2:.2f}");
axe[1].axhline(y[-1], linestyle=":", color="red", label="End of Linear Region");
# proof stress

offset = 0.2

half = np.shape(strain)[0]//2
strainOffset = strain[:half];
pstress = a1*(strainOffset-(offset*0.01)) + a0

xint = (strainOffset - strain[:half])/(pstress-sigmaboi[:half]) * strain[:half] - strain[:half];

axe[1].plot(strainOffset, pstress, color='purple', linestyle=':', label=f'0.2% Proof Stress');

axe[1].legend(loc="best");
plt.show(block=True);


