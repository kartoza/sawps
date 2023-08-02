import React, {FC} from 'react';
import './styles.scss'
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Legend,
    Tooltip,
    Filler,
    LegendItem,
} from 'chart.js';

import {Line} from 'react-chartjs-2'

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Legend,
    Tooltip,
    Filler,
);

interface ISpeciesChartProps{
    species_name?:string,
    areaFillColor?:string,
    areaLineColor?:string,
    lineColor?:string,
    index?:number
}

// National trend structure
const testData = [
    {
        "year": 2010,
        "fit": 322.2998,
        "se.fit": 79.5974,
        "lower_ci": 83.5075,
        "upper_ci": 561.0921
    },
    {
        "year": 2010.5,
        "fit": 319.1916,
        "se.fit": 73.9494,
        "lower_ci": 97.3435,
        "upper_ci": 541.0396
    },
    {
        "year": 2011,
        "fit": 316.0833,
        "se.fit": 68.687,
        "lower_ci": 110.0223,
        "upper_ci": 522.1443
    },
    {
        "year": 2011.5,
        "fit": 312.9751,
        "se.fit": 63.908,
        "lower_ci": 121.2509,
        "upper_ci": 504.6992
    },
    {
        "year": 2012,
        "fit": 309.8668,
        "se.fit": 59.7321,
        "lower_ci": 130.6705,
        "upper_ci": 489.0631
    },
    {
        "year": 2012.5,
        "fit": 306.7586,
        "se.fit": 56.2978,
        "lower_ci": 137.8652,
        "upper_ci": 475.652
    },
    {
        "year": 2013,
        "fit": 303.6503,
        "se.fit": 53.7514,
        "lower_ci": 142.3962,
        "upper_ci": 464.9044
    },
    {
        "year": 2013.5,
        "fit": 300.5421,
        "se.fit": 52.224,
        "lower_ci": 143.8699,
        "upper_ci": 457.2142
    },
    {
        "year": 2014,
        "fit": 297.4338,
        "se.fit": 51.8025,
        "lower_ci": 142.0264,
        "upper_ci": 452.8412
    },
    {
        "year": 2014.5,
        "fit": 294.3255,
        "se.fit": 52.5051,
        "lower_ci": 136.8103,
        "upper_ci": 451.8408
    },
    {
        "year": 2015,
        "fit": 291.2173,
        "se.fit": 54.2788,
        "lower_ci": 128.381,
        "upper_ci": 454.0536
    },
    {
        "year": 2015.5,
        "fit": 288.109,
        "se.fit": 57.0164,
        "lower_ci": 117.0599,
        "upper_ci": 459.1582
    },
    {
        "year": 2016,
        "fit": 285.0008,
        "se.fit": 60.584,
        "lower_ci": 103.2488,
        "upper_ci": 466.7528
    },
    {
        "year": 2016.5,
        "fit": 281.8925,
        "se.fit": 64.8445,
        "lower_ci": 87.3591,
        "upper_ci": 476.426
    },
    {
        "year": 2017,
        "fit": 278.7843,
        "se.fit": 69.6722,
        "lower_ci": 69.7677,
        "upper_ci": 487.8009
    },
    {
        "year": 2017.5,
        "fit": 275.676,
        "se.fit": 74.9594,
        "lower_ci": 50.7979,
        "upper_ci": 500.5542
    },
    {
        "year": 2018,
        "fit": 272.5678,
        "se.fit": 80.6173,
        "lower_ci": 30.7159,
        "upper_ci": 514.4197
    },
    {
        "year": 2018.5,
        "fit": 269.4595,
        "se.fit": 86.5746,
        "lower_ci": 9.7358,
        "upper_ci": 529.1833
    },
    {
        "year": 2019,
        "fit": 266.3513,
        "se.fit": 92.7744,
        "lower_ci": -11.972,
        "upper_ci": 544.6746
    },
    {
        "year": 2019.5,
        "fit": 71.3343,
        "se.fit": 44.3261,
        "lower_ci": -61.644,
        "upper_ci": 204.3125
    },
    {
        "year": 2020,
        "fit": 65.9006,
        "se.fit": 47.1237,
        "lower_ci": -75.4706,
        "upper_ci": 207.2717
    },
    {
        "year": 2020.5,
        "fit": 60.4669,
        "se.fit": 49.999,
        "lower_ci": -89.53,
        "upper_ci": 210.4637
    },
    {
        "year": 2021,
        "fit": 55.0331,
        "se.fit": 52.9392,
        "lower_ci": -103.7845,
        "upper_ci": 213.8507
    }
]

const SpeciesChart:FC<ISpeciesChartProps> = (props)=>{
    const data={
        labels: testData.map((a) => {
            if (a.year % 2 === 0) return a.year
            return ""
        }),
        datasets:[
            {
                label:props.species_name,
                data:testData,
                borderColor:props.lineColor,
                fill:false,
                parsing: {
                    xAxisKey: 'year',
                    yAxisKey: 'fit'
                },
                pointRadius: 0
            },
            {
                label: 'upper_ci',
                data:testData,
                fill:1,
                parsing: {
                    xAxisKey: 'year',
                    yAxisKey: 'upper_ci'
                },
                backgroundColor: props.areaFillColor,
                showLine: false,
                pointRadius: 0,
            },
            {
                label: 'lower_ci',
                data:testData,
                fill:1,
                parsing: {
                    xAxisKey: 'year',
                    yAxisKey: 'lower_ci'
                },
                backgroundColor: props.areaFillColor,
                showLine: false,
                pointRadius: 0,
            },
        ]
    }

    const options:object={
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio:1.5,
        scales:{
            y:{grace:50},
        },
        plugins: {
            legend: {
                labels: {
                    filter: function(item: LegendItem, chart: ChartJS) {
                        // Logic to remove a particular legend item goes here
                        return !item.text.includes('_ci');
                    }
                }
            },
            tooltips: {
                enabled: false
           }
        }
    }
    
    return(
        <>
            <div className="species-chart-container" data-testid="species-chart">
                <Line
                    data={data}
                    options={options}
                    plugins={[]}
                ></Line>
            </div>
        </>
    )
}

export default SpeciesChart