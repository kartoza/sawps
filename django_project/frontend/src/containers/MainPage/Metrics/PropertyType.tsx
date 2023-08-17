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

const FETCH_SPECIES_DENSITY = '/api/total-area-per-property-type/'

const PropertyTypeBarChart = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [propertyTypeData, setPropertyTypeData] = useState([])
    const labels = [];
    const  totalArea= [];

    const fetchActivityPercentageData = () => {
        setLoading(true)
        axios.get(`${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setPropertyTypeData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchActivityPercentageData();
    }, [propertyId, startYear, endYear, selectedSpecies])

    for (const each of propertyTypeData) {
        labels.push(each.property_type__name);
        totalArea.push(each.total_area);
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Population density (individuals/Ha)',
                backgroundColor: '#FF5252',
                borderColor: '#FF5252',
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
                    <Typography>Total area per property type</Typography>
                    <Bar data={data} options={options} height={225} width={1000} />
                    <Typography>Property type</Typography>
                </Box >}
        </Box>
    );
};

export default PropertyTypeBarChart;
