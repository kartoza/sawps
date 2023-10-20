import React, { useEffect, useState } from "react";
import {alpha, Box, Button, Checkbox, Grid, ListItemText, Typography} from "@mui/material";

import OverviewCardsHolder, {Fr} from '../../../components/LandingPage/LandingPagePopulationOverview/OverviewCardsHolder'
import './index.scss';
import Topper from "../Data/Topper";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Loading from "../../../components/Loading";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import SpeciesCard from "../../../components/LandingPage/LandingPagePopulationOverview/SpeciesCard";
import axios from "axios";

const FETCH_GRAPH_SPECIES_LIST = '/api/species/trend-page/'

const Trends = () => {
    const [loading, setLoading] = useState(false)
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    // const speciesListUrl = props.speciesListUrl ? props.speciesListUrl : FETCH_FRONT_PAGE_SPECIES_LIST
    const [species, setSpecies] = useState<FrontPageSpecies[]>([])

    const fetchSpeciesList = () => {
        axios.get(`${FETCH_GRAPH_SPECIES_LIST}?species=${selectedSpecies}`).then((response) => {
            if (response) {
                setSpecies(response.data as FrontPageSpecies[])
            }
        }).catch((error) => {
            console.log(error)
        })
    }

    useEffect(() => {
        fetchSpeciesList()
    }, [selectedSpecies])

    return (
      <Box className='dataContainer'>
                {loading ? <Loading /> :
                  <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12, xl: 12 }}  data-testid='landing-page-overview-cards-holder' className='landing-page-overview-cards-holder-flex'>
                      {species.map((species,index)=>{
                          let chartColors = {
                              'line': species.colour,
                              'area': alpha(species.colour, 0.3)
                          }
                          return <Grid item xs={4} xl={2} key={index}>
                              <SpeciesCard key={index} species_id={species.id} species_name={species.species_name} pic={species.icon} population={species.total_population.toString()}
                                  total_area={species.total_area} chartColors={chartColors} index={index}
                              />
                          </Grid>
                      })}
                  </Grid>
                }
                {loading ? <Loading/> : (
                  <Box className="downlodBtn">
                    <Button onClick={() => {}} variant="contained" color="primary">
                        Download data Report
                    </Button>
                    <Button onClick={() => {}} variant="contained" color="primary">
                        Download data CSV
                    </Button>
                </Box>
                )}
            </Box>
    )
}

export default Trends
