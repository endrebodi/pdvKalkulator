import requests
import json
import time
import re

# prompt user for start date and end date
start_date = input("Unesite pocetni datum u formatu '2023-01-01' (bez navodnika) i pritisnite ENTER: ")
end_date = input("Unesite krajnji datum u formatu '2023-12-31' (bez navodnika) i pritisnite ENTER: ")

print("")
print("Preuzimam eFakture, molim sacekajte...")
print("")

# purchase tax
purchase_url = f'https://efaktura.mfin.gov.rs/api/publicApi/purchase-invoice/ids?dateFrom={start_date}&dateTo={end_date}'
headers = {
    'accept': 'text/plain',
    'ApiKey': 'EFAKTUREAPIKEY'
}
response = requests.post(purchase_url, headers=headers)
response_json = json.loads(response.text)
purchase_invoice_ids = response_json['PurchaseInvoiceIds']

time.sleep(1)  # Wait 1 second

if response.status_code == 200:
    total_tax_amount_purchase = 0
    for invoice_id in purchase_invoice_ids:
        time.sleep(1)  # Wait 1 second
        invoice_url = f"https://efaktura.mfin.gov.rs/api/publicApi/purchase-invoice/xml?invoiceId={invoice_id}"
        invoice_response = requests.get(invoice_url, headers=headers)
        if invoice_response.status_code == 200:
            invoice_xml = invoice_response.text
            tax_amount_match = re.search(r'<cac:TaxTotal>.*?<cbc:TaxAmount currencyID="RSD">([0-9.]+)</cbc:TaxAmount>', invoice_xml, re.DOTALL)
            if tax_amount_match:
                tax_amount = float(tax_amount_match.group(1))
                total_tax_amount_purchase += tax_amount
                print(f"Faktura: {invoice_id}, iznos PDV: {tax_amount}")
            else:
                print(f"Porez nije pronadjen za fakturu {invoice_id}")
        else:
            print(f"Greska preuzimanja fakture sa ID {invoice_id}. Broj greske: {invoice_response.status_code}")
else:
    print(f"Greska u preuzimanju faktura, broj greske: {response.status_code}")

# sales tax
sales_url = f'https://efaktura.mfin.gov.rs/api/publicApi/sales-invoice/ids?dateFrom={start_date}&dateTo={end_date}'
headers = {
    'accept': 'text/plain',
    'ApiKey': 'EFAKTUREAPIKEY'
}
response = requests.post(sales_url, headers=headers)
response_json = json.loads(response.text)
sales_invoice_ids = response_json['SalesInvoiceIds']

time.sleep(1)  # Wait 1 second

if response.status_code == 200:
    total_tax_amount_sales = 0
    for invoice_id in sales_invoice_ids:
        time.sleep(1)  # Wait 1 second
        invoice_url = f"https://efaktura.mfin.gov.rs/api/publicApi/sales-invoice/xml?invoiceId={invoice_id}"
        invoice_response = requests.get(invoice_url, headers=headers)
        if invoice_response.status_code == 200:
            invoice_xml = invoice_response.text
            tax_amount_match = re.search(r'<cac:TaxTotal>.*?<cbc:TaxAmount currencyID="RSD">([0-9.]+)</cbc:TaxAmount>', invoice_xml, re.DOTALL)
            if tax_amount_match:
                tax_amount = float(tax_amount_match.group(1))
                total_tax_amount_sales += tax_amount
                print(f"Faktura: {invoice_id}, iznos PDV: {tax_amount}")
            else:
                print(f"Porez nije pronadjen za fakturu {invoice_id}")
        else:
            print(f"Greska preuzimanja fakture sa ID {invoice_id}. Broj greske: {invoice_response.status_code}")
else:
    print(f"Greska u preuzimanju faktura, broj greske: {response.status_code}")

print("")
print(f"Ukupno PDV prodaja: {total_tax_amount_sales}")
print(f"Ukupno PDV nabavke: {total_tax_amount_purchase}")
print(f"Ukupno PDV: {total_tax_amount_sales - total_tax_amount_purchase}")
print("")