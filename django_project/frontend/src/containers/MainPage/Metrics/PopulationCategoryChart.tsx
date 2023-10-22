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
  'rgba(112, 178, 118, 0.5)',
  'rgba(250, 167, 85, 0.5)',
  'rgba(157, 133, 190, 0.5)',
  'rgba(255, 82, 82, 0.5)',
  'rgba(97, 97, 97, 0.5)'
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
      onEmptyDatasets
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
            if (Object.keys(response.data).length === 0) {
                onEmptyDatasets(false)
            } else {
                onEmptyDatasets(true)
            }
            
            const filteredData: any = {};

            for (const key in response.data) {
                if (response.data[key].year >= startYear && response.data[key].year <= endYear) {
                    filteredData[key] = response.data[key];
                }
            }
            setPopulationData(filteredData);
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
  
    // CREATE DATASETS FOR THE CHART
    const newDatasets: {
        label: string;
        backgroundColor: string;
        data: number[];
    }[] = [];

    const firstOccurrenceIndex : Record<string, number> = {};
    let zerosToAdd = 0;
    let trackZerosToAdd = 0;

    for (const category in populationData) {
      const index = populationCategories.indexOf(category);
    
      const [year, label] = category.split('_');
    
      let dataValue: number[] = [];

      for (let i = 0; i <= index; i++) {
        if (!(label in firstOccurrenceIndex)) {
            firstOccurrenceIndex[label] = index;
        }
      }


      if (label in firstOccurrenceIndex) {
        // determine the number of leading zeros to add 
        // based on the number of times a category repeated before the current one
        if(index === firstOccurrenceIndex[label]){
            if((index - trackZerosToAdd) !== 0){
                for (let i = 0; i < index - trackZerosToAdd; i++) {
                    dataValue.push(0);
                }
            }  
        }
        else {
            zerosToAdd = firstOccurrenceIndex[label]
            if(zerosToAdd !== 0){
                for (let i = 0; i < zerosToAdd; i++) {
                    dataValue.push(0);
                } 
            }
            trackZerosToAdd+=1
        }
      }
      
    
      dataValue.push(populationData[category].property_count);


      newDatasets.push({
        label: year,
        backgroundColor: availableColors[index % availableColors.length],
        data: dataValue,
       });
  
    }

    // JOIN LEGEND LABELS AND COLORS WITH THE SAME YEAR
    const resultObject: Record<string, { label: string; backgroundColor: string; data: number[] }> = {};

    newDatasets.forEach((item) => {
    const { label, data } = item;

    if (resultObject[label]) {
        // If the year already exists, append the non-zero values
        for (let i = 0; i < data.length; i++) {
        if (data[i] !== 0) {
            resultObject[label].data[i] = data[i];
        }
        }
    } else {
        // If the year is unique, create a new entry
        resultObject[label] = { label, backgroundColor: item.backgroundColor, data };
    }
    });

    // Convert the result object back to an array
    const resultArray = Object.values(resultObject);


    // SORT THE LABELS AND CATEGORIES FROM LOWEST TO HIGHEST
    const customSort = (a: string, b: string): number => {
        const [minA, maxA] = a.split(/-|>/).map((num) => parseInt(num, 10) || 0);
        const [minB, maxB] = b.split(/-|>/).map((num) => parseInt(num, 10) || 0);
    
      // Compare based on the maximum values
      return maxA - maxB;
    };

    labels.sort(customSort);

    // Find the maximum size of the data arrays
    const maxSize = Math.max(...resultArray.map((item) => item.data.length));
      
    // Pad the other arrays to match the maximum size by adding zeros at the end
    resultArray.forEach((item) => {
        const { data } = item;
        const sizeDifference = maxSize - data.length;
      
        if (sizeDifference > 0) {
          // Create an array of zeros with the size difference
          const zeros = new Array(sizeDifference).fill(0);
          // Append zeros to the end of the data array
          item.data = [...data, ...zeros];
        }
    });
      
    // Reverse the order of the data arrays
    resultArray.forEach((item) => {
        item.data.reverse();
    });


    // ADD PROCESSED DATA TO CHART AND DEFINE CHART BEHAVIOUR
    const data = {
        labels: labels,
        datasets: resultArray
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
            />
        ) : (
            <Loading containerStyle={{ minHeight: 160 }} />
        )}
    </Grid>
);
};

export default PopulationCategoryChart;
