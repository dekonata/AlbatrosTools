import csv


def get_club_rounds(csv_file, club):
    with open(csv_file) as file:
        reader = csv.reader(file)
        for row in reader:
            if club.upper() in row[1]:
                return(row[5])
        return('Club not found')


if __name__ == '__main__':
	print(get_club_rounds('2020_Rounds_Report.csv', 'Kragga'))

