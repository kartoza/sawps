import React, {useEffect, useRef, useState} from "react";
import {Box, Button, Grid, Typography} from "@mui/material";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import PopulationTrend from "../Metrics/PopulationTrend";
import {useGetTaxonDetailQuery, useGetUserInfoQuery} from "../../../services/api";
import './index.scss';
import Skeleton from "@mui/material/Skeleton";
import SpeciesChart from "../../../components/LandingPage/LandingPagePopulationOverview/SpeciesChart";

const FETCH_GRAPH_SPECIES_LIST = '/api/species/trend-page/'

const Trends = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [icon, setIcon] = useState<string>('/static/images/footer/default-species.png')
    const [totalArea, setTotalArea] = useState<number>(0)
    const [totalPopulation, setTotalPopulation] = useState<number>(0)
    const [lineColour, setLineColour] = useState<string>('#000000')
    const [rerender, setRerender] = useState<boolean>(false)
    const contentRef = useRef(null);
    const { data: taxonDetail, isLoading: isTaxonDetailLoading, isSuccess } = useGetTaxonDetailQuery(selectedSpecies)

    // Declare errorMessage as a state variable
    const [showCharts, setShowCharts] = useState(false);

    useEffect(() => {
        if(selectedSpecies){
            setRerender(false)
            setShowCharts(true)
        }else {
            setShowCharts(false);
        }
    }, [propertyId, startYear, endYear, selectedSpecies])

    useEffect(() => {
        if (taxonDetail?.id) {
            setLineColour(taxonDetail.colour)
            setTotalPopulation(taxonDetail.total_population)
            setTotalArea(taxonDetail.total_area)
            setIcon(taxonDetail.graph_icon ? taxonDetail.graph_icon : '/static/images/default-species.png')
            setRerender(true)
        }
    }, [isSuccess, taxonDetail])

    return (
      <Box>
        <Box className="charts-container">

          {showCharts ? (
            <Grid container spacing={2} ref={contentRef}>
              {selectedSpecies && rerender && (
                <Grid item xs={12} md={6}>
                    <div className='species-card-container' data-testid='species-card-container'>
                        <div className='species-card-image-container'>
                              <img
                                src={icon}
                                className='species-card-image'
                                data-testid='species-card-image'
                              />
                            <p className='species-card-text species-name-text'> {selectedSpecies} </p>
                            <hr/>
                        </div>
                        <div className='species-card-text-container'>
                            <p className='species-card-text' data-testid='species-card-population'>Total Population : {totalPopulation}</p>
                            <p className='species-card-text' data-testid='species-card-total-area'>Total Area : {+totalArea.toFixed(2)}</p>
                        </div>
                        <div className='ChartHolder'>
                          <PopulationTrend
                            selectedSpecies={selectedSpecies}
                            propertyId={propertyId}
                            startYear={startYear}
                            endYear={endYear}
                            loading={loading}
                            setLoading={setLoading}
                            lineColor={lineColour}
                            onEmptyDatasets={() => {}}
                          />
                        </div>
                    </div>
                </Grid>
              )}
            </Grid>) : (
            // Render message to user
            <Grid container justifyContent="center" alignItems="center" flexDirection={'column'}>
              <Grid item>
                <Typography variant="body1" color="textPrimary" style={{fontSize: '20px', fontWeight: 'bold'}}>
                  Ready to explore?
                </Typography>
              </Grid>
              <Grid>
                <Typography variant="body1" color="textPrimary" style={{fontSize: '16px', fontWeight: 'bold'}}>
                  Choose a species to view the data as charts.
                </Typography>
              </Grid>
            </Grid>
          )}
        </Box>
        {showCharts && (
          <Box className="download-btn-box" style={{position: 'fixed', bottom: '20px', right: '20px'}}>
            <Button
              onClick={() => alert('This is an experimental feature! No JSON document available.')}
              variant="contained"
              color="primary"
            >
              Download data visualizations
            </Button>
          </Box>
        )}
      </Box>
    )
}

export default Trends
