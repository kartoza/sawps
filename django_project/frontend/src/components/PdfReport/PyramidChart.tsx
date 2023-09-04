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
                <Typography style={{ marginRight: '10px', fontSize: 20 }}>
                    {species.species_name}
                    <img src={species.Icon} alt="species Icon" 
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
                                    display: true,
                                    font: {
                                        size: 20,
                                        weight: "bold" as "bold"
                                    }
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
                                    usePointStyle: true,// Show only legend titles, not the select boxes
                                    font: {
                                        size: 20,
                                        weight: "bold" as "bold"
                                    }
                                }
                            },
                        }
                    }} 
                />
            </Box>
        );

        return generateChartContainer(chartComponent, index);
    });

    return (
        <Box>
            {generatedCharts.length > 0 && (
                <Typography variant="h6" gutterBottom style={{ textAlign: "left" }}>
                    Population Pyramids
                </Typography>
            )}
            <Box style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'flex-start' }}>
                {!loading ? (
                    speciesWithCurrentYearValues.length > 0 && generatedCharts.length > 0 ? (
                        generatedCharts
                    ) : null
                ) : (
                    <Loading />
                )}
            </Box>
        </Box>
    );
    
};

export default PyramidChartForPdf;
