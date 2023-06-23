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

const SpeciesChart:FC<ISpeciesChartProps> = (props)=>{
    const data={
        labels:['January', 'February', 'March', 'April','May', 'June', 'July'],
        datasets:[{
            label:props.species_name,
            data:[65, 75, 78, 73, 78, 75, 65],
            borderColor:props.lineColor,
            fill:false,
        }]
    }

    const shadingArea = {
        id:"shadingArea",
        beforeDatasetsDraw(chart:any,args:any,pluginOptions:object){
            const {ctx,chartArea, scales} = chart;
            const y:{height:number,max:number} = scales.y;
            const tickHeight:number = y.height / y.max;
            let numberOfDataPoints:number = chart.data.labels.length;
            ctx.save()
            ctx.beginPath();
            ctx.moveTo(chart.getDatasetMeta(0).data[0].x, chart.getDatasetMeta(0).data[0].y+(tickHeight*30));
            for(let i=1; i<numberOfDataPoints;i++){
                ctx.lineTo(chart.getDatasetMeta(0).data[i].x, chart.getDatasetMeta(0).data[i].y+(tickHeight*30));
            };

            for(let i=numberOfDataPoints-1;0<i;i--){
                ctx.lineTo(chart.getDatasetMeta(0).data[i].x, chart.getDatasetMeta(0).data[i].y-(tickHeight*30));
            }
            ctx.lineTo(chart.getDatasetMeta(0).data[0].x, chart.getDatasetMeta(0).data[0].y-(tickHeight*30));
            ctx.closePath();
            ctx.fillStyle = props.areaFillColor;
            ctx.fill();
            ctx.restore();
        
        }
    }

    const options:object={
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio:1.5,
        scales:{
            y:{grace:50},
        },    }
    
    return(
        <>
            <div className="species-chart-container" data-testid="species-chart">
                <Line
                    data={data}
                    options={options}
                    plugins={[shadingArea]}
                ></Line>
            </div>
        </>
    )
}

export default SpeciesChart