import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from 'react-chartjs-2';
import axios from "axios";
import Loading from "../../../components/Loading";
import "./index.scss";

const FETCH_PROPERTY_POPULATION_SPECIES = '/api/species-population-count/';

interface PopulationCount {
    year: number;
    year_total: number;
}

interface Species {
    species_colour: any;
    species_name: string;
    annualpopulation_count: PopulationCount[];
}

const availableColors = [
  'rgba(112, 178, 118, 1)', 
  'rgba(250, 167, 85, 1)', 
  'rgba(157, 133, 190, 1)', 
  '#FF5252', 
  '#616161'
];

const SpeciesSideBarChart = (props: {
      property: any;
      selectedSpecies: string | string[];
    }) => {
    const propertyId = props.property;
    var selectedSpecies = props.selectedSpecies;
    const [loading, setLoading] = useState(false);
    const [speciesData, setSpeciesData] = useState<Species[]>([]);
    const [noData, setNoData] = useState(false);

    const yearsData = Array.from(new Set(speciesData.flatMap(species => species.annualpopulation_count.map(entry => entry.year))));
    yearsData.sort((a, b) => a - b);

    const speciesPopulation = {
        labels: yearsData.map(year => year.toString()),
        datasets: speciesData.map((species) => ({
            label: species.species_name,
            data: yearsData.map(year => {
              const yearData = species.annualpopulation_count.find(entry => entry.year === year);
                return yearData ? yearData.year_total : 0;
            }),
            backgroundColor: species.species_colour, // Use the species_color from the API response
        })),
    };

    const speciesOptions = {
        plugins: {
          responsive: true,
          maintainAspectRatio: false,
          tooltip: {
            enabled: true,
          },
          datalabels: {
            display: false,
          },
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Year',
                font: {
                    size: 14,
                },
            },
          },
          y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Count',
                font: {
                    size: 14,
                },
            },
          },
        },
        interaction: {
          mode: 'index' as const,
          intersect: false,
        },
      };

    useEffect(() => {
        if (
            propertyId && 
            selectedSpecies.length > 0
        ) {
            fetchPropertyPopulation();
        }
    }, [propertyId, selectedSpecies]); // Re-fetch when propertyId or selectedSpecies change


    const fetchPropertyPopulation = () => {
        setLoading(true);
        axios.get(`${FETCH_PROPERTY_POPULATION_SPECIES}?species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false);
            if (response.data) {
                if(response.data[0]?.annualpopulation_count.length > 0){
                    setNoData(false);
                    setSpeciesData(response.data);
                }
                else {
                    setNoData(true);
                }
                
            }
        }).catch((error) => {
            setLoading(false);
            setNoData(true);
            console.log(error);
        });
    };
    
    return (
        <Box>
          {propertyId && selectedSpecies.length > 0 ? (
            loading ? (
              <Loading />
            ) : noData ? (
              <Typography>No data available for current selections.</Typography>
            ) : (
              <Box className="white-chart">
                <Box className="white-chart-heading">
                  <Typography>{selectedSpecies} population counts per year</Typography>
                </Box>
                <Bar data={speciesPopulation} options={speciesOptions} />
              </Box>
            )
          ) : (
            <Typography>Please select a property and species.</Typography>
          )}
        </Box>
      );
};

export default SpeciesSideBarChart;
