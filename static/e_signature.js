document.addEventListener("DOMContentLoaded", function() {
    const signaturePad = new SignaturePad(document.getElementById('signatureCanvas'));

    // Handle the clear button
    document.getElementById('clearButton').addEventListener('click', function() {
        signaturePad.clear();
    });

    // Handle the save button
    document.getElementById('saveButton').addEventListener('click', function() {
        if (signaturePad.isEmpty()) {
            alert("Please provide a signature!");
        } else {
            const signatureData = signaturePad.toDataURL();
            document.getElementById('signatureResult').innerHTML = `<img src="${signatureData}" alt="Signature"/>`;
            saveSignature(signatureData); // Send the signature data to the backend
        }
    });

    // Function to send the signature to the backend (replace with your backend route)
    function saveSignature(signatureData) {
        const formData = new FormData();
        formData.append('signature', signatureData);
        
        // If you have the document upload functionality, append the file data as well
        const fileInput = document.getElementById('file');
        if (fileInput.files.length > 0) {
            formData.append('document', fileInput.files[0]);
        }
        
        // Send the signature data and document to the backend
        fetch('/save_signature', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert('Document successfully signed and saved!');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
