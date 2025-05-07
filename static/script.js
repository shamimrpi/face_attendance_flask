const video = document.getElementById('video');
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; });

function capture() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const dataURL = canvas.toDataURL('image/jpeg');
    
    fetch('/mark_attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('response').innerText = data.message;
    });
}
