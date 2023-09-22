import React, { useEffect, useState } from "react";
import { Box, Typography, Card } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import Loading from "../../../components/Loading";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import "./index.scss";
import {ChartCard} from "./ChartCard";


Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_DENSITY = '/api/total-area-per-property-type/'

const PropertyTypeBarChart = (props:any) => {
    const {selectedSpecies, propertyId, startYear, endYear, loading, setLoading} = props
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
        <ChartCard
            loading={loading}
            chartComponent={
                <Bar data={data} options={options} height={225} width={1000} />
            }
            title={'Total area per property type'}
            xLabel={'Property type'}
        />
    )
};

export default PropertyTypeBarChart;
