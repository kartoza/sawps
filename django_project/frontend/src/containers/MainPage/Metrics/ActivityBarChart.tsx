import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Loading from "../../../components/Loading";
import "./index.scss";

import axios from "axios";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import { Bar } from 'react-chartjs-2';

const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/'

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const ActivityBarChart = (props: {property: any}) => {
    const [loading, setLoading] = useState(false);
    const [activityData, setActivityData] = useState([]);
    const [activityMethods, setActivityMethods] = useState([]);
    const [animals, setAnimals] = useState([]);
    const currentYear = new Date().getFullYear();
    const startYear = currentYear - 1;
    const endYear = currentYear;
    const selectedSpecies = ['Lion', 'Cheetah', 'Elephant', 'White rhinoceros', 'Black rhinoceros', 'Leopard'];
    const propertyId = props.property;

    useEffect(() => {
        fetchActivityData();
    }, []);

    const fetchActivityData = async () => {
        setLoading(true);

        try {
            const response = await axios.get(
                `${FETCH_ACTIVITY_TOTAL_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
            );

            
            
            type ActivityData = {
                [key: string]: number;
            };
            
            type SpeciesActivity = {
                total: number;
                species_name: string;
                activities: ActivityData[];
            };
            
            type TransformedSpecies = {
                animal: string;
                [key: string]: number | string;
            };
            
            const transformedData: TransformedSpecies[] = response.data.map((species: SpeciesActivity) => {
                const speciesData: TransformedSpecies = {
                    animal: species.species_name,
                };
            
                species.activities.forEach((activity: ActivityData) => {
                    const [activityName, activityValue] = Object.entries(activity)[0];
                    speciesData[activityName] = activityValue;
                });
            
                return speciesData;
            });
            
            const allActivities: string[] = [...new Set(transformedData.flatMap(species => Object.keys(species).filter(key => key !== 'animal')))];
            
            setActivityMethods(allActivities);
            setAnimals(transformedData.map(species => species.animal));
            setActivityData(transformedData);
            
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    };

    const barColors = ['black', 'green', 'purple', 'orange', 'red'];

const barData = {
    labels: animals,
    datasets: activityMethods.map((method, index) => ({
        label: method,
        data: activityData.map((item) => item[method]),
        backgroundColor: barColors[index % barColors.length], // Cycle through the colors
    })),
};

const barOptions = {
    maintainAspectRatio: false,
    plugins: {
        datalabels: {
            display: false,
        },
        legend: {
            position: 'bottom' as 'bottom',
            labels: {
                position: 'bottom' as 'bottom',
                usePointStyle: true,
                font: {
                    size: 15,
                },
                generateLabels: (chart: any) => {
                    const { datasets } = chart.data;
                    return datasets.map((dataset: any, index: any) => ({
                        text: dataset.label,
                        fillStyle: barColors[index % barColors.length], // Match legend color to bar color
                        hidden: !chart.isDatasetVisible(index),
                        lineCap: 'round',
                        lineDash: [] as number[],
                        lineDashOffset: 0,
                        lineJoin: 'round',
                        lineWidth: 10,
                        strokeStyle: barColors[index % barColors.length], // Match legend color to bar color
                        pointStyle: 'rect',
                        rotation: 0,
                    }));
                },
            },
        },
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
        <Box className="white-chart chartFullWidth leftBoxRound">
            <Typography>Species activity data, as totals by method</Typography>
            {loading ? (
                <Loading />
            ) : (
                <Box className="BoxChartType">
                    <Bar data={barData} options={barOptions} />
                </Box>
            )}
        </Box>
    );
};

export default ActivityBarChart;
