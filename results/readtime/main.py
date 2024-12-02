from workbench.readtime.calculator import ReadTimeCalculator

def main():
    calculator = ReadTimeCalculator()
    content = "This is a sample content for reading time estimation."
    format = "plain"
    wpm = 265
    reading_time = calculator.estimate_reading_time(content, format, wpm)
    print(f"Estimated Reading Time: {reading_time} minutes")

if __name__ == "__main__":
    main()