import React, { FC ,useState} from 'react';
import './styles.scss'
import SpeciesCard from '../SpeciesCard';

interface IOverviewCardsHolder{}

const OverviewCardsHolder:FC<IOverviewCardsHolder> = ()=>{
    const [species, setSpecies] = useState([
        {'species_name':'Panthera leo','image':'/static/images/species/leo.png','total_population':'25000','population_growth':'1000','population_loss':'1500'},
        {'species_name':'Panthera pardus','image':'/static/images/species/pardus.png','total_population':'15000','population_growth':'2000','population_loss':'900'},
        {'species_name':'Ceratotherium simum','image':'/static/images/species/simum.png','total_population':'50000','population_growth':'200','population_loss':'900'},
        {'species_name':'Diceros bicornis','image':'/static/images/species/bicornis.png','total_population':'20000','population_growth':'100','population_loss':'200'},
        {'species_name':'Loxodonta africana','image':'/static/images/species/africana.png','total_population':'550000','population_growth':'100','population_loss':'200'},
        {'species_name':'Acinonyx jubatus','image':'/static/images/species/jubatus.png','total_population':'10000','population_growth':'100','population_loss':'200'},

    ])

    const [chartsColors, setChartsColors] = useState([
        {'line':'#86BC8B', 'area':'rgb(112,178,118,.5)'},{'line':'#FAA755','area':'rgb(173,122,75,.5)'},
        {'line':'#9F89BF', 'area':'rgb(111,98,132,.5)'},{'line':'#000', 'area':'rgb(70,70,71,.5)'},
        {'line':'#FFF', 'area':'rgb(169,169,169,.5)'},{'line':'#FF5252', 'area':'rgb(162,64,64,.5)'}
    ])

    return(
        <div className='landing-page-overview-cards-holder' data-testid='landing-page-overview-cards-holder'> 
            {species.map((species,index)=>{
            let chartColors = chartsColors[index]
            return <SpeciesCard key={index} species_name={species.species_name} pic={species.image} population={species.total_population}
            growth={species.population_growth} loss={species.population_loss} chartColors={chartColors} index={index}
            />})}
        </div>
    )
}

export default OverviewCardsHolder