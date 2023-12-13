import React, {useState, useEffect} from 'react';
import {Line} from 'react-chartjs-2'
import ChartContainer from "../../../components/ChartContainer";
import './index.scss';

export interface PopulationTrendItem {
    year: number;
    sum_fitted: number;
    lower_ci: number;
    upper_ci: number;
    raw_pop_est?: number;
}

export interface PopulationTrendChartInterface {
    data: PopulationTrendItem[];
    chartTitle: string;
    chartId: string;
    showRawPopEst?: boolean;
}

const PopulationTrendChart = (props: PopulationTrendChartInterface) => {
    const [chartData, setChartData] = useState(null)

    useEffect(() => {
        let _datasets = []
        if (props.showRawPopEst) {
            _datasets.push({
                label: "Counts",
                data: props.data,
                parsing: {
                    xAxisKey: "year",
                    yAxisKey: "raw_pop_est",
                },
                borderColor: "rgba(0, 0, 0, 0)", // Transparent line
                pointBackgroundColor: "rgba(0, 0, 0, 0.8)", // Point color
                pointRadius: 4, // Point size
            })
        }
        _datasets.push({
            label: "Population",
            data: props.data,
            borderColor: "#86BC8B",
            fill: false,
            parsing: {
              xAxisKey: "year",
              yAxisKey: "sum_fitted",
            },
            pointRadius: 0, // Disable points for the trend line
        })
        _datasets.push({
            label: "upper_ci",
            data: props.data,
            fill: 1,
            parsing: {
              xAxisKey: "year",
              yAxisKey: "upper_ci",
            },
            backgroundColor: "rgba(117, 179, 122, 0.63)",
            showLine: false,
            pointRadius: 0,
        })
        _datasets.push({
            label: "lower_ci",
            data: props.data,
            fill: 1,
            parsing: {
              xAxisKey: "year",
              yAxisKey: "lower_ci",
            },
            backgroundColor: "rgba(117, 179, 122, 0.63)",
            showLine: false,
            pointRadius: 0,
        })
        setChartData({
            labels: props.data.map((a) => {
              if (a.year % 1 === 0) return a.year;
              return "";
            }),
            datasets: _datasets,
          })
    }, [props.data])

    const options:object={
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
              beginAtZero: true,
              grace:50,
              title: {
                display: true,
                text: 'Population', // Y-axis label
                font: {
                  size: 14,
                },
              },
            },
            x: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Year', // X-axis label
                font: {
                  size: 14,
                },
              },
              ticks: {
                maxRotation: 45,
                minRotation: 45
              }
            },
        },
        plugins: {
            datalabels: {
              display: false,
            },
            legend: {
                display: false,
            },
            tooltips: {
                enabled: true
           },
           title: {
            display: false
          },
        }
    }

    return (
        <ChartContainer title={props.chartTitle}>
            <div className={'PopulationTrendChartContainer'}>
                {chartData !== null && <Line
                    key={props.chartId}
                    data={chartData}
                    options={options}
                    plugins={[]}
                    className={'PopulationTrendChart'}
                />}
            </div>
        </ChartContainer>
    )
}

export default PopulationTrendChart
