import sys
import time
import urllib.error
import urllib.request


def run_benchmark(url: str, iterations: int = 10) -> None:
    total_bytes = 0
    durations = []

    print(f"Запуск теста для: {url}")
    print(f"Количество последовательных запросов: {iterations}\n")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }

    for i in range(1, iterations + 1):
        req = urllib.request.Request(url, headers=headers)
        start_time = time.perf_counter()

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                elapsed = time.perf_counter() - start_time

                bytes_downloaded = len(data)
                total_bytes += bytes_downloaded
                durations.append(elapsed)

                print(
                    f"Запрос {i:2d}/{iterations}: "
                    f"{bytes_downloaded / (1024 * 1024):.2f} МБ за {elapsed:.3f} сек."
                )

        except urllib.error.URLError as e:
            print(f"\nОшибка при выполнении запроса {i}: {e}")
            sys.exit(1)

    total_time = sum(durations)
    avg_time = total_time / iterations
    total_mb = total_bytes / (1024 * 1024)
    speed_mbps = (total_bytes * 8) / (total_time * 1_000_000)

    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Среднее время запроса: {avg_time:.3f} сек.")
    print(
        f"Общий объем данных:    {total_mb:.2f} МБ ({total_bytes:,} байт)".replace(
            ",", " "
        )
    )
    print(f"Скорость скачивания:   {speed_mbps:.2f} Мбит/с")
    print("=" * 40)


if __name__ == "__main__":
    target_url = input("Введите URL для тестирования: ").strip()

    if not target_url:
        print("Ошибка: URL не может быть пустым.")
        sys.exit(1)

    run_benchmark(target_url)
