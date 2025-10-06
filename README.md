# Identificação de Padrões em Imagens Utilizando Processamento Digital

## Resumo

Este trabalho apresenta o desenvolvimento de um sistema de identificação de padrões em imagens utilizando técnicas de processamento digital. O sistema foi implementado em Python com a biblioteca OpenCV, empregando uma abordagem híbrida que combina análise interativa de padrões de cor com detecção automatizada. O sistema permite tanto a identificação manual de padrões através de uma interface interativa quanto a utilização de valores pré-definidos para detecção automática.

## 1. Introdução

A identificação de padrões em imagens digitais é uma área fundamental do processamento digital de imagens, com aplicações em diversos campos como controle de qualidade, diagnóstico médico e análise agrícola. Este trabalho propõe uma solução computacional flexível que permite tanto a análise interativa de padrões quanto a detecção automatizada baseada em parâmetros pré-definidos.

## 2. Metodologia

### 2.1 Ferramentas Utilizadas

- Linguagem de Programação: Python 3
- Bibliotecas: OpenCV (cv2), NumPy
- Ambiente de Desenvolvimento: Visual Studio Code

### 2.2 Arquitetura do Sistema

O sistema foi reorganizado em dois arquivos principais que trabalham em conjunto:

#### 2.2.1 Módulo Principal (`rust_pattern_detector.py`)

Implementa a classe `PatternDetector` que contém toda a lógica de processamento:

- Conversão e análise no espaço de cores HSV
- Interface interativa para seleção de padrões
- Sistema de tolerância específico para cada canal HSV
- Detecção de padrões e processamento morfológico
- Visualização e salvamento dos resultados

Principais características:

- Tolerâncias independentes para Hue (10), Saturação (50) e Valor (50)
- Processamento totalmente em HSV para maior robustez
- Mecanismo de fallback para detecção automática de ferrugem
- Interface visual interativa com feedback em tempo real

#### 2.2.2 Módulo de Aplicação (`app.py`)

Implementa a interface de usuário e o fluxo principal da aplicação:

- Inicialização do detector de padrões
- Configuração dos caminhos de entrada e saída
- Gerenciamento do fluxo de execução
- Tratamento de exceções

### 2.3 Metodologias de Detecção

#### 2.3.1 Detecção Interativa em HSV

- Seleção manual de áreas de interesse
- Cálculo automático de intervalos de tolerância específicos para HSV
- Armazenamento de múltiplos padrões
- Combinação de padrões via operações lógicas

```python
def add_pattern(self, color: np.ndarray):
    lower_bound = np.array([
        max(0, color[0] - self.h_tolerance),
        max(0, color[1] - self.s_tolerance),
        max(0, color[2] - self.v_tolerance)
    ])
    upper_bound = np.array([
        min(179, color[0] + self.h_tolerance),  # Hue vai de 0 a 179 no OpenCV
        min(255, color[1] + self.s_tolerance),
        min(255, color[2] + self.v_tolerance)
    ])
    self.patterns.append((lower_bound, upper_bound))
```

#### 2.3.2 Detecção Automatizada

- Utilização de intervalos HSV pré-definidos para ferrugem
  - Hue: 0-30
  - Saturação: 100-255
  - Valor: 100-255
- Ativação automática na ausência de padrões selecionados
- Otimização específica para detecção de ferrugem

### 2.4 Pipeline de Processamento

O sistema implementa uma pipeline de processamento otimizada em HSV:

1. Conversão de espaços de cores:
   - BGR → HSV para processamento
   - BGR → RGB apenas para visualização
2. Seleção e análise de padrões:
   - Amostragem de regiões 5x5 pixels
   - Cálculo de médias no espaço HSV
   - Definição de intervalos com tolerâncias específicas para cada canal
3. Detecção de padrões:
   - Criação de máscaras individuais para cada padrão
   - Combinação de máscaras via operações OR
   - Operações morfológicas para redução de ruído
4. Visualização de resultados:
   - Exibição da imagem original
   - Visualização da máscara de detecção
   - Resultado final com áreas destacadas em vermelho

## 3. Resultados e Discussão

### 3.1 Interface do Usuário

O sistema oferece uma interface intuitiva e eficiente:

- Seleção visual de padrões com feedback imediato
- Exibição dos valores HSV das áreas selecionadas
- Visualização em múltiplas perspectivas
- Encerramento automático ao fechar qualquer janela de resultado
- Controle interativo do processo via mouse e teclado

### 3.2 Adaptabilidade e Robustez

O sistema demonstra alta flexibilidade e robustez através de:

- Utilização otimizada do espaço de cores HSV
- Tolerâncias específicas para cada canal (H, S, V)
- Suporte a múltiplos padrões de cor
- Fallback automático para detecção de ferrugem
- Processamento morfológico adaptativo

### 3.3 Visualização dos Resultados

São geradas três visualizações distintas:

1. Imagem Original
2. Máscara de Detecção
3. Resultado com Áreas Destacadas

## 4. Conclusão

A solução desenvolvida demonstrou-se eficaz e flexível, oferecendo:

- Interface intuitiva para análise manual
- Detecção automática robusta
- Combinação eficiente de abordagens
- Resultados visuais claros e informativos

A metodologia híbrida implementada permite tanto a análise detalhada de padrões específicos quanto a detecção automatizada eficiente, adaptando-se a diferentes necessidades e contextos de uso.

## 5. Referências

1. OpenCV Documentation. https://docs.opencv.org/
2. Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing (4th ed.).
3. Python NumPy Documentation. https://numpy.org/doc/
4. Szeliski, R. (2010). Computer Vision: Algorithms and Applications.
5. Parker, J. R. (2016). Algorithms for Image Processing and Computer Vision.
