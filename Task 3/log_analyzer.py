import sys

def parse_log_line(line: str) -> dict:
    """
    Парсити рядок логу у словник з ключами: date, time, level, message.
    """
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        return {}
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': parts[3]
    }

def load_logs(file_path: str) -> list:
    """
    Завантажує лог-файл та повертає список словників.
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                log = parse_log_line(line)
                if log:
                    logs.append(log)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує логи за рівнем логування.
    """
    level = level.upper()
    return [log for log in logs if log['level'] == level]

def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів для кожного рівня логування.
    """
    counts = {}
    for log in logs:
        lvl = log['level']
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts

def display_log_counts(counts: dict):
    """
    Виводить статистику у вигляді таблиці.
    """
    print("Рівень логування | Кількість записів")
    print("-----------------|------------------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python log_analyzer.py <шлях_до_лог_файлу> [рівень]")
        sys.exit(1)
    file_path = sys.argv[1]
    logs = load_logs(file_path)
    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered = filter_logs_by_level(logs, level)
        for log in filtered:
            print(f"{log['date']} {log['time']} {log['level']} {log['message']}")
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

if __name__ == "__main__":
    main()

# Sample log data for testing
log_data = """2024-06-01 12:00:00 INFO Application started
2024-06-01 12:01:00 ERROR Failed to connect to database
2024-06-01 12:02:00 WARNING Low disk space
2024-06-01 12:03:00 DEBUG Checking system health
2024-06-01 12:04:00 INFO User logged out
"""

# Writing sample log data to a file
with open('sample_log.txt', 'w', encoding='utf-8') as f:
    f.write(log_data)