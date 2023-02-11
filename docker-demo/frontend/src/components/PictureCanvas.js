import React, { useRef } from "react";

const PictureCanvas = () => {
    const canvasRef = useRef(null);

    const handleFileSelect = (evt) => {
        const allowedExtReg = /(\.jpg|\.jpeg|\.png)$/i;
        let files = evt.target.files;
        if (files && files.length) {
            let myFile = files[0];
            let myFileName = myFile.name;
            // check file ext
            if (allowedExtReg.exec(myFileName)) {
                let fr = new FileReader()
                fr.readAsDataURL(myFile);
                fr.onload = (evt) => {
                    handleImageLoad(evt.target.result);
                }
            }
        }

    };

    const handleImageLoad = (base64Image) => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.src = base64Image;
        img.onload = () => {
            const hRatio = canvas.width / img.width;
            const vRatio = canvas.height / img.height;
            const ratio = Math.min(hRatio, vRatio);
            const centerShift_x = (canvas.width - img.width * ratio) / 2;
            const centerShift_y = (canvas.height - img.height * ratio) / 2;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, img.width, img.height, centerShift_x, centerShift_y, img.width * ratio, img.height * ratio);
        };
    };

    return (
        <>
            <input type="file" onChange={handleFileSelect} />
            <br />
            <canvas ref={canvasRef} width={800} height={600} />
        </>
    );
};

export default PictureCanvas;