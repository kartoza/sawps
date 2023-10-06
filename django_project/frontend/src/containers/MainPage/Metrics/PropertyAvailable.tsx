import React, { useEffect, useState } from "react";
import { Box, Grid, Typography } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import Loading from "../../../components/Loading";
import "./index.scss";
import Card from "@mui/material/Card";
import { ChartCard } from "./ChartCard";

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_AREA_AVAILABLE = '/api/total-area-available-to-species/';

interface PropertyAreaAvailableData {
    property_name: string;
    area: number;
}

interface PropertyAvailableBarChartProps {
    selectedSpecies: string;
    propertyId: string;
    startYear: number;
    endYear: number;
    loading: boolean;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const PropertyAvailableBarChart: React.FC<PropertyAvailableBarChartProps> = (props) => {
    const { selectedSpecies, propertyId, startYear, endYear, loading, setLoading } = props;
    const [propertyAreaAvailableData, setPropertyAreaAvailableData] = useState<PropertyAreaAvailableData[]>([]);
    const labels: string[] = [];
    const totalArea: number[] = [];

    const availableColors: string[] = [
        "#FF5252",
        "rgb(83 83 84)",
        "#75B37A",
        "#282829",
        "#F9A95D",
        "#000000",
        "#70B276",
        "#9F89BF",
        "#FF5252", // Repeating the colors for more options if needed
        "rgb(83 83 84)",
        "#75B37A",
    ];

    const fetchActivityPercentageData = () => {
        setLoading(true);
        axios.get(`${FETCH_SPECIES_AREA_AVAILABLE}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`)
            .then((response) => {
                setLoading(false);
                if (response.data) {
                    setPropertyAreaAvailableData(response.data);
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

    for (const each of propertyAreaAvailableData) {
        labels.push(each.property_name);
        totalArea.push(each.area);
    }

    const backgroundColors: string[] = labels.map((label, index) => {
        const colorIndex = index % availableColors.length; // Use modulo to cycle through available colors
        return availableColors[colorIndex];
    });

    const data = {
        labels: propertyAreaAvailableData.map((nextProperty) => nextProperty.property_name),
        datasets: [
            {
                label: propertyAreaAvailableData[0]?.property_name || 'Total area available to species',
                backgroundColor: availableColors.slice(0, propertyAreaAvailableData.length),
                borderColor: availableColors.slice(0, propertyAreaAvailableData.length),
                borderWidth: 1,
                data: propertyAreaAvailableData.map((nextProperty) => nextProperty.area),
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
                labels: {
                    font: {
                        size: 11,
                    },
                },
                generateLabels: (chart: { data: { labels: any[]; }; }) => {
                    const labels = chart.data.labels.slice();
                    return labels.map((label: any, index:  number) => {
                        return {
                            text: label, // Use the property name as the legend label
                            fillStyle: backgroundColors[index], // Assign the corresponding background color
                        };
                    });
                },
            },
            title: {
                display: true,
                text: 'Total area available to species',
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
                    text: 'Properties', // X-axis label
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

export default PropertyAvailableBarChart;
