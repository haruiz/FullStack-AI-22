navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

export default class Camera {
    constructor(videoElement,
                width=250,
                height=250) {
        this.widht = width;
        this.height = height;
        this.videoElement = videoElement;
        this.stream = null;
        this.isRunning = false;
    }
    async start(deviceId){
        try {
            const constraints = {
                audio: false,
                video: {
                    deviceId: deviceId,
                    //facingMode: 'user',
                    width: this.widht,
                    height: this.height
                }
            };
            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.videoElement.srcObject = this.stream;
            return new Promise((resolve) => {
                this.videoElement.onloadedmetadata = () => {
                    this.isRunning = true;
                    resolve(this.videoElement);
                };
            });
        }
        catch (e) {
            console.log("Error starting the camera");
        }
    }

    async takePicture(fileName){
        const canvas = document.createElement('canvas');
        canvas.width = this.widht;
        canvas.height = this.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoElement, 0, 0, this.widht, this.height);
        //canvas.toDataURL('image/png'); // base64
        return new Promise((resolve, reject)=> {
            return canvas.toBlob((blob) => {
                let file = new File([blob], fileName, { type: "image/jpeg" })
                resolve(file);
            });
        })
    }
    async stop(){
        const tracks = this.stream.getTracks();
        tracks.forEach((track)=>{
            track.stop();
        });
        this.videoElement.srcObject = null;
        this.isRunning = false;
    }
    static async devicesList() {
        try{
            let devices = [];
            const devicesList = await navigator.mediaDevices.enumerateDevices();
            for (let i = 0; i !== devicesList.length; ++i) {
                const deviceInfo = devicesList[i];
                if (deviceInfo.kind === 'videoinput'){
                    devices.push({
                        "id" : deviceInfo.deviceId,
                        "label": deviceInfo.label || `camera ${i}`
                    });
                }
            }
            return devices;
        }
        catch (e) {
            throw new Error("error listing the devices");
        }
    }
    static isSupported(){
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    }
}