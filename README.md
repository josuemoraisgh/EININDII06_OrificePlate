# Sumário

- [1. Derivação da Equação de Velocidade a partir da Equação de Bernoulli](#1-derivação-da-equação-de-velocidade-a-partir-da-equação-de-bernoulli)
- [2. Equação para Vazão Real com Correções](#2-equação-para-vazão-real-com-correções)
- [3. Método Iterativo para Dimensionamento de Placa de Orifício](#3-método-iterativo-para-dimensionamento-de-placa-de-orifício)
- [4. Valores Genéricos Típicos para Referência](#4-valores-genéricos-típicos-para-referência)
- [5. Exemplo Prático](#5-exemplo-prático)
- [6. Conclusão](#6-conclusão)

---

## 1. Derivação da Equação de Velocidade a partir da Equação de Bernoulli

Para obter a relação
$$
V = \sqrt{\frac{2\Delta P}{\rho}},
$$
partimos da equação de Bernoulli para um escoamento incompressível, estacionário e sem atrito. Em sua forma geral, para dois pontos (1 e 2) ao longo de uma linha de corrente, a equação de Bernoulli é dada por

$$
\frac{P_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{P_2}{\rho g} + \frac{V_2^2}{2g} + z_2,
$$

onde:
>>> - $P$ é a pressão;
>>> - $\rho$ é a densidade do fluido;
>>> - $V$ é a velocidade do escoamento;
>>> - $g$ é a aceleração da gravidade;
>>> - $z$ é a elevação.

### Simplificações e Assunções

1. **Fluxo Horizontal:**  
   Se o tubo é horizontal, então $z_1 = z_2$. Isso elimina os termos de energia potencial:
   $$
   \frac{P_1}{\rho g} + \frac{V_1^2}{2g} = \frac{P_2}{\rho g} + \frac{V_2^2}{2g}.
   $$

2. **Velocidade Inicial Desprezível:**  
   Escolhe-se o ponto 1 em uma seção ampla antes da placa, onde o fluido tem velocidade muito baixa em comparação com a velocidade na seção restrita (vena contracta). Assim, assumimos:
   $$
   V_1 \approx 0.
   $$

3. **Ausência de Perdas Dissipativas:**  
   Nesta análise ideal, não consideramos perdas por atrito ou turbulência; estas serão incorporadas posteriormente via coeficiente de descarga.

### Derivação

Com as simplificações, a equação de Bernoulli entre o ponto 1 (antes da restrição) e o ponto 2 (na vena contracta) torna-se:
$$
\frac{P_1}{\rho g} = \frac{P_2}{\rho g} + \frac{V_2^2}{2g}.
$$
Multiplicando ambos os lados por $g$:
$$
\frac{P_1}{\rho} = \frac{P_2}{\rho} + \frac{V_2^2}{2}.
$$
Reorganizando:
$$
\frac{P_1 - P_2}{\rho} = \frac{V_2^2}{2}.
$$
Definindo a queda de pressão $\Delta P = P_1 - P_2$, temos:
$$
\frac{\Delta P}{\rho} = \frac{V_2^2}{2}.
$$
Multiplicando por 2 e isolando $V_2$:
$$
V_2 = \sqrt{\frac{2\Delta P}{\rho}}.
$$

Portanto, sob as condições:
- Fluxo horizontal: $z_1 = z_2$
- Velocidade inicial desprezível: $V_1 \approx 0$
- Sem perdas dissipativas

obtém-se a equação fundamental:
$$
V = \sqrt{\frac{2\Delta P}{\rho}}.
$$

---

## 2. Equação para Vazão Real com Correções

Na prática, o escoamento através de uma placa de orifício sofre efeitos de contração do jato (vena contracta) e outras perdas, o que faz com que a área efetiva de escoamento seja menor que a área física do orifício. Para levar isso em conta, aplicamos os seguintes ajustes:

1. **Área do Orifício:**  
   Se o diâmetro do orifício é $d$, a área física é
   $$
   A = \frac{\pi d^2}{4}.
   $$
   Como o orifício é parte de uma tubulação com diâmetro $D$, define-se a razão
   $$
   \beta = \frac{d}{D}.
   $$

2. **Correção pela Contração do Jato:**  
   Estudos experimentais indicam que a vazão teórica deve ser corrigida por um fator que depende de $\beta$. Uma correção comum é incorporar o termo $(1-\beta^4)$ no denominador, ajustando a velocidade efetiva de escoamento.

3. **Coeficiente de Descarga e Fator de Expansibilidade:**  
   Para compensar as perdas reais (devido à turbulência, efeitos de instalação, etc.), introduz-se o coeficiente de descarga $C_d$ (ou base $C$). Para fluidos compressíveis, aplica-se também o fator de expansibilidade $\varepsilon$ (que é 1 para líquidos e menor que 1 para gases).

Portanto, a vazão volumétrica real é dada por:
$$
Q = C \cdot \varepsilon \cdot A \cdot \sqrt{\frac{2\Delta P}{\rho (1-\beta^4)}}.
$$
Quando outros fatores de correção são considerados (como o tipo de tomadas, condições de instalação, material da tubulação e tipo de orifício), define-se:
$$
C_{\text{eff}} = C \cdot K_{\text{tap}} \cdot K_{\text{inst}} \cdot K_{\text{material}} \cdot K_{\text{orifice}}.
$$
Substituindo, obtemos a equação final:
$$
Q = C_{\text{eff}} \cdot \varepsilon \cdot A \cdot \sqrt{\frac{2\Delta P}{\rho (1-\beta^4)}}.
$$

---

## 3. Método Iterativo para Dimensionamento de Placa de Orifício

O objetivo prático é encontrar o diâmetro do orifício $d$ (ou a razão $\beta$) que atenda à vazão volumétrica desejada $Q_{\text{desired}}$. Para isso, definimos a função:
$$
f(\beta) = C_{\text{eff}} \cdot \varepsilon \cdot \frac{\pi (\beta D)^2}{4} \cdot \sqrt{\frac{2\Delta P}{\rho (1-\beta^4)}} - Q_{\text{desired}} = 0.
$$
Encontrar a raiz de $f(\beta)$ equivale a determinar o valor de $\beta$ que satisfaça a condição de vazão.

### Método da Bissecção

O método da bissecção é aplicado da seguinte forma:

>>> 1. **Definição do Intervalo:**  
Escolhe-se um intervalo $[\beta_{\text{min}}, \beta_{\text{max}}]$ onde a função $f(\beta)$ muda de sinal. Para placas de orifício, normalmente utiliza-se um intervalo de 0.25 a 0.72.

>>> 2. **Cálculo do Ponto Médio:**  
Calcula-se o ponto médio:
$$
\beta_{\text{mid}} = \frac{\beta_{\text{min}} + \beta_{\text{max}}}{2},
$$
e avalia-se $f(\beta_{\text{mid}})$.

>>> 3. **Critério de Parada:**  
Se $|f(\beta_{\text{mid}})|$ for menor que uma tolerância (por exemplo, $10^{-6}$), $\beta_{\text{mid}}$ é aceita como solução.

>>> 4. **Atualização do Intervalo:**  
Se $f(\beta_{\text{min}})$ e $f(\beta_{\text{mid}})$ tiverem sinais opostos, a raiz está entre $\beta_{\text{min}}$ e $\beta_{\text{mid}}$; caso contrário, está entre $\beta_{\text{mid}}$ e $\beta_{\text{max}}$.

>>> 5. **Iteração:**  
Repete-se o procedimento com o novo intervalo até atingir a precisão desejada.

Após determinar $\beta$, o diâmetro do orifício é calculado por:
$$
d = \beta \cdot D.
$$

---

## 4. Valores Genéricos Típicos para Referência

Para facilitar a aplicação prática, seguem valores típicos usados no dimensionamento de placas de orifício:

>>> - **Vazão Volumétrica Desejada ($Q_{\text{desired}}$):**  
>>>> - Gases: 0.01 a 0.1 Nm³/s  
>>>> - Líquidos: 0.001 a 0.1 m³/s  
>>>> - Vapores: 0.01 a 1.0 Nm³/s
>>>
>>> - **Diâmetro Interno da Tubulação ($D$):**  
>>>> - Pequenas tubulações: 0.025 a 0.15 m (1″ a 6″)  
>>>> - Médias: 0.15 a 0.6 m (6″ a 24″)
>>>
>>> - **Queda de Pressão ($\Delta P$):**  
>>>> - Geralmente entre 25 kPa e 100 kPa (0.25 a 1.0 bar)
>>>
>>> - **Densidade do Fluido ($\rho$):**  
>>>> - Gases: aproximadamente 1.0 a 1.2 kg/m³ (ar)  
>>>> - Líquidos: aproximadamente 1000 kg/m³ (água)  
>>>> - Vapores: cerca de 0.6 kg/m³ em condições de saturação
>>>
>>> - **Coeficiente de Descarga Base ($C$):**  
>>>> - Aproximadamente 0.61 para placas de orifício padrão
>>>
>>> - **Fator de Expansibilidade ($\varepsilon$):**  
>>>> - Líquidos: 1.0  
>>>> - Gases/Vapores: geralmente entre 0.90 e 0.98
>>>
>>> - **Distâncias a Montante e Jusante ($L_{\text{upstream}}$ e $L_{\text{downstream}}$):**  
>>>> - Recomenda-se pelo menos 10 diâmetros ($10D$) a montante e 5 diâmetros ($5D$) a jusante

---

## 5. Exemplo Prático

Considere os seguintes parâmetros para uma aplicação com líquido:
>>> - $Q_{\text{desired}} = 0.02\, \text{m}^3/\text{s}$
>>> - $D = 0.15\, \text{m}$
>>> - $\Delta P = 50\,000\, \text{Pa}$
>>> - $\rho = 1000\, \text{kg/m}^3$
>>> - $C = 0.61$
>>> - $\varepsilon = 1.0$
>>> - $L_{\text{upstream}} = 1.5\, \text{m}$ (aproximadamente $10D$)
>>> - $L_{\text{downstream}} = 0.75\, \text{m}$ (aproximadamente $5D$)
>>> - Tipo de tomadas: "flange"
>>> - Material: "steel"
>>> - Tipo de orifício: "concentrico"

A função a ser resolvida é:
$$
C_{\text{eff}} \cdot \varepsilon \cdot \frac{\pi (\beta D)^2}{4} \cdot \sqrt{\frac{2\Delta P}{\rho (1-\beta^4)}} - 0.02 = 0.
$$
Suponha que, após iterações via bissecção, encontre-se $\beta \approx 0.4271$. Assim, o diâmetro do orifício é:
$$
d = \beta \cdot D \approx 0.4271 \times 0.15\,\text{m} \approx 0.0641\,\text{m},
$$
ou seja, aproximadamente 64,1 mm.

---

## 6. Conclusão

A abordagem apresentada combina a fundamentação teórica da equação de Bernoulli – com as simplificações necessárias para um fluxo horizontal e sem perdas – com a aplicação prática de fatores de correção empíricos. O método iterativo, utilizando a bissecção, permite encontrar o valor de $\beta$ que satisfaça a vazão desejada e, consequentemente, determinar o diâmetro do orifício. Esta metodologia é amplamente utilizada em aplicações industriais, onde a precisão da medição de vazão é crítica e as condições reais de operação (como o tipo de tomadas, instalação, material e geometria do orifício) devem ser levadas em conta para obter resultados confiáveis.
