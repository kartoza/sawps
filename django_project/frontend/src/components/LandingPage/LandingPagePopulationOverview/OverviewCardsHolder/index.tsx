import React, { FC ,useState, useEffect} from 'react';
import './styles.scss'
import SpeciesCard from '../SpeciesCard';
import axios from 'axios';
import { alpha } from '@mui/material';

interface IOverviewCardsHolder{}

interface FrontPageSpecies {
    id: number;
    species_name: string;
    icon?: string;
    total_population: number;
    population_growth: number;
    population_loss: number;
    colour: string;
}

const FETCH_FRONT_PAGE_SPECIES_LIST = '/api/species/front-page/list/'


const OverviewCardsHolder:FC<IOverviewCardsHolder> = ()=>{
    const [species, setSpecies] = useState<FrontPageSpecies[]>([])

    const fetchSpeciesList = () => {
        axios.get(FETCH_FRONT_PAGE_SPECIES_LIST).then((response) => {
            if (response) {
                setSpecies(response.data as FrontPageSpecies[])
            }
        }).catch((error) => {
            console.log(error)
        })
    }

    useEffect(() => {
        fetchSpeciesList()
    }, [])

    return(
        <div className='landing-page-overview-cards-holder' data-testid='landing-page-overview-cards-holder'> 
            {species.map((species,index)=>{
                let chartColors = {
                    'line': species.colour,
                    'area': alpha(species.colour, 0.3)
                }
                return <SpeciesCard key={index} species_id={species.id} species_name={species.species_name} pic={species.icon} population={species.total_population.toString()}
                    growth={species.population_growth.toString()} loss={species.population_loss.toString()} chartColors={chartColors} index={index}
            />})}
        </div>
    )
}

export default OverviewCardsHolder