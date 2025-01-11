import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

#validar as entradas
def validarEntradas(valores):
    for variavel, valor in valores.items():
        if variavel == 'acidez' and not (0 <= valor <= 10):
            print(f"Erro: 'acidez' deve estar entre 0 e 10, mas recebeu {valor}.")
            return False
        elif variavel == 'teorAlcoolico' and not (0 <= valor <= 15):
            print(f"Erro: 'teorAlcoolico' deve estar entre 0 e 15, mas recebeu {valor}.")
            return False
        elif variavel == 'acucar' and not (0 <= valor <= 10):
            print(f"Erro: 'acucar' deve estar entre 0 e 10, mas recebeu {valor}.")
            return False
    return True

#variaveis de entrada
acidez = ctrl.Antecedent(np.arange(0, 11, 1), 'acidez')
teorAlcoolico = ctrl.Antecedent(np.arange(0, 16, 1), 'teorAlcoolico')
acucar = ctrl.Antecedent(np.arange(0, 11, 1), 'acucar')

#variavel de saida
qualidade = ctrl.Consequent(np.arange(0, 11, 1), 'qualidade')

#pertinencia das entradas

#acidez
acidez['baixa'] = fuzz.trimf(acidez.universe, [0, 0, 5])
acidez['media'] = fuzz.trimf(acidez.universe, [3, 5, 7])
acidez['alta'] = fuzz.trimf(acidez.universe, [5, 10, 10])

#teor alcoolico
teorAlcoolico['baixo'] = fuzz.trimf(teorAlcoolico.universe, [0, 0, 7])
teorAlcoolico['medio'] = fuzz.trimf(teorAlcoolico.universe, [5, 8, 12])
teorAlcoolico['alto'] = fuzz.trimf(teorAlcoolico.universe, [10, 15, 15])

#açucar
acucar['baixo'] = fuzz.trimf(acucar.universe, [0, 0, 4])
acucar['medio'] = fuzz.trimf(acucar.universe, [2, 5, 8])
acucar['alto'] = fuzz.trimf(acucar.universe, [6, 10, 10])

#qualidade do vinho (saída)
qualidade['baixa'] = fuzz.trimf(qualidade.universe, [0, 0, 5])
qualidade['media'] = fuzz.trimf(qualidade.universe, [3, 5, 7])
qualidade['alta'] = fuzz.trimf(qualidade.universe, [5, 10, 10])

#regras do fuzzy
regra1 = ctrl.Rule(acidez['baixa'] & teorAlcoolico['alto'] & acucar['baixo'], qualidade['alta'])
regra2 = ctrl.Rule(acidez['media'] & teorAlcoolico['medio'] & acucar['medio'], qualidade['media'])
regra3 = ctrl.Rule(acidez['alta'] & teorAlcoolico['baixo'] & acucar['alto'], qualidade['baixa'])
regra4 = ctrl.Rule(acidez['media'] & teorAlcoolico['alto'] & acucar['baixo'], qualidade['alta'])
regra5 = ctrl.Rule(acidez['alta'] & teorAlcoolico['medio'] & acucar['medio'], qualidade['media'])
regra6 = ctrl.Rule(acidez['baixa'] & teorAlcoolico['baixo'] & acucar['alto'], qualidade['baixa'])

sistemaQualidadeVinho = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
simulacaoQualidade = ctrl.ControlSystemSimulation(sistemaQualidadeVinho)

#entrada dos valores para teste
valoresEntradas = {'acidez': 9, 'teorAlcoolico': 6, 'acucar': 9}

if validarEntradas(valoresEntradas):
    for variavel, valor in valoresEntradas.items():
        simulacaoQualidade.input[variavel] = valor

    #calcula a saida da qualidade 
    simulacaoQualidade.compute()

    #resultado + grafico
    qualidadeVinho = simulacaoQualidade.output['qualidade']
    print(f"A qualidade do vinho é: {qualidadeVinho:.2f}")
    qualidade.view(sim=simulacaoQualidade)
    plt.show()
else:
    print("variaveis de entrada fora dos limites de seu universo.")
