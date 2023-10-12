import React, { useEffect, useState } from "react";
import { Bar } from 'react-chartjs-2';
import axios from "axios";
import { Grid } from "@mui/material";
import Loading from "../../../components/Loading";

const FETCH_SPECIES_DENSITY = "/api/properties-per-population-category/";

const availableColors = [
    'rgba(112, 178, 118, 1)',
    'rgba(250, 167, 85, 1)',
    'rgba(157, 133, 190, 1)',
    '#FF5252',
    '#616161',
  ];

const PopulationCategoryChart = (props: any) => {
    const {
      selectedSpecies,
      propertyId,
      startYear,
      endYear,
      loading,
      setLoading,
      populationData,
      setPopulationData,
    } = props;
  
    const fetchPopulationCategoryData = () => {
      setLoading(true);
      axios
        .get(
          `${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
        )
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
      fetchPopulationCategoryData();
    }, [propertyId, startYear, endYear, selectedSpecies]);

    // Extract years from the population data for legend labels
    const populationCategoriesB = Object.keys(populationData);

    // Initialize a Set to store unique labels
    const uniqueLabels = new Set();

    // Iterate through populationCategories to add unique labels to the Set
    populationCategoriesB.forEach((category) => {
    const [year, label] = category.split('_');
    uniqueLabels.add(label);
    });

    // Convert the Set back to an array
    const labels = Array.from(uniqueLabels);
    
    // Extract years from the population data for legend labels
    const populationCategories = Object.keys(populationData);
  
    const newDatasets: {
        label: string;
        backgroundColor: string;
        data: number[];
    }[] = [];

    const firstAppearanceIndex: Record<string, number> = {};

    for (const category in populationData) {
        const index = populationCategories.indexOf(category);

        const [year, label] = category.split('_');

        if (firstAppearanceIndex[label] === undefined) {
            firstAppearanceIndex[label] = index;
        }

        let dataValue: number[] = [];
        if (index > 0) {
            for (let i = 0; i < firstAppearanceIndex[label]; i++) {
                dataValue.push(0);
            }
        }

        dataValue.push(populationData[category].property_count);

        newDatasets.push({
            label: year,
            backgroundColor: availableColors[index % availableColors.length],
            data: dataValue,
        });
    }

  const data = {
    labels: labels,
    datasets: newDatasets
  };

  const options = {
    plugins: {
        responsive: true,
        maintainAspectRatio: false,
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
            text: `Number of properties per population category for ${selectedSpecies}`,
            font: {
                size: 16,
                weight: 'bold' as 'bold',
            },
        },
    },
    layout: {
        padding: {
            top: 0, // Remove top padding
        },
    },
    scales: {
        x: {
            beginAtZero: true,
            stacked: true,
            title: {
                display: true,
                text: 'Population category',
                font: {
                    size: 14,
                },
            },
        },
        y: {
            beginAtZero: true,
            stacked: true,
            type: 'linear' as 'linear',
            title: {
                display: true,
                text: 'Properties count',
                font: {
                    size: 14,
                },
            },
            ticks: {
                stepSize: 1, // Ensure whole number ticks
                max: Math.ceil(200), // Round up to the nearest whole number
            },
        },
    },
};


return (
    <Grid>
        {!loading ? (
            <Bar 
                data={data} 
                options={options} 
                height={200} width={500} 
            />
        ) : (
            <Loading containerStyle={{ minHeight: 160 }} />
        )}
    </Grid>
);
};

export default PopulationCategoryChart;
