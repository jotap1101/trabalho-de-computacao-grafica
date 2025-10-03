# Detecção de Ferrugem em Folhas Utilizando Processamento Digital de Imagens

## Resumo

Este trabalho apresenta uma implementação de um sistema de detecção de ferrugem em folhas utilizando técnicas de processamento digital de imagens. O sistema foi desenvolvido em Python utilizando a biblioteca OpenCV, e emprega uma abordagem de duas etapas: análise interativa de padrões de cor e detecção automatizada de áreas afetadas pela ferrugem.

## 1. Introdução

A ferrugem em folhas é uma doença comum em plantas que pode causar sérios danos à agricultura. A detecção precoce dessa condição é crucial para o manejo adequado das culturas. Este trabalho propõe uma solução computacional para identificação automática de áreas afetadas pela ferrugem em folhas através de processamento de imagens.

## 2. Metodologia

### 2.1 Ferramentas Utilizadas

- Linguagem de Programação: Python 3
- Bibliotecas: OpenCV (cv2), NumPy
- Ambiente de Desenvolvimento: Visual Studio Code

### 2.2 Abordagem em Duas Etapas

#### 2.2.1 Etapa de Análise de Padrões (`pattern_analysis.py`)

O primeiro script implementa uma interface interativa que permite:

- Carregamento da imagem em formato RGB
- Seleção manual de regiões de interesse através de cliques do mouse
- Análise de regiões 5x5 pixels ao redor do ponto selecionado
- Cálculo da média de cores na região selecionada
- Visualização em tempo real das áreas selecionadas
- Exibição dos valores RGB de cada região analisada

```python
# Exemplo do cálculo da média de cores em uma região
avg_color = np.mean(region, axis=(0, 1)).astype(int)
```

#### 2.2.2 Etapa de Detecção Automática (`rust_detection.py`)

O segundo script implementa a detecção automática através de:

- Conversão da imagem para o espaço de cores HSV
- Definição de intervalos de cor para identificação da ferrugem
- Aplicação de máscara de cor para segmentação
- Operações morfológicas para redução de ruído
- Visualização dos resultados em três perspectivas diferentes

```python
# Definição dos limites de cor para detecção
lower_rust = np.array([0, 100, 100])
upper_rust = np.array([30, 255, 255])
```

### 2.3 Justificativa do Uso do Espaço de Cores HSV

O espaço de cores HSV (Hue, Saturation, Value) foi escolhido para a detecção por:

1. Separação mais efetiva entre informação de cor e luminosidade
2. Maior robustez a variações de iluminação
3. Melhor capacidade de segmentação para cores específicas

## 3. Resultados e Discussão

### 3.1 Processamento da Imagem

O sistema realiza as seguintes operações:

1. Conversão inicial de BGR para RGB
2. Conversão para HSV para segmentação
3. Aplicação de operações morfológicas:
   - Opening para remoção de ruídos
   - Closing para preenchimento de pequenas lacunas

```python
kernel = np.ones((3, 3), np.uint8)
rust_mask = cv2.morphologyEx(rust_mask, cv2.MORPH_OPEN, kernel)
rust_mask = cv2.morphologyEx(rust_mask, cv2.MORPH_CLOSE, kernel)
```

### 3.2 Visualização dos Resultados

O sistema gera três visualizações:

1. Imagem Original
2. Máscara de Detecção (em preto e branco)
3. Resultado Final (áreas de ferrugem destacadas em vermelho)

## 4. Conclusão

A metodologia implementada demonstrou-se eficaz na detecção de áreas afetadas pela ferrugem em folhas. A abordagem em duas etapas permite:

1. Calibração inicial através da análise interativa
2. Detecção automática baseada nos padrões identificados

A utilização do espaço de cores HSV, combinada com operações morfológicas, proporcionou resultados robustos na segmentação das áreas afetadas.

## 5. Referências

1. OpenCV Documentation. Disponível em: https://docs.opencv.org/
2. Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing (4th ed.).
3. Python NumPy Documentation. Disponível em: https://numpy.org/doc/
