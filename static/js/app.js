$(document).ready(function () {
    const chatbox = $('#chatbox');
    const userInput = $('#user-input');
    const sendButton = $('#send-button');
    const recordButton = $('#record-button');
    const stopButton = $('#stop-button');

    let mediaRecorder;
    let audioChunks = [];

    sendButton.click(async function () {
        const message = userInput.val();
        if (message.trim() === '') return;

        appendMessage('User', message);
        userInput.val('');

        const response = await sendMessage(message);
        appendMessage('Bot', response.text);

        const audio = new Audio(response.audio + '?' + new Date().getTime());
        audio.play();
    });

    recordButton.click(function () {
        startRecording();
    });

    stopButton.click(function () {
        stopRecording();
    });

    function appendMessage(sender, message) {
        const messageElement = $('<div>').text(`${sender}: ${message}`);
        chatbox.append(messageElement);
        chatbox.scrollTop(chatbox[0].scrollHeight);
    }

    async function sendMessage(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        return response.json();
    }

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordButton.hide();
                stopButton.show();

                mediaRecorder.ondataavailable = function (event) {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async function () {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    audioChunks = [];
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'audio.webm');

                    const response = await fetch('/voice_chat', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    appendMessage('Bot', data.text);

                    const audio = new Audio(data.audio + '?' + new Date().getTime());
                    audio.play();

                    recordButton.show();
                    stopButton.hide();
                };
            });
    }

    function stopRecording() {
        mediaRecorder.stop();
    }
});
