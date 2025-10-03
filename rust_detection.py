import cv2
import numpy as np


def detect_rust(image_path, output_path=None):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to HSV color space (better for color segmentation)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    # Define rust color ranges in HSV
    # Orange-reddish colors typical for rust
    lower_rust = np.array([0, 100, 100])  # Lower bound of rust color
    upper_rust = np.array([30, 255, 255])  # Upper bound of rust color

    # Create mask for rust colors
    rust_mask = cv2.inRange(img_hsv, lower_rust, upper_rust)

    # Apply some morphological operations to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    rust_mask = cv2.morphologyEx(rust_mask, cv2.MORPH_OPEN, kernel)
    rust_mask = cv2.morphologyEx(rust_mask, cv2.MORPH_CLOSE, kernel)

    # Create output image with rust spots highlighted in blue
    result = img_rgb.copy()
    result[rust_mask > 0] = [0, 0, 255]  # Mark rust spots in red

    # Convert back to BGR for OpenCV display/save
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    if output_path:
        cv2.imwrite(output_path, result_bgr)

    # Display results with controlled window sizes
    # Original Image
    cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original Image", 800, 600)
    cv2.imshow("Original Image", img)

    # Rust Mask
    cv2.namedWindow("Rust Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Rust Mask", 800, 600)
    cv2.imshow("Rust Mask", rust_mask)

    # Result
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Result", 800, 600)
    cv2.imshow("Result", result_bgr)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Path to the image
    image_path = "82add70df6ab2854.jpg"
    output_path = "result_rust_detection.jpg"

    try:
        detect_rust(image_path, output_path)
    except Exception as e:
        print(f"Error: {e}")
