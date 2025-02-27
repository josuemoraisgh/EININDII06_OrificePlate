import math

def compute_corrections(tap_type, L_upstream, L_downstream, D, material, orifice_type):
    # Fator de correção para o tipo de tomadas (taps)
    tap_correction = {
        "flange": 1.00,
        "radius": 0.98,
        "vena": 0.95,
        "corner": 0.97,
        "pipe": 0.96
    }
    K_tap = tap_correction.get(tap_type.lower(), 1.00)
    
    # Correção para instalação: recomenda-se L_upstream >= 10*D e L_downstream >= 5*D.
    K_up = 1.0 if L_upstream >= 10 * D else L_upstream / (10 * D)
    K_down = 1.0 if L_downstream >= 5 * D else L_downstream / (5 * D)
    K_inst = K_up * K_down

    # Fator de correção para material da tubulação
    material_correction = {
        "steel": 1.00,
        "cast iron": 0.98,
        "stainless steel": 1.02,
        "plastic": 1.00,
        "copper": 1.00
    }
    K_material = material_correction.get(material.lower(), 1.00)

    # Fator de correção para o tipo de orifício
    orifice_correction = {
        "concentrico": 1.00,
        "excêntrico": 0.98,
        "segmental": 0.96,
        "conica": 1.01,
        "bordo": 1.00
    }
    K_orifice = orifice_correction.get(orifice_type.lower(), 1.00)

    # Produto final dos fatores de correção
    return K_tap, K_inst, K_material, K_orifice

def flow_rate_from_beta(beta, D, deltaP, rho, C_eff, epsilon):
    """
    Calcula a vazão volumétrica Q (m³/s) para um dado beta,
    onde d = beta * D e A = π*(d)²/4.
    """
    d = beta * D
    A = math.pi * d**2 / 4.0
    # Cuidado: 1 - beta^4 não pode ser zero; beta está em (0,1)
    Q = C_eff * epsilon * A * math.sqrt(2 * deltaP / (rho * (1 - beta**4)))
    return Q

def find_beta(Q_desired, D, deltaP, rho, C_eff, epsilon, tol=1e-6, max_iter=100):
    """
    Resolve a equação f(beta) = Q(beta) - Q_desired = 0 por bisseção para beta.
    Considera beta no intervalo [0.25, 0.72], faixa típica para dimensionamento.
    """
    beta_min = 0.25
    beta_max = 0.72
    
    f_min = flow_rate_from_beta(beta_min, D, deltaP, rho, C_eff, epsilon) - Q_desired
    f_max = flow_rate_from_beta(beta_max, D, deltaP, rho, C_eff, epsilon) - Q_desired
    
    # Verifica se há mudança de sinal; se não, o Q_desired pode estar fora do alcance
    if f_min * f_max > 0:
        raise ValueError("A vazão desejada não está no intervalo possível para beta entre 0.25 e 0.72.")

    for _ in range(max_iter):
        beta_mid = (beta_min + beta_max) / 2.0
        f_mid = flow_rate_from_beta(beta_mid, D, deltaP, rho, C_eff, epsilon) - Q_desired
        if abs(f_mid) < tol:
            return beta_mid
        if f_min * f_mid < 0:
            beta_max = beta_mid
            f_max = f_mid
        else:
            beta_min = beta_mid
            f_min = f_mid

    return (beta_min + beta_max) / 2.0

def calculate_orifice_diameter(Q_desired, D, deltaP, rho, C, epsilon,
                               L_upstream, L_downstream, tap_type, material, orifice_type):
    """
    Calcula o diâmetro do orifício (d) necessário para atingir a vazão volumétrica desejada.
    
    Parâmetros:
      Q_desired   : Vazão volumétrica desejada (m³/s)
      D           : Diâmetro interno da tubulação (m)
      deltaP      : Queda de pressão diferencial (Pa)
      rho         : Densidade do fluido (kg/m³)
      C           : Coeficiente de descarga base (ex.: 0.61)
      epsilon     : Fator de expansibilidade (1.0 para líquidos)
      L_upstream  : Distância a montante (m)
      L_downstream: Distância a jusante (m)
      tap_type    : Tipo de tomadas (ex.: "flange", "radius", etc.)
      material    : Material da tubulação (ex.: "steel", "cast iron", etc.)
      orifice_type: Tipo de orifício (ex.: "concentrico", "excêntrico", "segmental", "conica", "bordo")
    
    Retorna:
      d_orifice   : Diâmetro do orifício (m)
      beta        : Razão (d_orifice / D)
      corrections : Dicionário com os fatores de correção e o coeficiente efetivo.
    """
    # Calcula os fatores de correção
    K_tap, K_inst, K_material, K_orifice = compute_corrections(tap_type, L_upstream, L_downstream, D, material, orifice_type)
    C_eff = C * K_tap * K_inst * K_material * K_orifice

    # Encontra o beta que satisfaz Q_desired
    beta = find_beta(Q_desired, D, deltaP, rho, C_eff, epsilon)
    d_orifice = beta * D

    corrections = {
        "K_tap": K_tap,
        "K_inst": K_inst,
        "K_material": K_material,
        "K_orifice": K_orifice,
        "C_eff": C_eff
    }

    return d_orifice, beta, corrections


print("Dimensionamento de Placa de Orifício a partir da Vazão Volumétrica Desejada")
print("-----------------------------------------------------------------------")

Q_desired = 0.02 # float(input("Digite a vazão volumétrica desejada Q (Nm³/s): "))
D = 0.15 # float(input("Digite o diâmetro interno da tubulação D (m): "))
deltaP = 50000 # float(input("Digite a queda de pressão ΔP (Pa): "))
rho = 1000.0 # float(input("Digite a densidade do fluido ρ (kg/m³): "))
C = 0.61 # float(input("Digite o coeficiente de descarga base C (ex.: 0.61): "))
epsilon = 1.0 # float(input("Digite o fator de expansibilidade ε (1.0 para líquidos): "))
L_upstream = 10*D # float(input("Digite a distância a montante da placa (m): "))
L_downstream = 5*D # float(input("Digite a distância a jusante da placa (m): "))
# print("\nTipos de tomadas disponíveis: flange, radius, vena, corner, pipe")
tap_type = "flange" # input("Digite o tipo de tomada utilizado: ").strip()
# print("\nMateriais de tubulação disponíveis: steel, cast iron, stainless steel, plastic, copper")
material = "steel" # input("Digite o material da tubulação: ").strip()
# print("\nTipos de orifício disponíveis: concentrico, excêntrico, segmental, conica, bordo")
orifice_type = "concentrico" # input("Digite o tipo de orifício da placa: ").strip()
        
d_orifice, beta, corrections = calculate_orifice_diameter(
    Q_desired, D, deltaP, rho, C, epsilon,
    L_upstream, L_downstream, tap_type, material, orifice_type
)

print("\nResultados:")
print("Razão β (d/D): {:.4f}".format(beta))
print("Diâmetro do orifício d: {:.4f} m".format(d_orifice))
print("\nFatores de Correção Aplicados:")
print(" - K_tap (tipo de tomada): {:.3f}".format(corrections["K_tap"]))
print(" - K_inst (instalação): {:.3f}".format(corrections["K_inst"]))
print(" - K_material (material): {:.3f}".format(corrections["K_material"]))
print(" - K_orifice (tipo de orifício): {:.3f}".format(corrections["K_orifice"]))
print(" - Coeficiente de Descarga Efetivo (C_eff): {:.3f}".format(corrections["C_eff"]))
