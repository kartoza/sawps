import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import Loading from "../../../components/Loading";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import "./index.scss";


Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_AREA_AVAILABLE = '/api/total-area-available-to-species/'

const PropertyAvailableBarChart = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [propertyAreaAvailableData, setPropertyAreaAvailableData] = useState([])
    const labels = [];
    const  totalArea= [];

    const fetchActivityPercentageData = () => {
        setLoading(true)
        axios.get(`${FETCH_SPECIES_AREA_AVAILABLE}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setPropertyAreaAvailableData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchActivityPercentageData();
    }, [propertyId, startYear, endYear, selectedSpecies])

    for (const each of propertyAreaAvailableData) {
        labels.push(each.property__name);
        totalArea.push(each.total_species_area);
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Population density (individuals/Ha)',
                backgroundColor: '#86BC8B',
                borderColor: '#86BC8B',
                borderWidth: 1,
                data: totalArea,
            },
        ],
    };

    const options = {
        plugins: {
            datalabels: {
                display: false,
            },
            legend:{
                display: false,
            }
        },
        scales: {
            x: {
                beginAtZero: true,
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50,
                    max: 200,
                },
            },
        },
    }

    return (
        <Box>
            {loading ? <Loading /> :
                <Box className="white-chart" >
                    <Typography>Total area available to species (ha)</Typography>
                    <Bar data={data} options={options} height={225} width={1000} />
                    <Typography>Properties</Typography>
                </Box >}
        </Box>
    );
};

export default PropertyAvailableBarChart;
