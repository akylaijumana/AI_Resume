"""
AI Resume Generator - Configuration
"""

# UI Color Scheme
COLORS = {
    'bg_gradient_start': '#0F172A',  # Dark blue
    'bg_gradient_end': '#1E293B',
    'accent_color': '#6366F1',  # Indigo
    'accent_hover': '#4F46E5',
    'card_bg': '#1E293B',
    'text_color': '#F1F5F9',
    'text_secondary': '#94A3B8',
    'success': '#10B981',
    'error': '#EF4444',
}

# Window Configuration
WINDOW_CONFIG = {
    'title': 'AI Resume Generator Pro',
    'width': 1100,
    'height': 800,
}

# AI Model Configuration
AI_CONFIG = {
    'model_name': 'facebook/bart-large-cnn',
    'max_input_length': 512,
    'max_output_length': 150,
    'temperature': 0.7,
}

