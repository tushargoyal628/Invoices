function addRow() {
    var container = document.querySelector('.lower-container');
    var newRow = document.createElement('div');
    newRow.className = 'row-lower-container';
    newRow.innerHTML = `
        <button class="plus-btn" onclick="addRow()">+</button>
        <input type="text" name="item[]" placeholder="Item" required>
        <input type="text" name="quantity[]" placeholder="Quantity" required oninput="calculateTotal(this)">
        <input type="text" name="price[]" placeholder="Price" required oninput="calculateTotal(this)">
        <input type="text" name="gst[]" placeholder="GST" required oninput="calculateTotal(this)">
        <input type="text" name="totalamount[]" placeholder="Total Amount" required readonly>
        <button class="delete-btn" onclick="removeRow(this)">-</button>

    `;
    container.appendChild(newRow);
}

function calculateTotal(inputElement) {
    var row = inputElement.parentNode;
    var quantity = parseFloat(row.querySelector('input[name="quantity[]"]').value) || 0;
    var price = parseFloat(row.querySelector('input[name="price[]"]').value) || 0;
    var gstPercentage = parseFloat(row.querySelector('input[name="gst[]"]').value) || 0;

    var totalAmount = quantity * price;
    var sgst = (totalAmount * gstPercentage) / 100 / 2;
    var cgst = sgst;
    var subtotal=totalAmount-sgst-cgst;

    row.querySelector('input[name="totalamount[]"]').value = totalAmount.toFixed(2);

    document.querySelector('#sgst').value = sgst.toFixed(2);
    document.querySelector("#cgst").value = cgst.toFixed(2);
    document.querySelector("#subtotal").value = subtotal.toFixed(2);

    updatedtotal();
}

function updatedtotal() {
    var rows = document.querySelectorAll('.row-lower-container');
    var totalAmount = 0;
    var totalSGST = 0;
    var totalCGST = 0;

    rows.forEach(function (row) {
        totalAmount += parseFloat(row.querySelector('input[name="totalamount[]"]').value) || 0;
        totalSGST += (row.querySelector('input[name="totalamount[]"]').value) * (row.querySelector('input[name="gst[]"]').value) / 200
        totalCGST = totalSGST
    });

    document.querySelector('#totalamount').value = totalAmount.toFixed(2);

    var totalsubtotal=totalAmount-totalCGST-totalSGST;

    document.querySelector('#sgst').value = totalSGST.toFixed(2);
    document.querySelector('#cgst').value = totalCGST.toFixed(2);
    document.querySelector('#subtotal').value = totalsubtotal.toFixed(2);

}
function removeRow(btn) {
    var row = btn.parentNode;
    row.parentNode.removeChild(row);
}

function submitForm() {
    // Get form values
    var customerName = document.getElementById("input-cust-name").value;
    var customerNum = document.getElementById("input-cust-no").value;
    var customerAddress = document.getElementById("input-cust-addr").value;
    var dateOfPurchase = document.getElementById("input-cust-date").value;
    var invoiceNumber = document.getElementById("input-invoice-num").value;
    var placeOfSupply = document.getElementById("input-place-of-supply").value;
    var supplyCode = document.getElementById("select-supply").value;
    var docType = document.getElementById("select-doc").value;
    var note1 = document.getElementById("notes1").value;
    var note2 = document.getElementById("notes2").value;
    var totalsgst = document.getElementById("sgst").value;
    var totalcgst = document.getElementById("cgst").value;
    var totaltotalamount = document.getElementById("totalamount").value;
    var totalsubamount = document.getElementById("subtotal").value;
    

    var items_data = document.querySelectorAll('.row-lower-container');
    var item_data = [];

    if(!customerName || !customerNum || !customerAddress || !dateOfPurchase || !placeOfSupply || !supplyCode || !docType || !totalcgst || !totalsgst || !totaltotalamount || !totalsubamount || !item_data){
        alert("Please fill in all required fields!");
        return;
    }

    items_data.forEach(function (row) {
        var itemName = row.querySelector('input[name="item[]"]').value;
        var quantity = row.querySelector('input[name="quantity[]"]').value;
        var price = row.querySelector('input[name="price[]"]').value;
        var gst = row.querySelector('input[name="gst[]"]').value;
        var totalAmount = row.querySelector('input[name="totalamount[]"]').value;

        item_data.push({
            itemName: itemName,
            quantity: quantity,
            price: price,
            gst: gst,
            totalAmount: totalAmount
        });
    });

    // Create an object with form data
    var formData = {
        customer_name: customerName,
        customer_num: customerNum,
        customer_addr: customerAddress,
        customer_dop: dateOfPurchase,
        customer_invoicenum: invoiceNumber,
        customer_pos: placeOfSupply,
        supplycode: supplyCode,
        doctype: docType,
        items: item_data,
        sgst: totalsgst,
        cgst: totalcgst,
        totalamount: totaltotalamount,
        totalsubamount: totalsubamount,
        note1: note1,
        note2: note2
    };
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data=> {
        console.log(data);
        const fileContent = data["File"];
        const invoiceNo = data["Invoice"];
        const blob = new Blob([new Uint8Array(atob(fileContent).split('').map(char => char.charCodeAt(0)))], { type: 'image/jpg' });
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = `${invoiceNo}.jpg`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        alert("File With Invoice Number "+invoiceNo+" Downloaded")
    })
    clearform();
}

function clearform(){
    document.getElementById("form").reset();
}

function searchform(){
    window.location.href = '/searchpage';
}