import React, {useRef} from 'react';
import GrowthChart, {GrowthDataItem} from './GrowthChart';
import { Box, Typography, Tooltip } from '@mui/material';
import html2canvas from "html2canvas";
import './index.scss';


interface GroupedGrowthChartInterface {
    data: GrowthDataItem[];
    title: string;
    chartId: string;
    popChangeCategories?: string[];
    periodCategories?: string[];
}

const INFO_CHART_ICON = '/static/images/information-chart-icon.svg'
const DOWNLOAD_CHART_ICON = '/static/images/download-chart-icon.svg'

const GroupedGrowthChart = (props: GroupedGrowthChartInterface) => {
    const chartRef = useRef(null)
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
        <Box className={'GroupedGrowthChartContainerBox'}>
            <Box className={'ChartContainers'} ref={chartRef}>
                <Box className={'ChartTitleBox'}>
                    <Typography className={'ChartTitle'}>{props.title}</Typography>
                </Box>
                <Box className={'ChartContainer'}>
                    <Box className={'ChartBox'}>
                        <GrowthChart data={props.data} chartId={props.chartId} popChangeCategories={props.popChangeCategories} periodCategories={props.periodCategories} />
                    </Box>
                </Box>
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

export default GroupedGrowthChart
