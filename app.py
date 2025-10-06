from rust_pattern_detector import PatternDetector


def main():
    # Inicializa o detector de padrões
    detector = PatternDetector()

    # Caminho para a imagem de referência para seleção de padrões
    reference_image = "82add70df6ab2854.jpg"

    # Caminho para a imagem alvo e saída
    target_image = "82add70df6ab2854.jpg"  # Pode ser a mesma imagem ou uma diferente
    output_path = "result_pattern_detection.jpg"

    try:
        # Passo 1: Selecionar padrões da imagem de referência
        print("Passo 1: Seleção de Padrões")
        print("------------------------")
        detector.select_patterns(reference_image)

        # Passo 2: Detectar padrões na imagem alvo
        print("\nPasso 2: Detecção de Padrões")
        print("------------------------")
        detector.detect_patterns(target_image, output_path)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
