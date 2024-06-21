import React, {useEffect, useState} from 'react';
import BarChart from "../../../components/BarChart";
import { backgroundClip } from 'html2canvas/dist/types/css/property-descriptors/background-clip';


export interface PopulationHistogramItem {
    count: number;
    percentage: number;
    count2: string;
    category_label: string;
    break_group?: string;
}

interface PopulationHistogramChartInterface {
    data: PopulationHistogramItem[];
    chartId: string;
    chartTitle: string;
    chartXLabel: string;
    chartYLabels: string[];
    color: string;
}

const PopulationHistogramChart = (props: PopulationHistogramChartInterface) =>{
    const options = {
        scales: {
            y: {
                grace: '20%',
                display: true,
                stacked: true,
                title: {
                    display: true,
                    text: props.chartYLabels,
                    font: {
                        size: 14,
                    },
                },
                grid: {
                    display: false,
                },
                ticks: {
                    color: "black",
                }
            },
        },
        plugins: {
            datalabels: {
                display: true,
                color: '#000',
                anchor: 'end',
                align: 'end',
                font: {
                    size: 12,
                },
                padding: {
                    top: 0,
                    bottom: 0
                },
                formatter: function(value: any, context: any) {
                    if (context.dataset.counts && context.dataset.counts[context.dataIndex])
                        return `n=${context.dataset.counts[context.dataIndex]}`;
                    return '';
                }
            },
        }
    }

    const labels = props.data.map(item => item.category_label);
    const datasets = [{
        label: props.chartTitle,
        data: props.data.map(item => item.percentage),
        counts: props.data.map(item => item.count),
        backgroundColor: props.color,
        categoryPercentage: 0.9,
        barPercentage: 0.9
    }]
    
    return (
        <BarChart
            chartData={{ labels: labels, datasets: datasets }}
            chartId={props.chartId}
            chartTitle={props.chartTitle}
            xLabel={props.chartXLabel}
            indexAxis={'x'}
            showLegend={false}
            options={options}
        />
    )
}

export default PopulationHistogramChart;
