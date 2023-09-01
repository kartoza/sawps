// src/BiDirectionalChart.js
import React from 'react';
import { Box, Typography } from "@mui/material";
import {Bar} from 'react-chartjs-2';
import "./index.scss";
import {ChartCard} from "./ChartCard";

const AgeGroupBarChart = (props: any) => {
    const { loading, ageGroupData, icon, name, colour } = props
    const datasetMale: number[] = [];
    const datasetFemale: number[] = [];
    ageGroupData?.forEach((data: any) => {
        datasetMale.push(data.total_adult_male, data.total_sub_adult_male, data.total_juvenile_male);
        datasetFemale.push(-data.total_adult_female, -data.total_sub_adult_female, -data.total_juvenile_female);
    })

    const data = {
        labels: ['Adult', 'Sub-Adult', 'Juvenile'],
        datasets: [
            {
                label: 'Male',
                data: datasetMale,
                backgroundColor: colour,
            },
            {
                label: 'Female',
                data: datasetFemale,
                backgroundColor: (colour.slice(0, 7) + '80' + colour.slice(7)),
            },
        ],
    };

    const options = {
        indexAxis: 'y' as const,
        scales: {
            x: {
                beginAtZero: true,
                display: false,
                stacked: true,
            },
            y: {
                display: false,
                stacked: true,
                grid: {
                    display: false,
                },
                ticks: {
                    color: "black",
                },
            },
        },
        plugins: {
            tooltip: {
                enabled: false
            },
            datalabels: {
                display: false,
            },
            legend: {
                display: false,
            }
        },
    } as const;

    return (
        <ChartCard
            loading={loading}
            chartComponent={
                <>
                    {ageGroupData?.length > 0 && <Box className="white-chart1" >
                        <Box className="barchart-head">
                            <Box className="barchart-head-left"></Box>
                            <Box className="barchart-head-right">
                                <Typography>{name}</Typography>
                                {icon &&
                                <img src={icon} alt='Icon image' />
                                }
                            </Box>
                        </Box>
                        <Box className="barChartBox">
                            <Box className="barchartleft">
                                <Typography className="adult-box"> Adult</Typography>
                                <Typography className="adult-box"> Sub-Adult</Typography>
                                <Typography className="adult-box"> Juvenile</Typography>
                            </Box>
                            <Box className="barchartright">
                                <Bar data={data} options={options} height={225} width={1000} />
                            </Box>
                        </Box>
                        <Box className="chartBottom">
                            <Box className="chartBottom-left"></Box>
                            <Box className="flex chartBottom-right">
                                <Typography className="femaleBox"> Female</Typography>
                                <Typography className="femaleBox"> Male</Typography>
                            </Box>
                        </Box>
                    </Box >}
                </>
            }
            title={''}
            xLabel={''}
        />
    )
};

export default AgeGroupBarChart;
