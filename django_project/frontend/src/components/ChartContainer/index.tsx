import React, {useRef} from "react";
import {Box, Typography, Tooltip} from "@mui/material";
import html2canvas from "html2canvas";
import './style.scss';


interface ChartContainerInterface {
    title: string;
    chart: any;
    icon?: string;
}

const INFO_CHART_ICON = '/static/images/information-chart-icon.svg'
const DOWNLOAD_CHART_ICON = '/static/images/download-chart-icon.svg'

export default function ChartContainer(props: ChartContainerInterface) {
    const chartRef = useRef(null);

    const downloadChart = () => {
        const chartElement = chartRef.current;
        if (chartElement) {
            html2canvas(chartElement).then(canvas => {
                const link = document.createElement('a');
                link.href = canvas.toDataURL('image/png');
                link.download = `${props.title}.png`;
                link.click();
            });
        }
    }

    return (
        <Box className={'ChartContainerBox'}>
            <Box ref={chartRef}>
                <Typography className={'TextBox'}>{props.title}</Typography>
                {props.chart}
            </Box>
            <Box className={'DownloadChartContainer'}>
                <Tooltip title={props.title} arrow placement={'left'}>
                    <img src={INFO_CHART_ICON} width={25}/>
                </Tooltip>
                <img src={DOWNLOAD_CHART_ICON} width={25} onClick={downloadChart}/>
            </Box>
        </Box>
    )
}
