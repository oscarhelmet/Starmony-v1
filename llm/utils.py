def remove_code_blocks(text):
    """
    Removes Markdown code blocks from the given text.
    
    Args:
        text (str): The input text.
        
    Returns:
        str: The text with Markdown code blocks removed.
    """
    lines = text.split('\n')
    result = []
    in_code_block = False
    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
        elif not in_code_block:
            result.append(line)
    return '\n'.join(result)