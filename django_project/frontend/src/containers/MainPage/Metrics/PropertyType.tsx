import React, { useEffect, useState } from "react";
import { Box, Typography, Card, Grid } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import Loading from "../../../components/Loading";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import "./index.scss";
import { ChartCard } from "./ChartCard";

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_DENSITY = '/api/total-area-per-property-type/';

const PropertyTypeBarChart = (props: any) => {
    const { selectedSpecies, propertyId, startYear, endYear, loading, setLoading } = props;
    const [propertyTypeData, setPropertyTypeData] = useState([]);
    const labels: string[] = [];
    const totalArea: number[] = [];

    const fetchActivityPercentageData = () => {
        setLoading(true);
        axios
            .get(`${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`)
            .then((response) => {
                setLoading(false);
                if (response.data) {
                    // Sort property types alphabetically
                    const sortedData = response.data.sort((a: { property_type__name: string; }, b: { property_type__name: any; }) =>
                        a.property_type__name.localeCompare(b.property_type__name)
                    );
                    setPropertyTypeData(sortedData);
                }
            })
            .catch((error) => {
                setLoading(false);
                console.log(error);
            });
    };

    useEffect(() => {
        fetchActivityPercentageData();
    }, [propertyId, startYear, endYear, selectedSpecies]);

    for (const each of propertyTypeData) {
        labels.push(each.property_type__name);
        totalArea.push(each.total_area);
    }

    // Assign colors based on availableColors array
    const availableColors: string[] = [
        "#FF5252",
        "rgb(83 83 84)",
        "#75B37A",
        "#282829",
        "#F9A95D",
        "#000000",
        "#70B276",
        "#9F89BF",
    ];

    // Ensure we have enough colors for all property types
    const backgroundColors = labels.map((_, index) => availableColors[index % availableColors.length]);

    const data = {
        labels: labels,
        datasets: [
            {
                label: labels.length === 1 ? labels[0] : 'Population density (individuals/Ha)',
                backgroundColor: backgroundColors,
                borderColor: backgroundColors,
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
            legend: {
                display: true,
                position: 'bottom' as 'bottom',
            },
            title: {
                display: true,
                text: 'Total area per property type',
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
                    text: 'Property type', // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50,
                    max: 200,
                },
                title: {
                    display: true,
                    text: 'Area (Ha)', // Y-axis label
                    font: {
                        size: 14,
                    },
                },
            },
        },
    };

    return (
        <Grid>
            {!loading ? (
                <Bar data={data} options={options} height={400} width={1000} />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    );
};

export default PropertyTypeBarChart;
