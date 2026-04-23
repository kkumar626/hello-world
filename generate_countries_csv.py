import csv

# List of countries with their capitals, currencies, and languages
countries = [
    {"Country": "United States", "Capital": "Washington, D.C.", "Currency": "USD", "Language": "English"},
    {"Country": "France", "Capital": "Paris", "Currency": "EUR", "Language": "French"},
    {"Country": "Japan", "Capital": "Tokyo", "Currency": "JPY", "Language": "Japanese"},
    {"Country": "Germany", "Capital": "Berlin", "Currency": "EUR", "Language": "German"},
    {"Country": "United Kingdom", "Capital": "London", "Currency": "GBP", "Language": "English"},
    {"Country": "Canada", "Capital": "Ottawa", "Currency": "CAD", "Language": "English/French"},
    {"Country": "Australia", "Capital": "Canberra", "Currency": "AUD", "Language": "English"},
    {"Country": "India", "Capital": "New Delhi", "Currency": "INR", "Language": "Hindi/English"},
    {"Country": "Brazil", "Capital": "Brasília", "Currency": "BRL", "Language": "Portuguese"},
    {"Country": "China", "Capital": "Beijing", "Currency": "CNY", "Language": "Mandarin"},
]

# Create and write to CSV file
with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Country", "Capital", "Currency", "Language"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for country in countries:
        writer.writerow(country)

print("CSV file 'countries.csv' has been created successfully.")