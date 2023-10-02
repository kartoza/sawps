import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Loading from "../../../components/Loading";
import "./index.scss";
import axios from "axios";
import { Bar } from 'react-chartjs-2';

const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/'

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const ActivityBarChart = (props: {
    property: any;
    selectedSpecies: string | string[];
    from: number;
    to: number;
  }) => {
    const [loading, setLoading] = useState(false);
    const [activityData, setActivityData] = useState([]);
    const [activityMethods, setActivityMethods] = useState([]);
    const [animals, setAnimals] = useState([]);
    const currentYear = new Date().getFullYear();
    const propertyId = props.property;
    var selectedSpecies = props.selectedSpecies;
    var startYear = props.from;
    var endYear = props.to; 
    const [noData, setNoData] = useState(false);
    const [speciesColors, setSpeciesColors] = useState<{ [key: string]: string }>({});
    const activityColors = ['#FF5252', '#9D85BE', '#FAA755', '#000', '#70B276'];



    useEffect(() => {
        if (
            propertyId && 
            selectedSpecies.length > 0 &&
            startYear &&
            endYear
        ) {
          fetchActivityData();
        }else {
            // assign defaults
            selectedSpecies = ['Lion', 'Cheetah', 'Elephant', 'White rhinoceros', 'Black rhinoceros', 'Leopard'];
            startYear = currentYear - 1;
            endYear = currentYear;
            fetchActivityData();
        }
    }, [propertyId, selectedSpecies, startYear, endYear]); // Re-fetch when propertyId or selectedSpecies change

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

            if (transformedData.length === 0) {
                setNoData(true);
            } else {
                setNoData(false);
            }

            // Extract and set species colors from the API response
            const speciesColors = response.data.reduce((colors: { [x: string]: any; }, species: { species_name: string | number; colour: any; }) => {
                colors[species.species_name] = species.colour;
                return colors;
            }, {});

            // Set species colors in state
            setSpeciesColors(speciesColors);
            
            const allActivities: string[] = [...new Set(transformedData.flatMap(species => Object.keys(species).filter(key => key !== 'animal')))];
            
            setActivityMethods(allActivities);
            setAnimals(transformedData.map(species => species.animal));
            setActivityData(transformedData);
            
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setNoData(true);
            setLoading(false);
        }
    };

    const barData = {
        labels: animals,
        datasets: activityMethods.map((method, index) => ({
            label: method,
            data: activityData.map((item) => item[method]),
            backgroundColor: animals.map((animal) => speciesColors[animal]), // Use speciesColors mapping
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
                        const activityColorMap: { [key: string]: string } = {};
                    
                        datasets.forEach((dataset: any, index: any) => {
                            const speciesName = dataset.label;
                            const activityData = activityColors.length > 1 ? dataset.label : Object.keys(dataset.data)[0];
                            
                            // Assign colors based on the activity count
                            if (!activityColorMap[activityData]) {
                                activityColorMap[activityData] = activityColors[index % activityColors.length];
                            }
                    
                            dataset.backgroundColor = activityColorMap[activityData];
                            dataset.borderColor = activityColorMap[activityData];
                        });
                    
                        return datasets.map((dataset: any, index: any) => ({
                            text: dataset.label,
                            fillStyle: activityColorMap[dataset.label], // Use activity color mapping
                            hidden: !chart.isDatasetVisible(index),
                            lineCap: 'round',
                            lineDash: [] as number[],
                            lineDashOffset: 0,
                            lineJoin: 'round',
                            lineWidth: 10,
                            strokeStyle: activityColorMap[dataset.label], // Use activity color mapping
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
      {propertyId && selectedSpecies.length > 0 ? (
        loading ? (
          <Loading />
        ) : (
          noData ? (
            <Typography>No data available for current selections.</Typography>
          ) : (
            <Box className="BoxChartType">
              <Bar data={barData} options={barOptions} />
            </Box>
          )
        )
      ) : (
        <Typography>Please select a property and species.</Typography>
      )}
    </Box>
);
};

export default ActivityBarChart;
