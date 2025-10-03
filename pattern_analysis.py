import cv2
import numpy as np


def analyze_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Convert BGR to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create a copy for visualization
    img_viz = img_rgb.copy()

    # Define region of interest (ROI) handling function
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get 5x5 region around clicked point
            region = img_rgb[
                max(0, y - 2) : min(y + 3, img_rgb.shape[0]),
                max(0, x - 2) : min(x + 3, img_rgb.shape[1]),
            ]

            # Calculate average color in region
            avg_color = np.mean(region, axis=(0, 1)).astype(int)
            print(
                f"Selected region RGB values: R={avg_color[0]}, G={avg_color[1]}, B={avg_color[2]}"
            )

            # Draw rectangle around selected area
            cv2.rectangle(
                img_viz,
                (max(0, x - 2), max(0, y - 2)),
                (min(x + 2, img_viz.shape[1]), min(y + 2, img_viz.shape[0])),
                (255, 255, 255),
                1,
            )
            cv2.imshow("Image Analysis", cv2.cvtColor(img_viz, cv2.COLOR_RGB2BGR))

    # Create window and set mouse callback
    cv2.namedWindow("Image Analysis", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image Analysis", 800, 600)  # Define um tamanho fixo de 800x600
    cv2.setMouseCallback("Image Analysis", mouse_callback)

    # Show the image
    cv2.imshow("Image Analysis", cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Path to the image
    image_path = "82add70df6ab2854.jpg"
    try:
        analyze_image(image_path)
    except Exception as e:
        print(f"Error: {e}")
