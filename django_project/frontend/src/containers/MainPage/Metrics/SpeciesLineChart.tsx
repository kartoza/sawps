import React, { useEffect, useState } from "react";
import { Box, Grid, Typography } from "@mui/material";
import {Bar, Line} from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import axios from "axios";
import Loading from "../../../components/Loading";
// import "./index.scss";
import Card from "@mui/material/Card";
import {ChartCard} from "./ChartCard";

Chart.register(CategoryScale);

const FETCH_PROPERTY_POPULATION_SPECIES = '/api/species-population-count/'

interface Species {
    species_name: string;
    species_colour: string;
    annualpopulation_count: { year: number; year_total: number }[];
}

interface SpeciesLineChartProps {
    selectedSpecies: string;
    propertyId: string;
    startYear: number;
    endYear: number;
    loading: boolean;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
    speciesData: Species[];
    setSpeciesData: React.Dispatch<React.SetStateAction<Species[]>>;
}

const SpeciesLineChart = (props:SpeciesLineChartProps) => {
    const {selectedSpecies, propertyId, startYear, endYear, loading, setLoading, speciesData, setSpeciesData} = props
    // Extract unique years and sort them
    const yearsData = Array.from(new Set(speciesData.flatMap((species) => species.annualpopulation_count.map((entry) => entry.year))));
    yearsData.sort((a, b) => a - b);

    // Sort speciesData by species_name
    speciesData.sort((a, b) => a.species_name.localeCompare(b.species_name));

    const speciesPopulation = {
    labels: yearsData.map((year) => year.toString()),
    datasets: speciesData.map((species) => ({
        label: species.species_name,
        data: yearsData.map((year) => {
        const yearData = species.annualpopulation_count.find((entry) => entry.year === year);
        return yearData ? yearData.year_total : 0;
        }),
        fill: false,
        borderColor: species.species_colour,
        borderWidth: 1,
    })),
    };

    const speciesOptions = {
        plugins: {
            datalabels: {
                display: false,
            },
            legend: {
                display: true,
                position: 'bottom' as 'bottom',
            },
            title: {
                display: true,
                text: 'Species Count per Year', 
                font: {
                    size: 16, 
                    weight: 'bold' as 'bold', 
                },
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Year', // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 65,
                    max: 260,
                },
                title: {
                    display: true,
                    text: 'Count', // Y-axis label
                    font: {
                        size: 14,
                    },
                },
            },
        },
    };

    const fetchPropertyPopulation = () => {
        setLoading(true)
        axios.get(`${FETCH_PROPERTY_POPULATION_SPECIES}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setSpeciesData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchPropertyPopulation()
    }, [propertyId, startYear, endYear, selectedSpecies])


    return (
        <Grid>
            {!loading ? (
                <Line data={speciesPopulation} options={speciesOptions} height={400} width={1000} />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    )
};

export default SpeciesLineChart;
