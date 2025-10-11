# run_all_tests.py
import os
import sys
import subprocess

def run_tests():

    # Папка для хранения allure-результатов
    allure_results_dir = "allure-results"

    # Создаем папку, если не существует
    os.makedirs(allure_results_dir, exist_ok=True)

    print("\n=== Запуск всех тестов проекта ===\n")
    # Формируем команду pytest
    cmd = [
        sys.executable, "-m", "pytest", "tests/",
        "-v",
        "--alluredir", allure_results_dir,
        "-s"
    ]

    # Запуск тестов
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n Тесты завершились с ошибками!")
    else:
        print("\n Все тесты выполнены успешно!")

    # После тестов можно сразу сгенерировать отчет allure (если установлен allure)
    generate_allure_report()

def generate_allure_report():

    allure_report_dir = "allure-report"
    print("\n=== Генерация Allure отчета ===\n")
    try:
        subprocess.run([
            "allure", "generate", "allure-results", "--clean", "-o", allure_report_dir
        ], check=True)
        print(f"Allure отчет успешно сгенерирован в папке '{allure_report_dir}'")
        print(f"Для просмотра локально выполните: allure open {allure_report_dir}")
    except FileNotFoundError:
        print("Allure не установлен или не найден в PATH. Пропускаем генерацию отчета.")
    except subprocess.CalledProcessError:
        print("Ошибка при генерации Allure-отчета.")

if __name__ == "__main__":
    run_tests()
