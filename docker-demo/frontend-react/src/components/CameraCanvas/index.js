import React, {useEffect, useRef, useState} from "react";
import Camera from "../Camera";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import IconButton from '@mui/material/IconButton';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import VideoCamIcon from '@mui/icons-material/Videocam';
import CameraIcon from '@mui/icons-material/Camera';
import SendIcon from '@mui/icons-material/Send';
import Grid from "@mui/material/Grid";
import ButtonGroup from "@mui/material/ButtonGroup";
import moment from "moment";
import styles from "./index.module.css";
import Paper from "@mui/material/Paper";


const CameraPicker = (props) => {
    const [disabled, setDisabled] = useState(true);
    const [devices, setDevices] = useState([]);
    const [deviceId, setDeviceId] = useState(null);
    const {onChange} = props;

    useEffect(() => {
        async function getDevices() {
            return await Camera.devicesList();
        }

        getDevices().then(devicesList => {
            setDevices(devicesList);
            setDisabled(false);
        });
    }, []);

    const handleChange = (evt) => {
        setDeviceId(evt.target.value);
        onChange(evt.target.value);
    }


    return (
        <FormControl variant="standard" className={styles.cameraPicker}>
            <InputLabel id="devicesSelectLabelId">Device</InputLabel>
            <Select
                labelId="devicesSelectLabelId"
                value={deviceId}
                disabled={disabled}
                onChange={handleChange}
                label="Device">
                {devices.map((device) => {
                    return (
                        <MenuItem key={device.id} value={device.id}>{device.label}</MenuItem>
                    )
                })}

            </Select>
        </FormControl>
    )
}
const CameraCapture = (props) => {

    const {width = 800, height = 600} = props;
    const videoRef = useRef();

    let cameraRef = useRef(null)
    let isCameraLive = useRef(false);


    const handleDeviceChange = async (selectedDeviceId) => {
        if (cameraRef.current) {
            await cameraRef.current.stop();
        }
        cameraRef.current = new Camera(videoRef.current, width, height);
        await cameraRef.current.start(selectedDeviceId);
        isCameraLive.current = true; // camera is live

    }

    const sendPictureToServer = async (image) => {
        const formData = new FormData();
        formData.append("image", image);
        formData.append("label", "test");
        const response = await fetch("http://localhost:8000/images", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        console.log(data);
    }

    const  generateUniqueFileName = (fileExtension) => {
        const timestamp = new Date().getTime();
        const randomString = Math.random().toString(36).substring(2, 15);
        return `${timestamp}-${randomString}.${fileExtension}`;
    }

    const handleTakePicture = async () => {
        if (cameraRef.current) {
            const filename = generateUniqueFileName("jpg");
            const image = await cameraRef.current.takePicture(filename);
            await sendPictureToServer(image)
        }
    }

    const handleStartCapturing = async () => {
        if (isCameraLive.current) {
            await videoRef.current.pause();
            isCameraLive.current = false;
            // take picture here

        } else {
            await videoRef.current.play();
            isCameraLive.current = true;
        }
    }

    useEffect(() => {
        return () => {
            if (cameraRef.current) {
                cameraRef.current.stop();
            }
        }
    }, [])

    return (
        <Paper>
            <Card elevation={20}>
                <CardHeader
                    style={{cursor: "move"}}
                    avatar={
                        <IconButton>
                            <VideoCamIcon fontSize="large"/>
                        </IconButton>
                    }
                    action={
                        <IconButton>
                            <MoreVertIcon/>
                        </IconButton>
                    }
                    title="Camera Viewer"
                    subheader={moment().format("MMM Do YY")}
                />
                <CardContent>
                    <Grid container
                          alignItems="center"
                          direction="row"
                          spacing={1}
                          justify="center">
                        <Grid item xs={12}>
                            <video autoPlay={true} ref={videoRef} className={styles.cameraVideo}/>
                        </Grid>
                        <Grid item xs={12}>
                            <Grid container
                                  spacing={2}
                                  direction="row"
                                  alignItems="center"
                                  justify="center">

                                <Grid item xs={12}>
                                    <CameraPicker onChange={handleDeviceChange}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <ButtonGroup variant="contained" aria-label="outlined primary button group">
                                        <IconButton aria-label="Play" onClick={handleStartCapturing}>
                                            <CameraIcon fontSize="large"/>
                                        </IconButton>
                                        <IconButton aria-label="Send" onClick={handleTakePicture}>
                                            <SendIcon fontSize="large"/>
                                        </IconButton>
                                    </ButtonGroup>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </CardContent>
            </Card>
        </Paper>
    )
}

const CameraViewer = (props) => {


    return (
        <>
            <CameraCapture width={800} height={600}/>
        </>
    )
}


export default CameraViewer;