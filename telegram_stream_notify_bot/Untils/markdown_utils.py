import re


def escape_markdown(text: str) -> str:
    """Экранирует специальные символы MarkdownV2"""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in special_chars else char for char in text)


def format_markdown(text: str) -> str:
    """Форматирует текст для MarkdownV2 (экранрование + обработка переносов)"""
    # Экранируем специальные символы
    escaped = escape_markdown(text)
    # Заменяем переносы строк на корректные для Markdown
    escaped = escaped.replace('\n', '\\n')
    return escaped


def validate_markdown(text: str) -> tuple[bool, str]:
    """Проверяет валидность MarkdownV2 синтаксиса (базовая проверка)"""
    # Простая проверка на незакрытые теги
    stack = []
    i = 0
    length = len(text)

    while i < length:
        if text[i] == '\\' and i + 1 < length:
            i += 2
            continue
        if text[i] in '*_~`':
            char = text[i]
            if char == '`':
                # Кодблок
                if text[i:i + 3] == '```':
                    i += 3
                    continue
                # Инлайн код
                if stack and stack[-1] == char:
                    stack.pop()
                else:
                    stack.append(char)
            else:
                if stack and stack[-1] == char:
                    stack.pop()
                else:
                    stack.append(char)
        i += 1

    if stack:
        return False, f"Незакрытые теги: {', '.join(stack)}"
    return True, "OK"