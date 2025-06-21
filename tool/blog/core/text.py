def clean_content(content: str) -> str:
    lines = content.splitlines()
    cleaned_lines = []
    
    prev_line_was_text = False
    prev_line_was_list = False
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
            continue
        
        is_list_item = stripped.startswith(('* ', '- ', '1. ', '2. ', '3. ', '4. ', '5. '))
        
        if is_list_item:
            if prev_line_was_text and not prev_line_was_list:
                if cleaned_lines[-1] != '':
                    cleaned_lines.append('')
            prev_line_was_list = True
        else:
            if prev_line_was_list and not prev_line_was_text:
                if cleaned_lines[-1] != '':
                    cleaned_lines.append('')
            prev_line_was_text = True
        
        cleaned_lines.append(stripped)
        prev_line_was_text = not is_list_item
    
    content = '\n'.join(cleaned_lines)
    
    sections = [s.strip() for s in content.split('\n\n') if s.strip()]
    content = '\n\n'.join(sections)
    
    return content