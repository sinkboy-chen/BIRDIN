//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var recorder; //WebAudioRecorder object
var input; //MediaStreamAudioSourceNode  we'll be recording
var encodingType; //holds selected encoding for resulting audio (file)
var encodeAfterRecord = true; // when to encode

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

// var encodingTypeSelect = document.getElementById("encodingTypeSelect");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var analyzeButton = document.getElementById("analyzeButton");

var blobUrl;

var latitude, longitude;

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
analyzeButton.addEventListener("click", function () {
	analyzeRecording(blobUrl);
});

function startRecording() {
	console.log("startRecording() called");
	__clear();

	/*
			Simple constraints object, for more advanced features see
			https://addpipe.com/blog/audio-constraints-getusermedia/
		*/

	var constraints = { audio: true, video: false };

	/*
			We're using the standard promise based getUserMedia() 
			https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
		*/

	navigator.mediaDevices
		.getUserMedia(constraints)
		.then(function (stream) {
			__log(
				"getUserMedia() success, stream created, initializing WebAudioRecorder..."
			);

			/*
						create an audio context after getUserMedia is called
						sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
						the sampleRate defaults to the one set in your OS for your playback device
		    
					*/
			audioContext = new AudioContext();

			//update the format
			// document.getElementById("formats").innerHTML="Format: 2 channel "+encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value+" @ "+audioContext.sampleRate/1000+"kHz"

			//assign to gumStream for later use
			gumStream = stream;

			/* use the stream */
			input = audioContext.createMediaStreamSource(stream);

			//stop the input from playing back through the speakers
			//input.connect(audioContext.destination)

			//get the encoding
			encodingType = "mp3";

			//disable the encoding selector
			// encodingTypeSelect.disabled = true;

			recorder = new WebAudioRecorder(input, {
				workerDir: "/static/audio_js/", // must end with slash
				encoding: encodingType,
				numChannels: 2, //2 is the default, mp3 encoding supports only 2
				onEncoderLoading: function (recorder, encoding) {
					stopButton.disabled = true;
					recordButton.disabled = true;
					analyzeButton.disabled = true;
					// show "loading encoder..." display
					__log("Loading " + encoding + " encoder...");
				},
				onEncoderLoaded: function (recorder, encoding) {
					stopButton.disabled = false;
					recordButton.disabled = true;
					analyzeButton.disabled = true;
					// hide "loading encoder..." display
					__log(encoding + " encoder loaded");
				},
			});

			recorder.onComplete = function (recorder, blob) {
				stopButton.disabled = true;
				recordButton.disabled = false;
				analyzeButton.disabled = false;

				__log("Encoding complete");
				createDownloadLink(blob, recorder.encoding);
				// encodingTypeSelect.disabled = false;
			};

			recorder.setOptions({
				timeLimit: 25,
				encodeAfterRecord: encodeAfterRecord,
				ogg: { quality: 0.5 },
				mp3: { bitRate: 160 },
			});

			//start the recording process
			recorder.startRecording();

			__log("Recording started");
		})
		.catch(function (err) {
			//enable the record button if getUSerMedia() fails
			recordButton.disabled = false;
			stopButton.disabled = true;
			analyzeButton.disabled = true;
		});

	//disable the record button
	recordButton.disabled = true;
	analyzeButton.disabled = true;
}

function stopRecording() {
	console.log("stopRecording() called");

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//disable the stop button
	stopButton.disabled = true;
	recordButton.disabled = false;
	analyzeButton.disabled = false;

	//tell the recorder to finish the recording (stop recording + encode the recorded audio)
	recorder.finishRecording();

	__log("Recording stopped");
}

// function analyzeRecording(blobUrl) {
// 	stopButton.disabled = true;
// 	recordButton.disabled = true;
// 	analyzeButton.disabled = true;

// 	console.log("analyzeRecording() called");
// 	__log(blobUrl);

// 	// Fetch the Blob data
// 	fetch(blobUrl)
// 		.then((response) => response.blob())
// 		.then((blob) => {
// 			// Create FormData object
// 			var formData = new FormData();
// 			formData.append("audio", blob, "audio.mp3");

