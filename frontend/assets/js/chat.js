$(document).ready(function() {
    // Function to upload a photo
    function uploadPhoto() {
        var fileInput = document.getElementById('uploaded_file');
        var customLabelsInput = document.getElementById('custom_labels');
        var file = fileInput.files[0];

        if (!file) {
            console.error('No file selected!');
            return;
        }

        var fileName = file.name;
        var customLabels = customLabelsInput.value.trim().split(/\s+/);
        console.log("labels being associated with the image", customLabels.join(','))

        var headers = {
            'Content-Type': file.type,
            'x-amz-meta-customLabels': customLabels.join(',')
        };

        var url = 'https://ntfe0po5jd.execute-api.us-east-1.amazonaws.com/dev/photos/' + fileName;

        axios.put(url, file, { headers: headers })
            .then(response => {
                console.log('Upload successful:', response);
                alert("Upload successful!");
            })
            .catch(error => {
                console.error('Error during upload:', error);
                alert("Upload failed!");
            });
    }

    // function uploadPhoto() {
    //     var fileInput = document.getElementById('uploaded_file');
    //     var customLabelsInput = document.getElementById('custom_labels');
    //     var filePath = fileInput.value.split("\\");
    //     var fileName = filePath[filePath.length - 1];
    //     var fileExtension = fileName.split(".")[1].toLowerCase();
    
    //     // Validate the file extension
    //     if (!fileInput.value || !['png', 'jpg', 'jpeg'].includes(fileExtension)) {
    //         alert("Please upload a valid .png/.jpg/.jpeg file!");
    //         return; // Exit the function if the file is not valid
    //     }
    
    //     var customLabelsValue = customLabelsInput.value.trim();
    //     console.log(fileName);
    //     console.log(customLabelsValue);
    
    //     var reader = new FileReader();
    //     var file = fileInput.files[0];
        
    //     // Clear the file input
    //     fileInput.value = "";
    
    //     console.log('File : ', file);
    //     console.log('File type :', file.type);
    //     console.log("Filepath", fileName);
    //     console.log("Extension: ", fileExtension);
    
    //     getBase64(file).then((data) => {
    //         console.log(data);
    
    //         var params = {
    //             key: fileName, // Use the variable fileName which is the extracted name from the path
    //             'Content-Type': 'application/json',
    //             //'ContentEncoding': 'base64',
    //             'x-amz-meta-customLabels': customLabelsValue, // Use the trimmed value from the input
    //             //Accept: 'image/*',
    //         };
            
    //         //var body = data;
    //         var additionalParams = {};

    //         var body = JSON.stringify({
    //             file: data,
    //             "x-amz-meta-customLabels": customLabelsValue // If you have custom labels to send
    //           });
            
    //         sdk.photosKeyPut(params, body, additionalParams)
    //         .then(function (res) {
    //             if (res.status == 200) {
    //                 console.log('success OK');
    //                 alert("Photo Uploaded Successfully");
    //             } else {
    //                 console.log('Error status:', res.status);
    //                 alert("Upload failed");
    //             }
    //         }).catch(function (error) {
    //             console.error('Upload error:', error);
    //             alert("Upload Error encountered");
    //         });
    //     }).catch(function (error) {
    //         console.error('Error converting file to base64:', error);
    //         alert("Could not read the file");
    //     });
    // }
    
    // // Assuming getBase64 is defined like this:
    // function getBase64(file) {
    //     return new Promise((resolve, reject) => {
    //       const reader = new FileReader();
    //       reader.readAsDataURL(file);
    //       // reader.onload = () => resolve(reader.result)
    //       reader.onload = () => {
    //         let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
    //         if (encoded.length % 4 > 0) {
    //           encoded += '='.repeat(4 - (encoded.length % 4));
    //         }
    //         resolve(encoded);
    //       };
    //       reader.onerror = (error) => reject(error);
    //     });
    //   }
    

    // Click to trigger photo upload
    $('#upload_files').click(uploadPhoto);

    // Function to handle search
    function insertMessage() {
        var msg = $('#searchQuery').val().trim();
        if (msg === '') {
            return false;
        }

        // Assuming callLexApi is a function to call your API gateway and fetch search results
        callLexApi(msg)
            .then((response) => {
                console.log(response.data);
                var data = response.data;
                var searchResultsElement = document.getElementById("searchResults");

                searchResultsElement.innerHTML = "";
        
                if (data === 'No Results found') {
                    searchResultsElement.innerHTML = '<p>No results found.</p>';
                    return;
                }
        
                data.forEach((imagePath) => {
                    var figure = document.createElement('figure');
                    var img = document.createElement('img');
                    img.src = `https://photos-bucket-s3.s3.us-east-2.amazonaws.com/${imagePath}`;
                    figure.appendChild(img);
                    searchResultsElement.appendChild(figure);
                });
            })
            .catch((error) => {
                console.error('An error occurred', error);
                searchResultsElement.innerHTML = '<p>Error loading results. Please try again.</p>';
            });
    }

    // Click event to trigger search
    $('#search').click(insertMessage);

    // Function call to AWS API Gateway
    function callLexApi(message) {
        var params = {
            'q': message
        };
        return sdk.searchGet(params, {}, {});
    }
});
