"""
Security utilities for input sanitization and validation.
"""
import re
import html
from typing import Optional


def sanitize_html(text: Optional[str]) -> Optional[str]:
    """
    Remove HTML tags and escape special characters to prevent XSS attacks.
    
    Args:
        text: Input string that may contain HTML
        
    Returns:
        Sanitized string with HTML tags removed and special chars escaped
    """
    if not text:
        return text
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special HTML characters
    text = html.escape(text)
    
    # Remove common XSS patterns
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def validate_length(text: Optional[str], max_length: int = 10000) -> Optional[str]:
    """
    Validate and truncate text to prevent DoS attacks via large payloads.
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Truncated text if too long
    """
    if not text:
        return text
    
    if len(text) > max_length:
        return text[:max_length]
    
    return text


def sanitize_and_validate(text: Optional[str], max_length: int = 10000) -> Optional[str]:
    """
    Combined sanitization and validation.
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized and validated text
    """
    if not text:
        return text
    
    # First validate length to prevent processing huge strings
    text = validate_length(text, max_length)
    
    # Then sanitize
    text = sanitize_html(text)
    
    return text
