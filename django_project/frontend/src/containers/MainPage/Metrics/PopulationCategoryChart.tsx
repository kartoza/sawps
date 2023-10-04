import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import "./index.scss";
import {ChartCard} from "./ChartCard";
import { Grid } from "@mui/material";
import Loading from "../../../components/Loading";



Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_DENSITY = '/api/properties-per-population-category/'

const PopulationCategoryChart = (props: any) => {
    const { selectedSpecies, propertyId, startYear, endYear, loading, setLoading, populationData, setPopulationData } = props;

    const fetchpopulationCategoryData = () => {
        setLoading(true);
        axios
            .get(`${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`)
            .then((response) => {
                setLoading(false);
                if (response.data) {
                    setPopulationData(response.data);
                }
            })
            .catch((error) => {
                setLoading(false);
                console.log(error);
            });
    };

    useEffect(() => {
        fetchpopulationCategoryData();
    }, [propertyId, startYear, endYear, selectedSpecies]);

    const categoryLabels = Object.keys(populationData);
    const categoryValues = Object.values(populationData);

    const data = {
        labels: categoryLabels,
        datasets: [
            {
                backgroundColor: categoryLabels.map((category) => {
                    return category === ">200" ? "#9F89BF" : ""; // Set color for category ">200"
                }),
                borderColor: "#9F89BF", // Default color for border
                borderWidth: 1,
                data: categoryValues,
            },
        ],
    };

    const options = {
        plugins: {
            datalabels: {
                display: false,
            },
            legend: {
                display: true,
                position: 'bottom' as 'bottom',
                labels: {
                    generateLabels: (chart: any) => {
                        const categoryLabels = chart.data.labels;
                        const legendLabels: { text: string; fillStyle: string; }[] = [];
    
                        categoryLabels.forEach((category: string) => {
                            if (populationData.hasOwnProperty(category) && populationData[category] > 0) {
                                legendLabels.push({
                                    text: category,
                                    fillStyle: category === ">200" ? "#9F89BF" : "", // Set color for category ">200"
                                });
                            }
                        });
    
                        return legendLabels;
                    },
                },
            },
            title: {
                display: true,
                text: 'Number of properties per population category',
                font: {
                    size: 16,
                    weight: 'bold' as 'bold',
                },
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Population category', // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50,
                    max: 200,
                },
                title: {
                    display: true,
                    text: 'Properties count', // Y-axis label
                    font: {
                        size: 14,
                    },
                },
            },
        },
    };
    
    
    

    return (
        <Grid>
            {!loading ? (
                <Bar data={data} options={options} height={800} width={2000} />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    );
};

export default PopulationCategoryChart;
