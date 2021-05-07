import utility
import colorDetection

# Welcome to the main script!



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("...")
    print()
    print('Welcome to the gate detection algorithm!')
    print("...")
    print()
    utility.convertJPGtoNPY()
    print("...")
    print()
    utility.clearCsvFile()
    print("cornersFound csv file cleared!")
    print("...")
    print()
    print("Starting up the orangeDetection algorithm! May take up to 10 seconds. Don't forget to hold Enter to play the algorithm!")
    colorDetection.colorDetection()
    print("...")
    print()
    print("Code ran successfully. To run the alternative algorithms, run them from within the associated file.")



