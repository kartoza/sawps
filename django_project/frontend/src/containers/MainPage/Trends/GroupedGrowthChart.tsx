import React, {useState, useEffect} from 'react';
import GrowthChart, {GrowthDataItem} from './GrowthChart';
import { Box, Typography } from '@mui/material';
import './index.scss';


interface GroupedGrowthChartInterface {
    data: GrowthDataItem[];
    title: string;
    chartId: string;
}

const GroupedGrowthChart = (props: GroupedGrowthChartInterface) => {
    return (
        <Box className={'GroupedGrowthChartContainerBox'}>
            <Box className={'ChartTitleBox'}>
                <Typography className={'ChartTitle'}>{props.title}</Typography>
            </Box>
            <Box className={'ChartContainers'}>
                <Box className={'ChartContainer'}>
                    <Box className={'ChartBox'}>
                        <GrowthChart data={props.data} chartId={props.chartId} />
                    </Box>
                </Box>
            </Box>
        </Box>        
    )
}

export default GroupedGrowthChart
