import React, {useRef, useEffect, useState, useMemo} from "react";
import {Chart, registerables} from "chart.js";
import {
    PointWithErrorBar,
    ScatterWithErrorBarsController
} from "chartjs-chart-error-bars";
import ChartContainer from "../../../components/ChartContainer";
import Loading from "../../../components/Loading";
import axios from "axios";
import {uniqueColors} from "../../../utils/Theme";

Chart.register(
    ScatterWithErrorBarsController,
    PointWithErrorBar,
    ...registerables
);

const API_URL= '/api/population-mean-sd-chart/'

interface StandardDeviationMeanChartProps {
    species: string,
    title: string,
    propertyIds: string,
    activityIds: string,
    spatialFilterValues: string
}

export default function StandardDeviationMeanChart(props: StandardDeviationMeanChartProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const chartRef = useRef<Chart | null>(null);
    const [loadingData, setLoadingData] = useState<boolean>(true);
    const [chartRawData, setChartRawData] = useState<any>(null);

    useEffect(() => {
        fetchData();
    }, [props.species, props.propertyIds, props.activityIds, props.spatialFilterValues]);

    const fetchData = () => {
        setLoadingData(true);
        axios.get(
            `${API_URL}?species=${props.species}&property=${props.propertyIds}&activity=${props.activityIds}&spatial_filter_values=${props.spatialFilterValues}`
        ).then((response) => {
            setChartRawData(response.data);
        }).catch((error) => {
            console.error(error);
        }).finally(() => {
            setLoadingData(false);
        })
    };

    const processedData = useMemo(() => {
        if (!chartRawData) return null;
        const categories = Object.keys(chartRawData);
        const groupNames = Object.keys(chartRawData[categories[0]]);
        let classesNames = [...new Set(groupNames.map((groupName) => {
            return groupName.replace('mean_', '').replace('sd_', '');
        }))];
        let datasets = categories.map((category, categoryIndex) => {
            let randomColor = uniqueColors[categoryIndex % uniqueColors.length];
            let groupDataByClass = classesNames.map((className, index) => {
                let mean = chartRawData[category]['mean_' + className];
                let sd = chartRawData[category]['sd_' + className];
                let chartIndex = (categoryIndex + 1) + ((classesNames.length + 1) * index);
                return {
                    x: chartIndex,
                    y: mean,
                    yMin: mean - sd,
                    yMax: mean + sd
                };
            });

            return {
                label: category,
                data: groupDataByClass,
                borderColor: randomColor,
                errorBarColor: randomColor,
                errorBarWhiskerColor: randomColor,
                errorBarLineWidth: 4,
                borderWidth: 4
            };
        });

        return {
            labels: categories,
            datasets: datasets,
            classNames: classesNames
        };
    }, [chartRawData]);

    const separatorPlugin = useMemo(() => ({
        id: 'separator',
        beforeDraw: (chart: any) => {
            if (!processedData) return;
            const ctx = chart.ctx;
            const xAxis = chart.scales.x;
            const yAxis = chart.scales.y;
            let xValues = processedData.classNames.map((className, index) => (index + 1) * 7);
            let formattedNames = processedData.classNames.map(className => className.charAt(0).toUpperCase() + className.slice(1).replaceAll('_', ' '))
            let prevXposition = xAxis.getPixelForValue(0);

            for (const xValue of xValues) {
                if (!xAxis || xValue < xAxis.min || xValue > xAxis.max) {
                    continue;
                }
                const xPosition = xAxis.getPixelForValue(xValue);
                if (xValues.indexOf(xValue) > 0) {
                    prevXposition = xAxis.getPixelForValue(xValues[xValues.indexOf(xValue) - 1]);
                }
                ctx.save();
                ctx.beginPath();
                ctx.strokeStyle = '#adadad';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.moveTo(xPosition, yAxis.top);
                ctx.lineTo(xPosition, yAxis.bottom);
                ctx.stroke();
                ctx.restore();

                ctx.save();
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';
                ctx.fillStyle = '#4f4f4f';
                const text = formattedNames[xValues.indexOf(xValue)];
                const textYPosition = yAxis.bottom + 20;
                const textXPosition = xPosition - ((xPosition - prevXposition) / 2);
                ctx.fillText(text, textXPosition, textYPosition);
                ctx.restore();
            }
        }
    }), [processedData]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas ? canvas.getContext("2d") : null;

        if (chartRef.current) {
            chartRef.current.destroy();
            chartRef.current = null;
        }

        if (ctx && processedData) {
            // eslint-disable-next-line no-new
            chartRef.current = new Chart(ctx, {
                type: "scatterWithErrorBars",
                data: processedData,
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    layout: {
                        padding: {
                            left: 50,
                            right: 50,
                            bottom: 20,
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            display: true,
                            ticks: {
                                display: false,
                                padding: 20,
                            },
                        },
                        y: {
                            beginAtZero: true,
                            display: true,
                            title: {
                                display: true,
                                font: {
                                    size: 14,
                                },
                            }
                        },
                    },
                    plugins: {
                        //@ts-ignore
                        tooltip: {
                            enabled: true,
                            callbacks: {
                                title: function () {
                                    return '';
                                },
                                label: function (context) {
                                    let label = context.dataset.label || '';
                                    let mean = 'Mean : ';
                                    let sd = 'SD : ';
                                    if (context.parsed.y !== null) {
                                        mean += new Intl.NumberFormat('en-US', {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                        }).format(context.parsed.y);

                                        if (context.parsed.yMax !== null) {
                                            sd += new Intl.NumberFormat('en-US', {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2,
                                            }).format((context.parsed.yMax as any - context.parsed.y));
                                        }
                                    }
                                    return [label, mean, sd];
                                }
                            }
                        },
                        datalabels: {
                            display: false
                        },
                        //@ts-ignore
                        separatorPlugin
                    },
                },
                plugins: [separatorPlugin]
            });
        }
    }, [canvasRef, processedData, separatorPlugin]);

    return (
        <ChartContainer title={props.title}>
            { loadingData ? <Loading/> : <canvas ref={canvasRef} style={{ width: 200 }} />}
        </ChartContainer>
    );
}
