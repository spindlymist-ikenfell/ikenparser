from .. import config as cfg

def consume_matched_braces(first_line, lines):
    brace_count = 0
    block_lines = [first_line]

    while (line := next(lines, None)) is not None:
        if line.startswith("{"):
            spaces = ' ' * (cfg.INDENT_SPACES * brace_count)
            brace_count += 1
        elif line.startswith("}"):
            brace_count -= 1
            spaces = ' ' * (cfg.INDENT_SPACES * brace_count)
        else:
            spaces = ' ' * (cfg.INDENT_SPACES * brace_count)
        
        block_lines.append(spaces + line)

        if brace_count == 0:
            break
    
    return '\n'.join(block_lines)
