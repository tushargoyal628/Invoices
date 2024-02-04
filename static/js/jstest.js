function searchInvoice() {
    var invoiceCode = document.getElementById('invoice-code').value;
    var purchaseDate = document.getElementById('purchase-date').value;
  
    formdata={"invoiceno":invoiceCode,"dop":purchaseDate}
    // Send AJAX request to Flask endpoint
    fetch('/searchinvoice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formdata)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.Status)
    })
}