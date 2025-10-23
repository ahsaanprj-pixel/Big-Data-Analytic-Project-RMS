
console.log('scripts.js loaded successfully');

// Function to dynamically add a product row to the order form
// Example: Adds a row with a dropdown for menu items and a quantity input
function addProductRow(menuItems) {

    console.log('Adding product row with menu items:', menuItems);
   
    const container = document.getElementById('products-container');
    
    if (!container) {
        console.error('Error: products-container not found');
        return;
    }
    // new div for product row
    const row = document.createElement('div');
    row.className = 'product-row';
    
    let options = '<option value="">Select a meal</option>';
    // Validate and populate dropdown with menu items
    if (menuItems && Array.isArray(menuItems)) {
        menuItems.forEach(item => {
            
            options += `<option value="${item}">${item}</option>`;
        });
    } else {
        console.error('Error: menuItems is not a valid array');
    }
    
    row.innerHTML = `
        <select name="product_name" class="form-control" onchange="updateStatus(this)" required>
            ${options}
        </select>
        <input type="number" name="quantity" min="1" max="100" value="1" class="form-control" required>
        <span class="status">Choosing</span>
        <button type="button" class="btn btn-danger" onclick="deleteRow(this)"><i class="fas fa-trash"></i></button>
    `;
    
    container.appendChild(row);
}

// update status based on dropdown selection
function updateStatus(selectElement) {
    
    const selectedValue = selectElement.value;
    console.log('Status updated for product:', selectedValue);
    // Find the status span in the same row
    const statusSpan = selectElement.parentElement.querySelector('.status');
    // Update status text and color based on selection
    if (statusSpan) {
        if (selectedValue !== '') {
            // Example: Set to "Ordered" and green color for valid selection
            statusSpan.textContent = 'Ordered';
            statusSpan.style.color = '#28a745'; // Green for Ordered
        } else {
            // gray color for no selection
            statusSpan.textContent = 'Choosing';
            statusSpan.style.color = '#6c757d'; // Gray for Choosing
        }
    } else {
        console.error('Error: status span not found');
    }
}


function deleteRow(button) {
    console.log('Delete button clicked for row');
  
    button.parentElement.remove();
}
