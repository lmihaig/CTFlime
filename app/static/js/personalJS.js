// Function to place default data in the edit modal
var edit = document.getElementById('editModal')
editModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget

    // Extract info from data-bs-rowvals attributes
    var data = button.getAttribute('data-bs-rowvals')

    // Save the data in the hiddenInfo form input
    hiddenBody = editModal.querySelector(".modal-body #hiddenInfo")
    hiddenBody.value = data

    // Decode the data from b64 and make it a json object
    data = atob(data)
    data = JSON.parse(data)

    // Put the data in the correct fields
    Object.keys(data).forEach(function (key) {
        modalBody = editModal.querySelector(".modal-body #" + String(key))
        modalBody.value = String(data[key])
    })

})


// Function to sort tables
function onPageReady() {
    new Tablesort(document.getElementById('main-table'));
}
document.addEventListener('DOMContentLoaded', onPageReady, false);
