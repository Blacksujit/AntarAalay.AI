"""
ControlNet Adapter for Layout Preservation

This module handles ControlNet conditioning for image-to-image transformation,
focusing on edge detection and structural preservation.

Key Features:
- Canny edge detection for layout preservation
- HED edge detection for softer boundaries
- Adaptive edge detection based on image content
- Resolution normalization for consistent processing
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Dict, Any
import logging
import io

logger = logging.getLogger(__name__)


class ControlNetAdapter:
    """
    Adapter for ControlNet conditioning in image-to-image transformation.
    
    Handles edge detection and preprocessing for layout preservation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ControlNet adapter.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.default_resolution = config.get('default_resolution', (512, 512))
        self.edge_detection_method = config.get('edge_method', 'canny')
        self.canny_low_threshold = config.get('canny_low_threshold', 50)
        self.canny_high_threshold = config.get('canny_high_threshold', 150)
        self.hed_threshold = config.get('hed_threshold', 0.5)
        
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for edge detection.
        
        Args:
            image_bytes: Input image as bytes
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            logger.debug(f"Preprocessed image shape: {image_array.shape}")
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise ValueError(f"Failed to preprocess image: {e}")
    
    def normalize_resolution(
        self, 
        image: np.ndarray, 
        target_resolution: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Normalize image resolution for consistent processing.
        
        Args:
            image: Input image as numpy array
            target_resolution: Target resolution (width, height)
            
        Returns:
            Resized image
        """
        if target_resolution is None:
            target_resolution = self.default_resolution
        
        height, width = image.shape[:2]
        target_width, target_height = target_resolution
        
        # Calculate aspect ratio
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height
        
        if abs(aspect_ratio - target_aspect_ratio) > 0.1:
            # Resize maintaining aspect ratio
            if aspect_ratio > target_aspect_ratio:
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                new_height = target_height
                new_width = int(target_height * aspect_ratio)
            
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Pad to target resolution
            pad_x = (target_width - new_width) // 2
            pad_y = (target_height - new_height) // 2
            
            padded = cv2.copyMakeBorder(
                resized, 
                pad_y, target_height - new_height - pad_y,
                pad_x, target_width - new_width - pad_x,
                cv2.BORDER_CONSTANT, value=(255, 255, 255)
            )
            
            return padded
        else:
            # Direct resize
            return cv2.resize(image, target_resolution, interpolation=cv2.INTER_AREA)
    
    def detect_canny_edges(self, image: np.ndarray) -> np.ndarray:
        """
        Detect edges using Canny edge detection.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Edge map as binary image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding based on image content
        median_intensity = np.median(blurred)
        
        # Adjust thresholds based on image content
        low_threshold = max(self.canny_low_threshold, int(median_intensity * 0.3))
        high_threshold = min(self.canny_high_threshold, int(median_intensity * 1.2))
        
        # Canny edge detection
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        
        # Morphological operations to clean up edges
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
        
        return edges
    
    def detect_hed_edges(self, image: np.ndarray) -> np.ndarray:
        """
        Detect edges using HED (Holistically-Nested Edge Detection).
        
        Note: This requires the HED model to be available.
        Falls back to Canny if HED is not available.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Edge map as binary image
        """
        try:
            # Try to use HED if available (requires additional dependencies)
            import cv2.dnn
            
            # Load HED model (this would need to be downloaded)
            # For now, fall back to Canny
            logger.warning("HED not available, falling back to Canny edge detection")
            return self.detect_canny_edges(image)
            
        except ImportError:
            logger.warning("OpenCV DNN not available, falling back to Canny edge detection")
            return self.detect_canny_edges(image)
    
    def detect_edges(self, image: np.ndarray, method: Optional[str] = None) -> np.ndarray:
        """
        Detect edges using the specified method.
        
        Args:
            image: Input image as numpy array
            method: Edge detection method ('canny' or 'hed')
            
        Returns:
            Edge map as binary image
        """
        if method is None:
            method = self.edge_detection_method
        
        if method.lower() == 'hed':
            return self.detect_hed_edges(image)
        else:
            return self.detect_canny_edges(image)
    
    def preprocess_for_controlnet(
        self, 
        image_bytes: bytes,
        target_resolution: Optional[Tuple[int, int]] = None,
        edge_method: Optional[str] = None
    ) -> bytes:
        """
        Preprocess image for ControlNet conditioning.
        
        Args:
            image_bytes: Input image as bytes
            target_resolution: Target resolution for processing
            edge_method: Edge detection method
            
        Returns:
            Processed edge map as bytes
        """
        try:
            # Preprocess image
            image = self.preprocess_image(image_bytes)
            
            # Normalize resolution
            if target_resolution:
                image = self.normalize_resolution(image, target_resolution)
            
            # Detect edges
            edges = self.detect_edges(image, edge_method)
            
            # Convert back to PIL Image
            edge_image = Image.fromarray(edges, mode='L')
            
            # Convert to bytes
            buffer = io.BytesIO()
            edge_image.save(buffer, format='PNG')
            edge_bytes = buffer.getvalue()
            
            logger.debug(f"Generated ControlNet edge map: {edges.shape}")
            return edge_bytes
            
        except Exception as e:
            logger.error(f"Error preprocessing for ControlNet: {e}")
            raise ValueError(f"Failed to preprocess for ControlNet: {e}")
    
    def get_controlnet_config(self, weight: float = 1.0) -> Dict[str, Any]:
        """
        Get ControlNet configuration for generation.
        
        Args:
            weight: ControlNet conditioning weight
            
        Returns:
            Configuration dictionary
        """
        return {
            'controlnet_conditioning_scale': weight,
            'guess_mode': False,
            'control_guidance_start': 0.0,
            'control_guidance_end': 1.0,
            'controlnet_type': 'canny' if self.edge_detection_method == 'canny' else 'hed'
        }
    
    def validate_edge_map(self, edge_bytes: bytes) -> Tuple[bool, Optional[str]]:
        """
        Validate generated edge map.
        
        Args:
            edge_bytes: Edge map as bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Load edge map
            edge_image = Image.open(io.BytesIO(edge_bytes))
            
            # Check if it's grayscale
            if edge_image.mode != 'L':
                return False, "Edge map must be grayscale"
            
            # Check dimensions
            if edge_image.size[0] < 256 or edge_image.size[1] < 256:
                return False, "Edge map resolution too small"
            
            # Check if edges are present (not all black or white)
            edge_array = np.array(edge_image)
            unique_values = np.unique(edge_array)
            
            if len(unique_values) < 2:
                return False, "Edge map contains no edges"
            
            if len(unique_values) == 2 and 0 in unique_values and 255 in unique_values:
                edge_ratio = np.sum(edge_array == 255) / edge_array.size
                if edge_ratio < 0.01:  # Less than 1% edges
                    return False, "Edge map has too few edges"
                if edge_ratio > 0.5:  # More than 50% edges
                    return False, "Edge map has too many edges"
            
            return True, None
            
        except Exception as e:
            return False, f"Failed to validate edge map: {e}"
    
    def get_edge_statistics(self, edge_bytes: bytes) -> Dict[str, Any]:
        """
        Get statistics about the generated edge map.
        
        Args:
            edge_bytes: Edge map as bytes
            
        Returns:
            Statistics dictionary
        """
        try:
            edge_image = Image.open(io.BytesIO(edge_bytes))
            edge_array = np.array(edge_image)
            
            unique_values = np.unique(edge_array)
            edge_pixels = np.sum(edge_array > 128)  # Assuming edges are bright
            total_pixels = edge_array.size
            edge_ratio = edge_pixels / total_pixels
            
            return {
                'resolution': edge_image.size,
                'unique_values': len(unique_values),
                'edge_pixel_count': int(edge_pixels),
                'total_pixel_count': int(total_pixels),
                'edge_ratio': float(edge_ratio),
                'mean_intensity': float(np.mean(edge_array)),
                'std_intensity': float(np.std(edge_array))
            }
            
        except Exception as e:
            logger.error(f"Error calculating edge statistics: {e}")
            return {}


class EdgeDetectionOptimizer:
    """
    Optimizes edge detection parameters based on image content.
    """
    
    @staticmethod
    def analyze_image_content(image: np.ndarray) -> Dict[str, Any]:
        """
        Analyze image content to optimize edge detection.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Analysis results
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate image statistics
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Estimate image complexity
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Determine if image is simple or complex
        complexity = 'simple' if laplacian_var < 100 else 'complex'
        
        # Determine if image is light or dark
        brightness = 'dark' if mean_intensity < 100 else 'light'
        
        return {
            'mean_intensity': mean_intensity,
            'std_intensity': std_intensity,
            'laplacian_variance': laplacian_var,
            'complexity': complexity,
            'brightness': brightness
        }
    
    @staticmethod
    def optimize_canny_parameters(analysis: Dict[str, Any]) -> Tuple[int, int]:
        """
        Optimize Canny parameters based on image analysis.
        
        Args:
            analysis: Image analysis results
            
        Returns:
            Tuple of (low_threshold, high_threshold)
        """
        mean_intensity = analysis['mean_intensity']
        complexity = analysis['complexity']
        
        if complexity == 'simple':
            # Simple images need lower thresholds
            low_threshold = max(30, int(mean_intensity * 0.2))
            high_threshold = min(120, int(mean_intensity * 0.8))
        else:
            # Complex images need higher thresholds
            low_threshold = max(50, int(mean_intensity * 0.3))
            high_threshold = min(200, int(mean_intensity * 1.2))
        
        return low_threshold, high_threshold
    
    def generate_canny_edge(self, image, target_resolution: int = 512) -> Image.Image:
        """
        Generate Canny edge map optimized for GTX 1650.
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            target_resolution: Target resolution (512 for 4GB VRAM)
            
        Returns:
            PIL Image containing Canny edge map
        """
        try:
            # Load image
            if isinstance(image, str):
                pil_image = Image.open(image)
            elif isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image)
            else:
                pil_image = image
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Resize to target resolution (512x512 for GTX 1650)
            pil_image = pil_image.resize(
                (target_resolution, target_resolution), 
                Image.Resampling.LANCZOS
            )
            
            # Convert to numpy array
            image_array = np.array(pil_image)
            
            # Fixed Canny parameters for consistency
            canny_low_threshold = 100
            canny_high_threshold = 200
            
            # Convert to grayscale
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(
                gray, 
                canny_low_threshold, 
                canny_high_threshold
            )
            
            # Convert back to PIL Image (RGB format for ControlNet)
            edge_image = Image.fromarray(edges, mode='L').convert('RGB')
            
            logger.debug(f"Generated Canny edge map: {edge_image.size}")
            
            return edge_image
            
        except Exception as e:
            logger.error(f"Failed to generate Canny edge map: {e}")
            raise
        
        return low_threshold, high_threshold
