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

type AvailableColors = {
    [key: string]: string;
};

const availableColors: AvailableColors = {
    'Unplanned/Illegal Hunting': "#FF5252",
    'Planned Euthanasia/DCA': "rgb(83 83 84)",
    'Unplanned/natural deaths': "#75B37A",
    'Planned Hunt/Cull': "#282829",
    'Translocation (Intake)': "#FAA755",
    'Translocation (Offtake)': "#70B276",
    'Other': "#9D85BE",
}

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
    const propertyId = props.property;
    var selectedSpecies = props.selectedSpecies;
    var startYear = props.from;
    var endYear = props.to; 
    const [noData, setNoData] = useState(false);
    const [useMainColor, setMainColor] = useState(false);
    const [mainColor, setColor] = useState('');
    const [speciesColors, setSpeciesColors] = useState<{ [key: string]: string }>({});
    const activityColors = ['#FF5252', '#75B37A', '#282829', '#FAA755','#70B276','#000', '#9D85BE'];



    useEffect(() => {
        if (
            propertyId && 
            selectedSpecies.length > 0 &&
            startYear &&
            endYear
        ) {
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
                setColor(species.colour)
                return colors;
            }, {});

            // Set species colors in state
            setSpeciesColors(speciesColors);
            
            const allActivities: string[] = [...new Set(transformedData.flatMap(species => Object.keys(species).filter(key => key !== 'animal')))];
            

            if(allActivities.length > 1){
                setMainColor(false)
            }else {
                setMainColor(true)
            }
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
            backgroundColor: animals.map((animal) => useMainColor ? mainColor:speciesColors[animal]),
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
                    
                            dataset.backgroundColor = useMainColor? mainColor:activityColorMap[activityData];
                            dataset.borderColor = useMainColor? mainColor:activityColorMap[activityData];
                        });
                    
                        return datasets.map((dataset: any, index: any) => ({
                            text: dataset.label,
                            fillStyle: useMainColor ? mainColor:activityColorMap[dataset.label],
                            hidden: !chart.isDatasetVisible(index),
                            lineCap: 'round',
                            lineDash: [] as number[],
                            lineDashOffset: 0,
                            lineJoin: 'round',
                            lineWidth: 10,
                            strokeStyle: useMainColor ? mainColor: activityColorMap[dataset.label],
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
            {propertyId && selectedSpecies.length > 0 ? (
                loading ? (
                    <Loading />
                ) : (
                    noData ? (
                        <Typography>No data available for current selections.</Typography>
                    ) : (
                        <Box>
                            <Typography>Species activity data, as totals by method</Typography>
                            <Box className="BoxChartType">
                                <Bar data={barData} options={barOptions} />
                            </Box>
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
