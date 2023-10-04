import { Grid } from '@mui/material';
import React from 'react';
import { Bar } from 'react-chartjs-2';

type AvailableColors = {
    [key: string]: string;
};

const availableColors: AvailableColors = {
    'Adult male': 'rgba(112, 178, 118, 1)', // Solid color for male
    'Adult female': 'rgba(112, 178, 118, 0.5)', // 50% transparency for female
    'Sub-adult male': 'rgba(250, 167, 85, 1)', // Solid color for male
    'Sub-adult female': 'rgba(250, 167, 85, 0.5)', // 50% transparency for female
    'Juvenile male': 'rgba(157, 133, 190, 1)', // Solid color for male
    'Juvenile female': 'rgba(157, 133, 190, 0.5)', // 50% transparency for female
};
const AgeGroupBarChart = (props: any) => {
    const { loading, ageGroupData } = props;

    // Define the labels (years) dynamically from ageGroupData
    const labels = ageGroupData.map((data: any) => data.total_year);

    // Define an array to hold datasets
    const datasets = [];

    // Loop through the available colors and create a dataset for each age group
    for (const [ageGroup, color] of Object.entries(availableColors)) {
        // Map the data dynamically based on the age group
        const data = ageGroupData.map((data: any) => data[`total_${ageGroup.toLowerCase().replace(' ', '_')}`]);

        // Create the dataset object
        const dataset = {
            label: ageGroup,
            data: data,
            backgroundColor: color,
        };

        datasets.push(dataset);
    }

    const data = {
        labels: labels,
        datasets: datasets,
    };

const options = {
    indexAxis: 'y' as const,
    scales: {
        x: {
            beginAtZero: true,
            display: true,
            stacked: true,
            title: {
                display: true,
                text: 'Count', // X-axis label
                font: {
                    size: 14,
                    weight: "bold" as "bold",
                },
            },
        },
        y: {
            display: true,
            stacked: true,
            title: {
                display: true,
                text: 'Year', // Y-axis label
                font: {
                    size: 14,
                    weight: "bold" as "bold",
                },
            },
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
            position: 'right' as 'right',
            labels: {
                boxWidth: 20,
                boxHeight: 13,
                padding: 12,
                font : {
                  size: 10,
                  weight: "bold" as "bold"
                }
            },
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
    <Grid style={{ overflow: 'auto'}}>
      <Bar data={data} options={options} height={200} width={500}/>
    </Grid>
  );
};

export default AgeGroupBarChart;
