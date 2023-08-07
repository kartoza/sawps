import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import Loading from "../../../components/Loading";
import "./index.scss";



Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_DENSITY = '/api/properties-per-population-category/'

const PopulationCategoryChart = () => {
    const [loading, setLoading] = useState(false)
    const [populationData, setPopulationData] = useState([])


    const fetchpopulationCategoryData = () => {
        setLoading(true)
        axios.get(FETCH_SPECIES_DENSITY).then((response) => {
            setLoading(false)
            if (response.data) {
                setPopulationData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }


    useEffect(() => {
        fetchpopulationCategoryData();
    }, [])

    const data = {
        labels: Object.keys(populationData),
        datasets: [
            {
                backgroundColor: 'rgb(83 83 84)',
                borderColor: 'rgb(83 83 84)',
                borderWidth: 1,
                data: Object.values(populationData),
            },
        ],
    };

    const options = {
        plugins: {
            datalabels: {
                display: false,
            },
            legend: {
                display: false,
            }
        },
        scales: {
            x: {
                beginAtZero: true,
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50,
                    max: 200,
                },
            },
        },
    };

    return (
        <Box>
            {loading ? <Loading /> :
                <Box className="white-chart" >
                    <Box className="white-chart-heading">
                        <Typography>Number of properties per population category</Typography>
                        <Bar data={data} options={options} height={435} width={1000}/>
                    </Box>
                    <Typography>Population category</Typography>
                </Box >
            }
        </Box>
    );
};

export default PopulationCategoryChart;
