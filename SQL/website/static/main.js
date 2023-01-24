function deleteRecord(event) {
    var id = event.target.dataset.id;
    if (confirm("Czy na pewno chcesz usunąć ten portfel? Twoje saldo z tego portfela zostanie przekazane na głodne pieski w schroniskach.")) {
      // Make an AJAX request to delete the record
      return fetch('/deletep', {
        method: 'DELETE',
        body: JSON.stringify({id: id}),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          location.reload();
        } else {
          // Handle error
        }
      })
      .catch(error => console.error('Error:', error));
    }
  }
