function searchInvoice() {
    var invoiceCode = document.getElementById('invoice-code').value;
    var purchaseDate = document.getElementById('purchase-date').value;
  
    if(!invoiceCode || !purchaseDate){
        alert("Kindly Fill All The Fields")
        return;
    }
    formdata={"invoiceno":invoiceCode,"dop":purchaseDate}
    
    fetch('/searchinvoice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formdata)
    })
    .then(response => response.blob())
    .then(blob => {
        if (blob.type != "application/json") {
            const imageUrl = URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = imageUrl;
            document.getElementById("img").src=imageUrl
            downloadLink.download = invoiceCode+'.jpg';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            alert("Invoice With Number "+ invoiceCode+" Downloaded")
        }
        else{
            alert("Something wrong....");
        }
    })
}

function goBack(){
    window.location.href = '/main';
}

function clearform(){
    document.getElementById("search-form").reset();
    document.getElementById("img").src="";
}