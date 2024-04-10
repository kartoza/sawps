import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Bar } from 'react-chartjs-2';
import Loading from "../../../components/Loading";
import axios from "axios";
import "./index.scss";

const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/';

const availableColors = [
    'rgba(112, 178, 118, 1)', 
    'rgba(250, 167, 85, 1)', 
    'rgba(157, 133, 190, 1)', 
    '#FF5252', 
    '#616161',
    // additional transparency colors for years
    'rgba(112, 178, 118, 0.5)',  // 50% transparency
    'rgba(255, 82, 82, 0.5)',  // 50% transparency
    'rgba(97, 97, 97, 0.5)',  // 50% transparency
    'rgba(157, 133, 190, 0.5)',  // 50% transparency
    'rgba(250, 167, 85, 0.5)',  // 50% transparency
];

const ActivityBarChart = (props: {
    property: any;
    selectedSpecies: string | string[];
    to: number;
}) => {
    const [loading, setLoading] = useState(false);
    const [activityData, setActivityData] = useState([]);
    const propertyId = props.property;
    var selectedSpecies = props.selectedSpecies;
    var endYear = props.to;
    const [noData, setNoData] = useState(false);

    useEffect(() => {
        if (
            propertyId && 
            selectedSpecies.length > 0 &&
            endYear
        ) {
          fetchActivityData();
        }
    }, [propertyId, selectedSpecies, endYear]); // Re-fetch when propertyId or selectedSpecies change

    const fetchActivityData = async () => {
        setLoading(true);

        try {
            const response = await axios.get(
                `${FETCH_ACTIVITY_TOTAL_COUNT}?start_year=${endYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
            );

            const speciesColors: { [key: string]: string } = {};
            const activityTypeData: { [key: string]: number } = {};

            let datasets: any[] = [];
            response.data.forEach((species: { activities: any; species_name: string | number; colour: any; }) => {
                const activities = species.activities;
                for (let {activity_type, total} of activities) {
                  if (activity_type in activityTypeData) {
                    activityTypeData[activity_type] += total
                  } else {
                    activityTypeData[activity_type] = total
                  }
                }
                const color = typeof species.colour === 'string' ? species.colour : '';
                speciesColors[species.species_name] = color;
            });

            for (const [index, activityType] of Object.keys(activityTypeData).entries()) {
                datasets.push({
                  label: activityType,
                  data: [activityTypeData[activityType]],
                  backgroundColor: availableColors[index % availableColors.length],
              });
            }

            setActivityData(datasets)
            setNoData(datasets.length === 0)            
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setNoData(true);
            setLoading(false);
        }
    };

    const BarData = {
        labels: ['labels'],
        datasets: activityData
    };
    
    const options = {
      indexAxis: 'x' as const,
      scales: {
        x: {
          beginAtZero: false,
          display: false,
          stacked: false,
          barPercentage: 1, // Set barPercentage to 1 to make bars fill the label space
          categoryPercentage: 1, // Set categoryPercentage to 1 to make bars fill the label space
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
            text: 'Total', // Y-axis label
            font: {
              size: 14,
            },
          },
        },
      },
      plugins: {
        responsive: true,
        maintainAspectRatio: false,
        tooltip: {
          enabled: true,
        },
        datalabels: {
          display: false,
        },
        legend: {
          display: true,
          position: 'bottom' as 'bottom',
          labels: {
            boxWidth: 20,
            boxHeight: 13,
            padding: 12,
            font: {
              size: 10,
              weight: "bold" as "bold"
            }
          },
        },
        
      },
    } as const;

    return (
        <Box className="white-chart chartFullWidth leftBoxRound">
            {propertyId && selectedSpecies.length > 0 ? (
                loading ? (
                    <Loading />
                ) : (
                    noData ? (
                        <Typography>No data available for current selections.</Typography>
                    ) : (
                        <Box>
                            <Typography>Species activity data, as totals by method for {endYear}</Typography>
                            <Box className="BoxChartType">
                                <Bar data={BarData} options={options} />
                            </Box>
                        </Box>
                    )
                )
            ) : (
                <Typography>Please select a property and species.</Typography>
            )}
        </Box>
    );
};

export default ActivityBarChart;
