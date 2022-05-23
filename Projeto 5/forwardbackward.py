Ps1T = 0.6 * 0.8 + 0.4*0.2
Ps1F = 0.6 * 0.2 + 0.4*0.8
Ps1 = (Ps1T, Ps1F)
print(Ps1)

pse1T = 0.72*Ps1[0]
pse1F = 0.21*Ps1[1]
Pse1 = (pse1T, pse1F)
Pse1N = (pse1T/(pse1T + pse1F), pse1F/(pse1T + pse1F))
print(Pse1)
print(Pse1N)
print("")

Ps2e1T = 0.8 * Pse1[0] + 0.2 * Pse1[1]
Ps2e1F = 0.2 * Pse1[0] + 0.8 * Pse1[1]
Ps2e1 = (Ps2e1T, Ps2e1F)
print(Ps2e1)

Pse2T = Ps2e1[0] * 0.18
Pse2F = Ps2e1[1] * 0.49
Pse2 = (Pse2T, Pse2F)
Pse2N = (Pse2T/(Pse2T + Pse2F), Pse2F/(Pse2T + Pse2F))
print(Pse2)
print(Pse2N)
print("")

Ps3e2T = 0.8 * Pse2[0] + 0.2 * Pse2[1]
Ps3e2F = 0.2 * Pse2[0] + 0.8 * Pse2[1]
Ps3e2 = (Ps3e2T, Ps3e2F)
print(Ps3e2)

Pse3T = Ps3e2[0] * 0.02
Pse3F = Ps3e2[1] * 0.21
Pse3 = (Pse3T, Pse3F)
Pse3N = (Pse3T/(Pse3T + Pse3F), Pse3F/(Pse3T + Pse3F))
print(Pse3)
print(Pse3N)
print("")

beta3F = 1
beta3T = 1
beta3 = (beta3T, beta3F)
saida3 = (beta3[0] * Pse3[0] / (beta3[0] * Pse3[0] + beta3[1] * Pse3[1]), beta3[1] * Pse3[1] / (beta3[0] * Pse3[0] + beta3[1] * Pse3[1]))

beta2T = 0.8 * 0.02 * beta3[0] + 0.2 * 0.21 * beta3[1] 
beta2F = 0.2 * 0.02 * beta3[0] + 0.8 * 0.21 * beta3[1]
beta2 = (beta2T, beta2F)
saida2 = (beta2[0] * Pse2[0] / (beta2[0] * Pse2[0] + beta2[1] * Pse2[1]), beta2[1] * Pse2[1] / (beta2[0] * Pse2[0] + beta2[1] * Pse2[1]))

beta1T = 0.8 * 0.18 * beta2[0] + 0.2 * 0.49 * beta2[1]
beta1F = 0.2 * 0.18 * beta2[0] + 0.8 * 0.49 * beta2[1]
beta1 = (beta1T, beta1F)
saida1 = (beta1[0] * Pse1[0] / (beta1[0] * Pse1[0] + beta1[1] * Pse1[1]), beta1[1] * Pse1[1] / (beta1[0] * Pse1[0] + beta1[1] * Pse1[1]))

print(beta1)
print(saida1)
print("")
print(beta2)
print(saida2)
print("")
print(beta3)
print(saida3)