// 			// Replace 'your-api-endpoint' with the actual API endpoint
// 			const apiEndpoint = "/analyze";

// 			fetch(apiEndpoint, {
// 				method: "POST",
// 				body: formData,
// 			})
// 				.then((response) => response.json())
// 				.then((data) => {
// 					console.log("API response:", data);
// 					console.log("API response:", data);
// 					__log("API response:<br>", JSON.stringify(data, null, 2));
// 				})
// 				.catch((error) => {
// 					console.error("Error uploading MP3 file:", error);
// 				});
// 		})
// 		.catch((error) => {
// 			console.error("Error fetching Blob data:", error);
// 		});
// 	stopButton.disabled = true;
// 	recordButton.disabled = false;
// 	analyzeButton.disabled = true;
// }

function analyzeRecording(blobUrl) {
	stopButton.disabled = true;
	recordButton.disabled = true;
	analyzeButton.disabled = true;

	console.log("analyzeRecording() called");
	__log(blobUrl);

	// Fetch the Blob data
	fetch(blobUrl)
		.then((response) => response.blob())
		.then((blob) => {
			if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(function (position) {
					const latitude = position.coords.latitude;
					const longitude = position.coords.longitude;
					console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);

					// Create FormData object
					var formData = new FormData();
					formData.append("audio", blob, "audio.mp3");
					formData.append("lat", latitude);
					formData.append("lon", longitude);

					// Replace 'your-api-endpoint' with the actual API endpoint
					const apiEndpoint = "/analyze";

					fetch(apiEndpoint, {
						method: "POST",
						body: formData,
					})
						.then((response) => response.json())
						.then((data) => {
							console.log("API response:", data);
							console.log("API response:", data);
							__log("API response:<br>", JSON.stringify(data, null, 2));
						})
						.catch((error) => {
							console.error("Error uploading MP3 file:", error);
						});
						});
			} else {
				console.log("Geolocation is not supported by this browser.");
			}
		})
		.catch((error) => {
			console.error("Error fetching Blob data:", error);
		});
	stopButton.disabled = true;
	recordButton.disabled = false;
	analyzeButton.disabled = true;
}

function createDownloadLink(blob, encoding) {
	var url = URL.createObjectURL(blob);
	blobUrl = url;
	var au = document.createElement("audio");
	var li = document.createElement("li");
	var link = document.createElement("a");

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//link the a element to the blob
	link.href = url;
	link.download = new Date().toISOString() + "." + encoding;
	link.innerHTML = link.download;

	//add the new audio and a elements to the li element
	li.appendChild(au);
	li.appendChild(link);

	//add the li element to the ordered list
	recordingsList.appendChild(li);
}

//helper function
function __log(e, data) {
	log.innerHTML += e + " " + (data || "") + "\n";
}

//helper function
function __clear(e, data) {
	log.innerHTML = "";
	recordingsList.innerHTML = "";
}

// function getLocation() {
// 	return new Promise((resolve, reject) => {
// 		if (navigator.geolocation) {
// 			navigator.geolocation.getCurrentPosition(
// 				(position) => {
// 					const location = {
// 						latitude: position.coords.latitude,
// 						longitude: position.coords.longitude,
// 					};
// 					resolve(location);
// 				},
// 				(error) => {
// 					showError(error);
// 					reject(error);
// 				}
// 			);
// 		} else {
// 			const errorMessage = "Geolocation is not supported by this browser.";
// 			__log(errorMessage);
// 			reject(new Error(errorMessage));
// 		}
// 	});
// }

function showError(error) {
	switch (error.code) {
		case error.PERMISSION_DENIED:
			__log("User denied the request for Geolocation.");
			break;
		case error.POSITION_UNAVAILABLE:
			__log("Location information is unavailable.");
			break;
		case error.TIMEOUT:
			__log("The request to get user location timed out.");
			break;
		case error.UNKNOWN_ERROR:
			__log("An unknown error occurred.");
			break;
	}
}
