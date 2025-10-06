import cv2
import numpy as np
from typing import List, Tuple


class PatternDetector:
    def __init__(self):
        self.patterns: List[Tuple[np.ndarray, np.ndarray]] = []
        self.tolerance = 30  # Faixa de tolerância para correspondência de cores

    def add_pattern(self, color: np.ndarray):
        """Adiciona um novo padrão de cor com faixas de tolerância."""
        lower_bound = np.clip(color - self.tolerance, 0, 255)
        upper_bound = np.clip(color + self.tolerance, 0, 255)
        self.patterns.append((lower_bound, upper_bound))

    def select_patterns(self, image_path: str):
        """Seleção interativa de padrões a partir da imagem de referência."""
        self.patterns = []  # Reinicia os padrões
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_viz = img_rgb.copy()

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # Obtém região 5x5 ao redor do ponto clicado
                region = img_rgb[
                    max(0, y - 2) : min(y + 3, img_rgb.shape[0]),
                    max(0, x - 2) : min(x + 3, img_rgb.shape[1]),
                ]

                # Calcula a cor média na região
                avg_color = np.mean(region, axis=(0, 1)).astype(int)
                print(
                    f"Selected pattern RGB values: R={avg_color[0]}, G={avg_color[1]}, B={avg_color[2]}"
                )

                # Adiciona o padrão
                self.add_pattern(avg_color)

                # Desenha retângulo ao redor da área selecionada
                cv2.rectangle(
                    img_viz,
                    (max(0, x - 2), max(0, y - 2)),
                    (min(x + 2, img_viz.shape[1]), min(y + 2, img_viz.shape[0])),
                    (255, 255, 255),
                    1,
                )
                cv2.imshow(
                    "Pattern Selection", cv2.cvtColor(img_viz, cv2.COLOR_RGB2BGR)
                )

        # Cria janela e configura callback do mouse
        cv2.namedWindow("Pattern Selection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Pattern Selection", 800, 600)
        cv2.setMouseCallback("Pattern Selection", mouse_callback)

        print(
            "Clique nas áreas para selecionar padrões de cor. Pressione 'q' quando terminar."
        )

        # Mostra a imagem e aguarda entrada do usuário
        cv2.imshow("Pattern Selection", cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        print(f"Total de padrões selecionados: {len(self.patterns)}")

    def detect_patterns(self, image_path: str, output_path: str = None):
        """Detecta os padrões selecionados na imagem alvo."""
        # Lê a imagem alvo
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = img_rgb.copy()

        # Se nenhum padrão foi selecionado, usa valores padrão de detecção de ferrugem
        if not self.patterns:
            print(
                "Nenhum padrão selecionado. Usando valores padrão de detecção de ferrugem..."
            )
            # Converte para o espaço de cores HSV (melhor para segmentação de cores)
            img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            # Valores padrão de ferrugem do arquivo rust_detection.py
            lower_rust = np.array([0, 100, 100])
            upper_rust = np.array([30, 255, 255])
            final_mask = cv2.inRange(img_hsv, lower_rust, upper_rust)
        else:
            # Cria uma máscara para detecção usando os padrões selecionados
            final_mask = np.zeros(img_rgb.shape[:2], dtype=np.uint8)

        # Verifica cada padrão
        for lower_bound, upper_bound in self.patterns:
            mask = cv2.inRange(img_rgb, lower_bound, upper_bound)
            final_mask = cv2.bitwise_or(final_mask, mask)

        # Aplica operações morfológicas para reduzir ruído
        kernel = np.ones((3, 3), np.uint8)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)

        # Destaca os padrões detectados em vermelho
        result[final_mask > 0] = [0, 0, 255]  # Marca padrões em vermelho

        # Converte de volta para BGR para exibição/salvamento no OpenCV
        result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

        if output_path:
            cv2.imwrite(output_path, result_bgr)

        # Exibe os resultados
        cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original Image", 800, 600)
        cv2.imshow("Original Image", img)

        cv2.namedWindow("Pattern Mask", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Pattern Mask", 800, 600)
        cv2.imshow("Pattern Mask", final_mask)

        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Result", 800, 600)
        cv2.imshow("Result", result_bgr)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


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
