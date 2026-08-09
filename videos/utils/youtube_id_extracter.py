import re

def extract_youtube_id(url: str) -> str | None:
    """
    Universal utility to extract the 11-character YouTube video ID 
    from any valid YouTube URL format.
    """
    if not url:
        return None
        
    # Clean whitespace strings or accidental formatting
    url = url.strip()
    
    # Universal regex pattern targeting:
    # - Standard watch links (youtube.com/watch?v=...)
    # - Shortened share links (youtu.be/...)
    # - Tracking links containing "?si=..." parameters
    # - Embed and legacy layouts (/embed/, /v/, /vi/)
    # - Privacy-enhanced layouts (youtube-nocookie.com)
    pattern = (
        r'(?:https?://)?'                    # Optional protocol
        r'(?:www\.)?'                        # Optional www sub-domain
        r'(?:youtube\.com|youtu\.be|youtube-nocookie\.com)' # Valid domains
        r'(?:/(?:[^/]+/.+/|(?:v|e(?:mbed)?|vi)/|watch\?.*v=)|/)' # Paths
        r'([^"&?/\s]{11})'                   # Capturing group: The 11-char ID
    )
    
    match = re.search(pattern, url)
    
    # Return the first captured group matching the 11-character limit
    return match.group(1) if match else None