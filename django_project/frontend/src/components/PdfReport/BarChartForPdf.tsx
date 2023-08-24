import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from "react-chartjs-2";
import axios from "axios";
import Loading from "../Loading";
import "./index.scss";

// fetch species list
const FETCH_SPECIES_LIST = '/api/species-list/';

interface Species {
    annualpopulation_count: { year: number; year_total: number; }[];
    species_name: string;
    species_colour: string;
    year: number;
    year_total: number;
    icon?: string;
}

const BarChartForPdf = () => {
    const [loading, setLoading] = useState(true);
    const [species, setSpecies] = useState<Species[]>([]);
    const availableColors = ['red', 'purple', 'orange', 'black', 'green'];

    const fetchSpeciesList = () => {
        axios.get(FETCH_SPECIES_LIST)
        .then((response) => {
            if (response) {
                setSpecies(response.data as Species[]);
                setLoading(false);
            }
        })
        .catch((error) => {
            console.log(error);
        });
    }

    useEffect(() => {
        fetchSpeciesList();
    }, []);

    const generateChartData = (speciesData: Species) => {
        const color = speciesData.species_colour || availableColors[Math.floor(Math.random() * availableColors.length)];

        const labels = speciesData.annualpopulation_count.map((entry: { year: any }) => entry.year);
        const femaleData = speciesData.annualpopulation_count.map((entry: { year_total: any; }) => entry.year_total);
        const maleData = speciesData.annualpopulation_count.map((entry: { year_total: any; }) => -entry.year_total); // Negative values for males

        return {
            labels: labels,
            datasets: [
                {
                    label: 'Male',
                    data: maleData,
                    backgroundColor: color,
                    borderWidth: 1
                },
                {
                    label: 'Female',
                    data: femaleData,
                    backgroundColor: color,
                    borderWidth: 1
                }
            ]
        };
    };

    const generatedCharts = species.map((specie, index) => (
        <Box key={index}>
            <Typography>{specie.species_name}</Typography>
            {specie.icon && <img src={specie.icon} alt={specie.species_name} />}
            <Bar data={generateChartData(specie)} />
        </Box>
    ));

    return (
        <Box>
            {!loading ? (
                generatedCharts.length > 0 ? (
                    generatedCharts
                ) : (
                    <Typography>No species data available.</Typography>
                )
            ) : (
                <Loading />
            )}
        </Box>
    );
};

export default BarChartForPdf;
