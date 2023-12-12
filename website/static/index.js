function buyCollection(species_name) {
    // Display a confirmation dialog
    var isConfirmed = confirm("Are you sure you want to buy the collection with $20?");

    // If the user confirms, make the POST request
    if (isConfirmed) {
        // Create a form element
        var form = document.createElement('form');

        // Set the form attributes (method and action)
        form.method = 'POST';
        form.action = '/buy_collection';  // Specify your POST endpoint here

        var input = document.createElement('input');
        input.style.display = 'none';
        input.type = 'text';
        input.name = 'species';
        input.value = species_name;

        // Append the input field to the form
        form.appendChild(input);

        // Append the form to the body
        document.body.appendChild(form);

        // Submit the form
        form.submit();
    }
}

function assignNickname(species_name, cost) {
    var newNickname = window.prompt("Enter the new nickname you want to assign:");
    if (newNickname !== null && newNickname!=="") {
        var isConfirmed = confirm(`Are you sure you want to assign the nickname '${newNickname}' for ${cost}?`);
        if (isConfirmed) {
            // Create a form element
            var form = document.createElement('form');
    
            // Set the form attributes (method and action)
            form.method = 'POST';
            form.action = '/assign_nickname';  // Specify your POST endpoint here
    
            var input1 = document.createElement('input');
            input1.style.display = 'none';
            input1.type = 'text';
            input1.name = 'species';
            input1.value = species_name;

            var input2 = document.createElement('input');
            input2.style.display = 'none';
            input2.type = 'text';
            input2.name = 'nickname';
            input2.value = newNickname;
    
            // Append the input field to the form
            form.appendChild(input1);
            form.appendChild(input2);
    
            // Append the form to the body
            document.body.appendChild(form);
    
            // Submit the form
            form.submit();
        }
    } else {
        alert("Canceled.");
    }
}
