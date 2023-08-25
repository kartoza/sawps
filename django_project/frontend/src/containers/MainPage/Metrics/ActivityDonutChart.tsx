import React from "react";
import { Box, Typography } from "@mui/material";
import { Doughnut } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Loading from "../../../components/Loading";
import "./index.scss";


Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

interface ActivityDataItem {
    total: number;
    species_name: string;
    icon: string;
    activities?: Array<{ [key: string]: number }>;


}

interface ActivityDonutChartProps {
    activityData: any[];
    activityType: {};
    loading: boolean;
    chartHeading: string;
    showPercentage: boolean;
    activities: any;
    icon: string
    total: number

}

const ActivityDonutChart = (props: ActivityDonutChartProps) => {
    const { activityData, activityType, loading, chartHeading, showPercentage, activities, icon, total } = props
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
                        size: 11,
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
                        if (showPercentage) {
                            const dataset = context.dataset;
                            const sum = dataset.data.reduce((acc: any, cur: any) => acc + cur, 0);
                            const percentage = ((value * 100) / sum).toFixed(1) + '%';
                            return percentage;
                        } else {
                            return value;
                        }
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

    const speciesDonutData = {
        labels: labels,
        datasets: [
            {
                data: labels.map((label) => {
                    const activity = activities?.find((activity: any) => activity[label]);
                    return activity ? activity[label] : 0;
                }),
                backgroundColor: Object.values(activityType),
                borderWidth: 1
            },
        ],
    };

    return (
        <Box>
            <Box className="white-chart chartFullWidth leftBoxRound">
                <Typography>{chartHeading}</Typography>
                {loading ? <Loading /> :
                    <Box className="BoxChartType">
                        {activities.length > 0 &&
                            <Box className="chartHalf">
                                <Box className="charBox">
                                    <Box className="chart-container">
                                        <Doughnut data={speciesDonutData} options={donutOptions} height={186} width={70} />
                                    </Box>
                                </Box>
                                <Box className="chart-img">
                                    <Box className="icon-image">
                                        <img src={icon} alt='Icon image' />
                                    </Box>
                                    <Typography className="charttext">{total}</Typography>
                                </Box>
                            </Box>}
                    </Box>
                }
            </Box>
        </Box>
    );
};

export default ActivityDonutChart;
