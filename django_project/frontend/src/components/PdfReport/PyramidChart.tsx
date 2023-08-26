import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from "react-chartjs-2";
import axios from "axios";
import Loading from "../Loading";
import "./index.scss";

const FETCH_SPECIES_DATA = '/api/species-list/';

const PyramidChartForPdf = () => {
    const [loading, setLoading] = useState(true);
    const [speciesData, setSpeciesData] = useState([]);

    const fetchSpeciesData = () => {
        axios.get(FETCH_SPECIES_DATA)
            .then((response) => {
                if (response.data) {
                    console.log('species data ',response.data)
                    setSpeciesData(response.data);
                    setLoading(false);
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }

    useEffect(() => {
        fetchSpeciesData();
    }, []);

    const sortData = (data: any[]) => {
        return data.slice().sort((a: number, b: number) => a - b);
    };

    const generateChartData = (species: { annualpopulation_count: any[]; species_colour: string }) => {
        const currentYear = new Date().getFullYear();
        const currentYearData = species.annualpopulation_count.find((entry: { year: number }) => entry.year === currentYear);
    
        if (!currentYearData) {
            return null; // Return null if data for the current year is not available
        }
    
        const defaultColorMale = species.species_colour; // Use species color for male
        const defaultColorFemale = `${species.species_colour}80`; // Use species color with 50% transparency for female (hex color with alpha value)
    
        const maleData = [
            { label: 'Adult', value: currentYearData.adult_male },
            { label: 'Sub-adult', value: currentYearData.sub_adult_male },
            { label: 'Juvenile', value: currentYearData.juvenile_male },
        ];
        const femaleData = [
            { label: 'Adult', value: currentYearData.adult_female },
            { label: 'Sub-adult', value: currentYearData.sub_adult_female },
            { label: 'Juvenile', value: currentYearData.juvenile_female },
        ];
    
        var sortedMaleData = sortData(maleData);
        var sortedFemaleData = sortData(femaleData);

        // create pyramid like structure
        const sumArraysAndSort = (array1: string | any[], array2: { value: any; }[]) => {
            const result = [];
          
            for (let i = 0; i < array1.length; i++) {
              result.push({
                label: array1[i].label,
                value: array1[i].value + array2[i].value,
              });
            }
          
            return result.sort((a, b) => a.value - b.value);
          };
          
        const sortedData = sumArraysAndSort(femaleData, maleData);
        // console.log('sorted',sortedData);
    
        const sortedMaleLabels = sortedMaleData.map((data) => data.label);

        // console.log('male labels', sortedMaleLabels)
        // console.log('male data',sortedMaleData.map((data) => -data.value))

        for (let count = 0; count < sortedData.length; count++) {
            for (let innerCount = 0; innerCount < sortedMaleLabels.length; innerCount++) {
              if (sortedData[count].label === sortedMaleLabels[innerCount]) {
                // Swap labels
                [sortedMaleLabels[count], sortedMaleLabels[innerCount]] = [sortedMaleLabels[innerCount], sortedMaleLabels[count]];
          
                // Swap data values
                [sortedMaleData[count], sortedMaleData[innerCount]] = [sortedMaleData[innerCount], sortedMaleData[count]];
                [sortedFemaleData[count], sortedFemaleData[innerCount]] = [sortedFemaleData[innerCount], sortedFemaleData[count]];
          
                break; // Break inner loop as the label match is found
              }
            }
          }
          
        //   console.log("New maleLabels:", sortedMaleLabels);
        //   console.log("New maleData:", sortedMaleData);
        
    
        return {
            labels: sortedMaleLabels,
            datasets: [
                {
                    label: 'Male',
                    data: sortedMaleData.map((data) => -data.value),
                    backgroundColor: defaultColorMale,
                    borderWidth: 0,
                    datalabels: {
                        display: false,
                    },
                },
                {
                    label: 'Female',
                    data: sortedFemaleData.map((data) => data.value),
                    backgroundColor: defaultColorFemale,
                    borderWidth: 0,
                    datalabels: {
                        display: false,
                    },
                },
            ],
        };
    };
    

    const speciesWithCurrentYearValues = speciesData.filter(species => {
        const currentYear = new Date().getFullYear();
        return species.annualpopulation_count.some((entry: { year: number; }) => entry.year === currentYear);
    });

    const generateChartContainer = (chartComponent: string | number | boolean | React.JSX.Element | Iterable<React.ReactNode>, index: React.Key) => (
        <Box key={index} mb={4} style={{ display: 'inline-block', width: '50%' }}>
            {chartComponent}
        </Box>
    );

    const generatedCharts = speciesWithCurrentYearValues.map((species, index) => {
        const chartComponent = (
            <Box>
                <Typography style={{ marginRight: '10px' }}>
                    {species.species_name}
                    <img src=" data:image/png;base64,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"
                    alt="species Icon" 
                    style={{ maxWidth: '60px', maxHeight: '60px' ,marginLeft: '262px'}} />
                </Typography>
                <Bar 
                    data={generateChartData(species)} 
                    options={{ 
                        indexAxis: 'y',
                        scales: {
                            x: {
                                display: false,
                                stacked: true,
                                beginAtZero: true,
                                ticks: {
                                    display: false
                                }
                            },
                            y: {
                                stacked: true,
                                ticks: {
                                    display: true
                                },
                                grid: {
                                    display: false
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'bottom',
                                align: 'center',
                                labels: {
                                    usePointStyle: true // Show only legend titles, not the select boxes
                                }
                            }
                        }
                    }} 
                />
            </Box>
        );

        return generateChartContainer(chartComponent, index);
    });

    return (
        <Box>
            <Typography className="white-chart" display="flex" flexWrap="wrap" gutterBottom style={{ marginLeft: 0, fontWeight: 'bold' }}>
                Population Pyramids
            </Typography>
            <Box style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'flex-start' }}>
                {!loading ? (
                    speciesWithCurrentYearValues.length > 0 ? (
                        generatedCharts.length > 0 ? (
                            generatedCharts
                        ) : (
                            <Typography>No species data available.</Typography>
                        )
                    ) : (
                        <Typography>No species data available for the current year.</Typography>
                    )
                ) : (
                    <Loading />
                )}
            </Box>
        </Box>
    );
};

export default PyramidChartForPdf;
