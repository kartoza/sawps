import React, {FC} from 'react';
import './styles.scss'
import SpeciesChart from '../SpeciesChart';

export interface IColors{
  line?:string,
  area?:string
}

interface ISpeciesCardProps{
    pic:string,
    species_name?:string,
    growth:string,
    loss:string,
    chartColors:IColors,
    index?:number,
    population?:string
}

const SpeciesCard:FC<ISpeciesCardProps> =(props)=>{
    return(
            <div className='species-card-container' data-testid='species-card-container'>
                <div className='species-card-image-container'>
                    <img src={props.pic} className='species-card-image' data-testid='species-card-image'/>
                    <p className='species-card-text species-name-text'> {props.species_name} </p>
                    <hr/>
                </div>
                <div className='species-card-text-container'>
                    <p className='species-card-text' data-testid='species-card-population'>Total Population : {props.population}</p>
                    <p className='species-card-text' data-testid='species-card-growth'>Population Growth : {props.growth}</p>
                    <p className='species-card-text' data-testid='species-card-loss'>Population Loss : {props.loss}</p>
                </div>
                <div className='ChartHolder'>
                <SpeciesChart species_name={props.species_name} lineColor={props.chartColors.line} areaFillColor={props.chartColors.area}  index={props.index}/>
                </div>
            </div>
    )   
}

export default SpeciesCard