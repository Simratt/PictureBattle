async function analyse() {
     // Start interval before fetch
     const waitingInterval = setInterval(() => {
        console.log("waiting");
    }, 3000);


    try{ 
        document.getElementById("analyse").disabled = true;
        document.getElementById("response").innerHTML = "Analyzing...";
        // Create FormData to send files
        const formData = new FormData();
        
        // Get both file inputs and add their files to formData
        const fileInput1 = document.getElementById('file-input-1');
        const fileInput2 = document.getElementById('file-input-2');
        
        if (fileInput1.files[0]) formData.append('image1', fileInput1.files[0]);
        if (fileInput2.files[0]) formData.append('image2', fileInput2.files[0]);

        const response = await fetch("/analyse", {
            method: "POST",
            body: formData  // Send the formData containing images
        });
        
        // Enhanced error handling for non-200 responses
        if (!response.ok) {
            // Try to get error details from response
            const errorText = await response.text();
            console.error('Server Error Details:', errorText);
            throw new Error(`Server Error (${response.status}): ${errorText || 'No error details available'}`);
        }
        
        // Try to parse the JSON response
        let data;
        try {
            data = await response.json();
        } catch (parseError) {
            throw new Error('Failed to parse server response as JSON');
        }
        
        document.getElementById("response").innerHTML = data.response;
        clearInterval(waitingInterval);
        console.log("analysis done");
    } catch(error) {
        console.error('Full error:', error);
        document.getElementById("response").innerHTML = `Error: ${error.message}`;
        clearInterval(waitingInterval);
    }
}

function selectImage(imageNumber) {
    const fileInput = document.getElementById(`file-input-${imageNumber}`);
    const preview = document.getElementById(`preview-${imageNumber}`);
    const placeholder = document.getElementById(`placeholder-${imageNumber}`);
    const container = document.getElementById(`image-container-${imageNumber}`);
    
    fileInput.onchange = function() {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                placeholder.style.display = 'none';
                container.style.border = 'none';
                container.style.padding = '0';
            }
            reader.readAsDataURL(file);
        }
    }
    
    fileInput.click();
} 