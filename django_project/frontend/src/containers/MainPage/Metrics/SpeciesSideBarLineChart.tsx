import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Line } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import axios from "axios";
import Loading from "../../../components/Loading";
import "./index.scss";

Chart.register(CategoryScale);

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

const SpeciesSideBarLineChart = (props: {
    property: any;
    selectedSpecies: string | string[];
    from: number;
    to: number;
    }) => {
    const propertyId = props.property;
    var selectedSpecies = props.selectedSpecies;
    var startYear = props.from;
    var endYear = props.to;
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
            fill: false,
            borderColor: species.species_colour, // Use the species_color from the API response
            borderWidth: 1,
        })),
    };

    const speciesOptions = {
    plugins: {
        datalabels: {
        display: false,
        },
        legend: {
        position: 'bottom' as 'bottom',
        labels: {
            usePointStyle: true,
            font: {
            size: 15,
            },
            generateLabels: (chart: any) => {
            const { datasets } = chart.data;
            return datasets.map((dataset: any, index: any) => ({
                text: dataset.label,
                fillStyle: dataset.borderColor,
                hidden: !chart.isDatasetVisible(index),
                lineCap: 'round',
                lineDash: [] as number[],
                lineDashOffset: 0,
                lineJoin: 'round',
                lineWidth: 10,
                strokeStyle: dataset.borderColor,
                pointStyle: 'rect',
                rotation: 0,
            }))
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
            stepSize: 65,
            max: 260,
        },
        },
    },
    };


    useEffect(() => {
        if (
            propertyId && 
            selectedSpecies.length > 0 &&
            startYear &&
            endYear
        ) {
            fetchPropertyPopulation();
        }
    }, [propertyId, selectedSpecies, startYear, endYear]); // Re-fetch when propertyId or selectedSpecies change


    const fetchPropertyPopulation = () => {
        setLoading(true);
        axios.get(`${FETCH_PROPERTY_POPULATION_SPECIES}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
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
                  <Typography>Species population counts per year </Typography>
                </Box>
                <Line data={speciesPopulation} options={speciesOptions} />
              </Box>
            )
          ) : (
            <Typography>Please select a property and species.</Typography>
          )}
        </Box>
      );
};

export default SpeciesSideBarLineChart;
