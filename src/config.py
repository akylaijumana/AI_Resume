"""
AI Resume Generator - Configuration
"""

# UI Color Scheme - Girly Theme
COLORS = {
    'bg_gradient_start': '#1a0a1e',  # Deep purple-black
    'bg_gradient_end': '#2d1b3d',
    'accent_color': '#E879F9',  # Bright purple-pink
    'accent_hover': '#D946EF',
    'card_bg': '#2d1b3d',
    'text_color': '#F1F5F9',
    'text_secondary': '#C4B5FD',  # Light lavender
    'success': '#F472B6',  # Pink
    'error': '#FB7185',  # Rose
    'pink': '#FF6B9D',
    'lavender': '#A78BFA',
    'mint': '#6EE7B7',
    'coral': '#FCA5A5',
}

# Window Configuration
WINDOW_CONFIG = {
    'title': 'AI Resume Generator Pro',
    'width': 950,
    'height': 750,
}

# AI Model Configuration
AI_CONFIG = {
    'model_name': 'facebook/bart-large-cnn',
    'max_input_length': 512,
    'max_output_length': 150,
    'temperature': 0.7,
}

