export function saveImageToClipboard(imageBase64) {
    const base64Data = imageBase64.replace(/^data:image\/png;base64,/, '');
    const binaryString = window.atob(base64Data);
    const byteArray = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        byteArray[i] = binaryString.charCodeAt(i);
    }
    const imageBlob = new Blob([byteArray], { type: 'image/png' });

    try {
        navigator.clipboard.write([
            new ClipboardItem({
                'image/png': imageBlob
            })
        ]);
    } catch (error) {
        console.error(error);
    }
}

export function downloadImage(imageBase64, fileName) {
    const base64Data = imageBase64.replace(/^data:image\/png;base64,/, '');
    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + base64Data;
    link.download = fileName;

    // Simulate a click on the link to start the download
    link.click();
}