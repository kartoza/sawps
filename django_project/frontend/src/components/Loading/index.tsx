import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import {Typography} from "@mui/material";
import './index.scss';

interface LoadingInterface {
    label?: string,
    size?: number,
    color?: any,
    style?: any
}

export default function Loading(props: LoadingInterface) {
    return (
        <div className="loading-container">
            <CircularProgress size={props.size} color={props.color} style={props.style}/>
            { props.label ? <Typography sx={{ fontSize: 15 }} style={{ marginLeft: 10 }}>{ props.label }</Typography> : '' }
        </div>
    )
}
