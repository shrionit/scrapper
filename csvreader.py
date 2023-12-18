import csv


def csv_to_array_of_dicts(csv_file):
    companies = []
    current_company = None

    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        headers = [e.strip() for e in next(reader)]

        for row in reader:
            if row[0]:  # Check if the first column (Company) has a value
                if current_company:
                    companies.append(current_company)

                current_company = {}
                for header, value in zip(headers, row):
                    value = value.strip()
                    if value and header != headers[-1]:
                        current_company[header] = value
                    else:
                        current_company[header] = []

                if row[-1]:
                    current_company[headers[-1]].append(row[-1])
            else:
                for header, value in zip(headers[1:], row[1:-1]):
                    value = value.strip()
                    if value:
                        current_company[header].append(value)

                if row[-1]:
                    current_company[headers[-1]].append(row[-1])

    if current_company:
        companies.append(current_company)

    return companies
