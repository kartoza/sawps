import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Line } from "react-chartjs-2";
import axios from "axios";
import Loading from "../Loading";
import "./index.scss";

// fetch species list
const FETCH_SPECIES_LIST = '/api/species-list/';

interface Species {
    annualpopulation_count: any;
    species_name: string;
    species_colour: string;
    year: number;
    year_total: number;
    icon?: string;
}

const LineChartForPdf = () => {
    const [loading, setLoading] = useState(true);
    const [species, setSpecies] = useState<Species[]>([]);
    const availableColors = ['#FF5252', '#9D85BE', '#FAA755', '#000', '#70B276'];

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
    
        const labels = speciesData.annualpopulation_count
        .map((entry: { year: any }) => entry.year)
        .sort((a: number, b: number) => a - b); // Sorting the years in ascending order

        const data = speciesData.annualpopulation_count.map((entry: { year_total: any; }) => entry.year_total);
    
        return {
            labels: labels,
            datasets: [{
                label: speciesData.species_name,
                data: data,
                borderColor: color,
                fill: false,
                tension: 0.1
            }]
        };
    };

    // Filter species with no data available
    const speciesWithChartData = species.filter(specie => specie.annualpopulation_count.length > 0);

    // Generate multiple line charts per species
    const generatedCharts = speciesWithChartData.map((specie, index) => (
        <Box key={index} style={{ width: '50%', padding: '10px' }}>
            <Typography>{specie.species_name}</Typography>
            {specie.icon && <img src={specie.icon} alt={specie.species_name} />}
            <Line
                data={generateChartData(specie)}
                options={{
                    plugins: {
                        datalabels: {
                            display: false
                        },
                        legend: {
                            display: false 
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: true
                            }
                        },
                        y: {
                            grid: {
                                display: true
                            }
                        }
                    },
                }}
                // width={800}
                // height={400}
            />
        </Box>
    ));

    return (
        <Box className="white-chart" display="flex" flexWrap="wrap">
            {!loading ? (
                speciesWithChartData.length > 0 ? (
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

export default LineChartForPdf;
