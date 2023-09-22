import React, { FC } from 'react';
import './styles.scss';
import SpeciesChart from '../LandingPage/LandingPagePopulationOverview/SpeciesChart';
import Skeleton from '@mui/material/Skeleton';

export interface IColors {
  line?: string;
  area?: string;
}

interface ISpeciesCardProps {
  pic: string;
  species_id: number;
  species_name?: string;
  total_area?: number;
  chartColors: IColors;
  index?: number;
  population?: string;
  textColor?: string; // Add the textColor prop
}

const CustomFirstPageCard: FC<ISpeciesCardProps> = (props) => {
  const textColor = props.textColor || 'black'; // Default to black if not provided

  return (
    <div className='species-card-container' data-testid='species-card-container'>
      <div className='species-card-image-container'>
        {props.pic ? (
          <img src={props.pic} className='species-card-image' data-testid='species-card-image' />
        ) : (
          <Skeleton variant='circular' className='species-card-no-image' />
        )}
        <p className='species-card-text species-name-text' style={{ color: textColor, fontSize: '22px', fontWeight: 'bold' }}>
          {props.species_name}
        </p>
        <hr />
      </div>
      <div className='species-card-text-container'>
        <p className='species-card-text' style={{ color: textColor, fontSize: '20px' }} data-testid='species-card-population'>
          Total Population : {props.population}
        </p>
        <p className='species-card-text' style={{ color: textColor, fontSize: '20px' }} data-testid='species-card-total-area'>
          Total Area : {props.total_area}
        </p>
      </div>
      <div className='ChartHolder'>
        <SpeciesChart species_id={props.species_id} species_name={props.species_name} lineColor={props.chartColors.line} areaFillColor={props.chartColors.area} index={props.index} />
      </div>
    </div>
  );
};

export default CustomFirstPageCard;
