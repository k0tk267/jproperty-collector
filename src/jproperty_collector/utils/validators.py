def validate_prefecture_code(code: str) -> bool:
    if not code or len(code) != 2:
        return False
    return code.isdigit() and "01" <= code <= "47"
