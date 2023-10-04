// src/BiDirectionalChart.js
import React from 'react';
import { Box, Grid, Typography } from "@mui/material";
import {Bar} from 'react-chartjs-2';
import "./index.scss";
import {ChartCard} from "./ChartCard";
import Loading from '../../../components/Loading';

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
                display: true,
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
                display: true,
                position: 'bottom' as 'bottom'
            },
            title: {
                display: true,
                text: 'Population per age group',
                font: {
                    size: 16, 
                    weight: 'bold' as 'bold', 
                },
            },
        },
    } as const;

    return (
        <Grid>
            {!loading ? (
               <Bar data={data} options={options} height={200} width={500} />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    )
};

export default AgeGroupBarChart;
