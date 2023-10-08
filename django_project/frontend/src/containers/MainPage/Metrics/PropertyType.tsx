import React, { useEffect, useState } from 'react';
import { Grid } from "@mui/material";
import { Bar } from 'react-chartjs-2';
import "./index.scss";
import Loading from '../../../components/Loading';
import axios from 'axios';


// Define colors for each year
const colors = ['rgba(112, 178, 118, 1)', 'rgba(250, 167, 85, 1)', 'rgba(157, 133, 190, 1)', '#FF5252', '#616161'];

const FETCH_SPECIES_DENSITY = '/api/total-area-per-property-type/';

const PropertyTypeBarChart = (props: any) => {
    const { selectedSpecies, propertyId, startYear, endYear, loading, setLoading } = props;
    const [propertyTypeData, setPropertyTypeData] = useState([]);
    const labels: string[] = [];
    const legend_labels: string[] = [];
    const totalArea: number[] = [];
    const datasets: any =[];

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

    // Extract labels and totalArea from propertyTypeData
const backgroundColors: string[] = [];


for (const each of propertyTypeData) {
    labels.push(each.property_type__name); // Use 'property_type__name' as label
    legend_labels.push(each.name);
    totalArea.push(each.total_area);
    backgroundColors.push(colors[labels.length - 1]); // Set background color based on the index
}

for(var count = 0; count < labels.length; count++){
    datasets.push(
        {
            label: legend_labels[count], // Use the 'name' field as the label
            data: [totalArea[count]], // Use 'total_area' as data
            backgroundColor: backgroundColors[count], // Use background color based on the index
        }
    )
}


const data = {
    labels: [''],
    datasets: datasets,
};
    
    const options = {
        indexAxis: 'x' as const,
        scales: {
            x: {
                beginAtZero: false,
                display: true,
                stacked: false,
                title: {
                    display: true,
                    text: 'Property type', // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                display: true,
                stacked: false,
                grid: {
                    display: false,
                },
                ticks: {
                    color: "black",
                },
                title: {
                    display: true,
                    text: 'Area (Ha)', // Y-axis label
                    font: {
                        size: 14,
                    },
                },
                callback: (value: string, index: number) => {
                    return legend_labels[index];
                },
            },
        },
        plugins: {
            tooltip: {
                enabled: true,
                callbacks: {
                    // Use the label callback to customize the tooltip label
                    label: (context: { dataset: any; parsed: any; dataIndex:number; }) => {
                        const datasetLabel = context.dataset.label || '';
                        const value = context.parsed.y;
                        const property = propertyTypeData[context.dataIndex];
                        return `${datasetLabel}: ${property.name} - ${value} Ha`;
                    },
                },
            },
            datalabels: {
                display: false,
            },
            legend: {
                display: true,
                position: 'right' as 'right',
                labels: {
                    boxWidth: 20,
                    boxHeight: 13,
                    padding: 12,
                    font : {
                      size: 10,
                    }
                },
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
    } as const;

    return (
        <Grid>
            {!loading ? (
                <Bar 
                    data={data} 
                    options={options} 
                    height={250} width={500} 
                />
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Grid>
    );
};

export default PropertyTypeBarChart;
