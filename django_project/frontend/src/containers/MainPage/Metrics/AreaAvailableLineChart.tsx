import React from "react";
import { Grid } from "@mui/material";
import { Line } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import Loading from "../../../components/Loading";
import "./index.scss";

Chart.register(CategoryScale);

const AreaAvailableLineChart = (props: any) => {
    const { loading, areaData, species_name } = props

    // Extract the species name
    const speciesName = species_name ? species_name : '';

    const AreaDataValue = {
        labels: areaData.map((item: any) => item?.annualpopulation__year),
        datasets: [
            {
                label: "Area available to species",
                data: areaData.map((item: any) => item?.area_available),
                borderColor: "#F9A95D",
                backgroundColor: "#F9A95D",
                fill: {
                    target: "origin",
                    above: "#F9A95D"
                }
            },
            {
                label: "Total area of property",
                data: areaData.map((item: any) => item?.area_total),
                borderColor: "#FF5252",
                backgroundColor: "#FF5252",
                fill: "origin",
                above: "#FF5252"
            }
        ]
    }

    const AreaOptions = {
        tension: 0.5,
        elements: {
            point: {
                radius: 0,
            },
        },
        plugins: {
            tooltip: {
                enabled: true,
            },
            datalabels: {
                display: false,
            },
            legend: {
                display: true,
                position: 'bottom' as 'bottom',
                labels: {
                    boxWidth: 20,
                    boxHeight: 13,
                    padding: 12,
                    font : {
                      size: 12,
                      weight: "bold" as "bold"
                    }
                },
            },
            title: {
                display: true,
                text: `Total area vs area available to ${speciesName}`,
                font: {
                    size: 16, 
                    weight: 'bold' as 'bold', 
                },
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                grid: {
                    display: false,
                },
                title: {
                    display: true,
                    text: 'Year', // X-axis label
                    font: {
                        size: 14,
                        weight: "bold" as "bold",
                    },
                },
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                },
                title: {
                    display: true,
                    text: 'Area (Ha)', // Y-axis label
                    font: {
                        size: 14,
                        weight: "bold" as "bold",
                    },
                },
            },
        },
    };

    return (
        <Grid>
            {!loading ? (
                <Line 
                    data={AreaDataValue} 
                    options={AreaOptions} 
                    height={265} 
                    width={650} 
                />
       
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    );
};

export default AreaAvailableLineChart;
