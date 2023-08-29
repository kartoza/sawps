import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Line } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import Loading from "../../../components/Loading";
import "./index.scss";
import { ChartCard } from "./ChartCard";

Chart.register(CategoryScale);

const AreaAvailableLineChart = (props: any) => {
    const { loading, areaData, message } = props
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
            datalabels: {
                display: false,
            },
            legend: {
                display: false,
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                grid: {
                    display: false,
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                },
                ticks: {
                    stepSize: 65,
                    max: 260,
                },
            },
        },
    };

    return (
        <ChartCard
            loading={loading}
            chartComponent={
                <>
                    <Box className="white-species">
                        <Box className="white-chart-species">
                            {message && <Typography className="info-message">{message}</Typography>}
                            <Typography className="total-heading">Total area vs area available to species</Typography>
                            <Box className="AreaDataValue"><Line data={AreaDataValue} options={AreaOptions} height={225} width={1000} /></Box>
                        </Box>

                        <Box className="white-species-text">
                            <Box className="flex species-Typography">
                                <Box
                                    width={20}
                                    height={20}
                                    sx={{ backgroundColor: '#FF5252' }}
                                />
                                <Typography>Total area of property</Typography>
                            </Box>
                            <Box className="flex species-Typography">
                                <Box
                                    width={20}
                                    height={20}
                                    sx={{ backgroundColor: '#F9A95D' }}
                                />
                                <Typography>Area available to species</Typography>
                            </Box>
                        </Box>
                    </Box>
                </>
            }
            title={''}
            xLabel={''}
        />
    );
};

export default AreaAvailableLineChart;
