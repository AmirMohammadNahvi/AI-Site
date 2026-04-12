import sys

def summarize_traceback(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    last_lines = lines[-12:] if len(lines) > 12 else lines
    return "\n".join(last_lines)

def main():
    data = sys.stdin.read()
    print(summarize_traceback(data))

if __name__ == "__main__":
    main()