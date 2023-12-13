import React, {useEffect, useState} from "react";
import { Box, Button, Checkbox, ListItemText, Typography, Grid } from "@mui/material";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import {
    useGetTaxonDetailQuery,
    TaxonDetail
} from "../../../services/api";
import { displayDateTime } from "../../../utils/Helpers";


interface TopperProps {
    activity: string;
    organisationId: string;
    propertyId: string;
    endYear: number;
    startYear: number;
    species: string;
}

const getTrendsTitle = (taxonDetail: TaxonDetail) => {
    if (taxonDetail?.model_updated_on)
        return `These trend models were created on ${displayDateTime(taxonDetail?.model_updated_on, '-')} using the South African Wildlife Population System (SAWPS). `
    return 'Insufficient amount of data for this species to generate trend models. '
}


const Topper = () => {
    const [tab, setTab] = useState<string>('')
    const startYearDisabled = ['map', 'charts'].includes(tab);
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const selectedSpeciesList = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpeciesList).split(',').join(', ')
    const selectedSpeciesListCount = selectedSpeciesList.split(', ').length
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const activityId = useAppSelector((state: RootState) => state.SpeciesFilter.activityId)
    const propertyName = useAppSelector((state: RootState) => state.SpeciesFilter.propertyName)
    const activityName = useAppSelector(
      (state: RootState) => state.SpeciesFilter.activityName
    ).split(',').join(', ')
    const organisationName = useAppSelector((state: RootState) => state.SpeciesFilter.organisationName)
    const organisationCount = useAppSelector((state: RootState) => state.SpeciesFilter.organisationCount)
    const propertyCount = useAppSelector((state: RootState) => state.SpeciesFilter.propertyCount)
    const activityCount = useAppSelector((state: RootState) => state.SpeciesFilter.activityCount)
    const today = new Date()
    const todayDate = String(today.getDate()).padStart(2, '0')
    const todayMonth = String(today.getMonth() + 1).padStart(2, '0')
    const todayYear = today.getFullYear()
    const todayStr = [todayDate, todayMonth, todayYear].join('/')
    const {data: taxonDetail, isLoading: isTaxonDetailLoading, isSuccess} = useGetTaxonDetailQuery(selectedSpecies)
    const [speciesIcon, setSpeciesIcon] = useState("/static/images/default-species-topper.svg")

    useEffect(() => {
        const pathname = window.location.pathname.replace(/\//g, '');
        setTab(pathname)
    }, [window.location.pathname])

    useEffect(() => {
        if (tab === 'reports') {
            setSpeciesIcon("/static/images/default-species-topper.svg")
        }
    }, [tab])


    useEffect(() => {
        if (tab === 'reports') {
            setSpeciesIcon("/static/images/default-species-topper.svg")
        }
        else if (taxonDetail) {
            if (taxonDetail.topper_icon) {
                setSpeciesIcon(taxonDetail.topper_icon)
            } else {
                setSpeciesIcon("/static/images/default-species-topper.svg")
            }
        }
    }, [isSuccess, taxonDetail])

    return (
      <Box className={'topper-container'}>
          <Box>
              <Box padding={'10px'}>
                  <Box borderBottom={'thin solid'}>
                      <b>SAWPS SUMMARY REPORT</b>
                  </Box>
                  <Box>
                      <Box>
                          {tab === 'trends' ? getTrendsTitle(taxonDetail)  : `This report was generated on the ${todayStr} using the South African Wildlife Population System (SAWPS). `}
                          The data presented is based on the following criteria.
                      </Box>
                      <Box className={'topper-detail'}>
                          <Grid container flexDirection={'row'} flexGrow={1}>
                              <Grid item xs>
                                  <Box><img className={'species-image'} src={speciesIcon} alt='Species image'/></Box>
                                  <Box className={'text-content'}><b>
                                      {tab === 'reports' ? `${selectedSpeciesListCount} Species` : selectedSpecies}
                                  </b></Box>
                              </Grid>
                              <Grid item xs>
                                  <img src="/static/images/separator.svg" alt='Separator'/>
                              </Grid>
                              <Grid item xs>
                                  <Box><img src="/static/images/organisation-topper.svg" alt='Organisation image'/></Box>
                                  <Box className={'text-content'}>
                                      <b>{organisationCount} Organisation{organisationCount > 1 ? 's' : ''}</b>
                                  </Box>
                              </Grid>
                              <Grid item xs>
                                  <img src="/static/images/separator.svg" alt='Separator'/>
                              </Grid>
                              <Grid item xs>
                                  <Box><img src="/static/images/property-topper.svg" alt='Property image'/></Box>
                                  <Box className={'text-content'}>
                                      <b>{propertyCount} {propertyCount > 1 ? 'Properties' : 'Property'}</b>
                                  </Box>
                              </Grid>
                              <Grid item xs>
                                  <img src="/static/images/separator.svg" alt='Separator'/>
                              </Grid>
                              <Grid item xs>
                                  <Box><img src="/static/images/clock-topper.svg" alt='Clock image'/></Box>
                                  <Box className={'text-content'}>
                                      <b>{startYearDisabled ? endYear : `${startYear} - ${endYear}`}</b>
                                  </Box>
                              </Grid>
                              {
                                  tab !== 'trends' && <>
                                      <Grid item xs>
                                          <img src="/static/images/separator.svg" alt='Separator'/>
                                      </Grid>
                                      <Grid item xs>
                                          <Box><img src="/static/images/activity-topper.svg" alt='Activity image'/></Box>
                                          <Box className={'text-content'}>
                                              <b>{activityCount} {activityCount > 1 ? 'Activities' : 'Activity'}</b>
                                          </Box>
                                      </Grid>
                                    </>
                              }
                          </Grid>
                      </Box>
                  </Box>
              </Box>
          </Box>
          <Box className={'topper-grey'} padding={'10px'}>
              <Box>
                  <b>Species list</b>: {tab === 'reports' ? selectedSpeciesList: selectedSpecies}
              </Box>
              <Box>
                  <b>Organisation list</b>: {organisationName}
              </Box>
              <Box>
                  <b>Property list</b>: {propertyName}
              </Box>
              {
                  tab != 'trends' && <>
                    <Box>
                      <b>Activity list</b>: {activityName}
                    </Box>
                </>
              }
          </Box>
      </Box>
    )
}

export default Topper;
