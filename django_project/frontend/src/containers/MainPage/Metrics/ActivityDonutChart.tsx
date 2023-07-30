import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import { Doughnut } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import "./index.scss";
import axios from "axios";
import Loading from "../../../components/Loading";


Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_ACTIVITY_PERCENTAGE_URL = '/activity-percentage/'

const ActivityDonutChart = () => {
    const [loading, setLoading] = useState(false)
    const [activityData, setActivityData] = useState([])
    const [activityType,setActivityType] = useState({})


    const fetchActivityPercentageData = () => {
        setLoading(true)
        axios.get(FETCH_ACTIVITY_PERCENTAGE_URL).then((response) => {
            setLoading(false)
            if (response.data) {
                setActivityData(response.data.data)
                setActivityType(response.data.activity_colours)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchActivityPercentageData()
    }, [])

    const labels = Object.keys(activityType);

    const donutOptions = {
        cutout: 50,
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                enabled: false
            },
            legend: {
                display: true,
                position: 'right' as 'right',
                labels: {
                    usePointStyle: true,
                    font: {
                        size: 13,
                    },
                    generateLabels: (chart: any) => {
                        const { datasets } = chart.data;
                        return datasets[0].data.map((data: any, index: any) => ({
                            text: Object.keys(activityType)[index],
                            fillStyle: datasets[0].backgroundColor[index],
                            hidden: false,
                            lineCap: 'round',
                            lineDash: [] as number[],
                            lineDashOffset: 0,
                            lineJoin: 'round',
                            lineWidth: 5,
                            strokeStyle: datasets[0].backgroundColor[index],
                            pointStyle: 'rect',
                            rotation: 0,
                        }))
                    },
                },
            },
            datalabels: {
                display: true,
                color: '#fff',
                formatter: (value: any, context: any) => {
                    if (value > 0) {
                        const dataset = context.chart.data.datasets[0];
                        const sum = dataset.data.reduce((acc: any, cur: any) => acc + cur, 0);
                        const percentage = ((value * 100) / sum).toFixed(1) + '%';
                        return percentage;
                    }
                    return ''
                },
                font: {
                    size: 11,
                    weight: 'bold' as 'bold',
                },
            }
        }
    };

    return (
        <Box className="white-chart chartFullWidth leftBoxRound">
            <Typography>Activity data, as % of total population</Typography>
            {loading ? <Loading /> :
                <Box className="BoxChartType">
                    {activityData?.map((item, index) => {
                        const speciesDonutData = {
                            labels: labels,
                            datasets: [
                                {
                                    data: labels.map((label) => {
                                        const activity = item?.activities?.find((activity: any) => activity[label]);
                                        return activity ? activity[label] : 0;
                                    }),
                                    backgroundColor: Object.values(activityType),
                                    borderWidth: 1
                                },
                            ],
                        };
                        return (
                            <Box key={index} className="chartHalf">
                                <Typography className="text-left">{item?.species_name}</Typography>
                                <Box className="charBox">
                                    <Box className="chart-container">
                                        <Doughnut data={speciesDonutData} options={donutOptions} height={200} width={70} />
                                    </Box>
                                </Box>
                                <Box className="chart-img">
                                    <Box className="icon-image">
                                        <img src={item?.icon} alt='Icon image' />
                                    </Box>
                                    <Typography className="charttext">{item?.total}</Typography>
                                </Box>
                            </Box>
                        );
                    })}
                </Box>
            }
        </Box>
    );
};

export default ActivityDonutChart;
