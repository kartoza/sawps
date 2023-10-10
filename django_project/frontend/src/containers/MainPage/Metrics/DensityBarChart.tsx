import React, { useEffect, useState } from 'react';
import { Grid } from "@mui/material";
import { Bar } from 'react-chartjs-2';
import "./index.scss";
import Loading from '../../../components/Loading';
import axios from 'axios';

const FETCH_SPECIES_DENSITY = "/api/species-population-total-density/";

const DensityBarChart = (props: any) => {
    const {
        selectedSpecies,
        propertyId,
        startYear,
        endYear,
        loading,
        setLoading,
        densityData,
        setDensityData,
    } = props;


    useEffect(() => {
        const fetchActivityPercentageData = () => {
            setLoading(true);
            axios
                .get(
                    `${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
                )
                .then((response) => {
                    setLoading(false);
                    if (response.data) {
                        const filteredData = response.data.filter((item: any) => item.density.density !== null);
                        setDensityData(filteredData.length > 0 ? filteredData : []);
                    }
                })
                .catch((error) => {
                    setLoading(false);
                    console.log(error);
                    setDensityData([])
                });
        };

        fetchActivityPercentageData();
    }, [propertyId, startYear, endYear, selectedSpecies, setLoading, setDensityData]);

    // Extract labels and data from the fetched API response
    const labels = densityData.map((each: any, index: number) => {
        const provinceName = each.province_name;
        const organizationName = each.organisation_name;
        
        // Check if the density array exists and has at least one item
        if (each.density && Array.isArray(each.density) && each.density.length > 0) {
            // Access the property_name field from the first item in the density array
            const propertyName = each.density[0].property_name;
        
            // Helper function to format a name based on the specified rules
            const formatName = (name: string) => {
                const words = name.split(' ');
                if (words.length === 1) {
                    return words[0].substring(0, 2).toUpperCase();
                } else {
                    return words.map(word => word.substring(0, 1).toUpperCase()).join('');
                }
            };
        
            const provinceCode = formatName(provinceName);
            const organizationCode = formatName(organizationName);
            const propertyCode = formatName(propertyName);
            const uniqueNumericValue = 1000 + index + 1; // Generate unique numeric value starting from 1001
        
            // Create the label by combining province, organization, property, and the unique numeric value
            const label = `${provinceCode}${organizationCode}${propertyCode}${uniqueNumericValue}`;
        
            return label;
        }
        
        return ''; // Return an empty string if density data is missing or invalid
    });

   // Extract years from the fetched API response
    const yearsInData = densityData.reduce((years: any[], each: any) => {
        // Check if the density array exists and has at least one item
        if (each.density && Array.isArray(each.density) && each.density.length > 0) {
            // Iterate through the density array and extract all unique years
            each.density.forEach((densityItem: any) => {
                if (densityItem.year) {
                    years.push(densityItem.year);
                }
            });
        }
        
        return years;
    }, []);

    // Remove duplicate years
    const uniqueYears = Array.from(new Set(yearsInData));

    // Create datasets for each year using available colors
    const datasets = uniqueYears.map((year: any, index: number) => {
        const backgroundColor = colors[index % colors.length];
        const data = densityData.map((each: any) => {
            // Check if the density array exists, is an array, and has at least one item
            if (each.density && Array.isArray(each.density) && each.density.length > 0) {
                // Find the density data object with the matching year, if it exists
                const densityItem = each.density.find((densityDataItem: any) => densityDataItem.year === year);
                if (densityItem) {
                    // Access the density value from the found density data object
                    return densityItem.density;
                }
            }
            return null; // Return null if density data is missing or invalid for the given year
        });

        return {
            label: `${year}`,
            data: data,
            backgroundColor: backgroundColor,
        };
    });



    const options = {
        indexAxis: 'y' as const,
        scales: {
            x: {
                beginAtZero: true,
                display: true,
                stacked: true,
                title: {
                    display: true,
                    text: "Population density", // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                display: true,
                stacked: true,
                grid: {
                    display: false,
                },
                title: {
                    display: true,
                    text: "Property", // Y-axis label
                    font: {
                        size: 14,
                    },
                },
                // Replace the tick values with the labels
                callback: (value: string, index: number) => {
                    return labels[index];
                },
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
                position: 'right' as 'right',
                labels: {
                    boxWidth: 20,
                    boxHeight: 13,
                    padding: 12,
                    font: {
                        size: 10,
                    },
                },
            },
            title: {
                display: true,
                text: `${selectedSpecies} population density per property`, // Dynamic chart title
                font: {
                    size: 16,
                    weight: 'bold' as 'bold',
                },
            },
        },
    } as const;

    return densityData.length > 0 ? (
        <Grid>
            {!loading ? (
                <Bar 
                    data={{ labels: labels, datasets: datasets }} 
                    options={options} 
                    height={200} width={500} 
                />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    ) : null;
    
};

// Define colors for each year
const colors = ['rgba(112, 178, 118, 1)', 'rgba(250, 167, 85, 1)', 'rgba(157, 133, 190, 1)', '#FF5252', '#616161'];

export default DensityBarChart;
