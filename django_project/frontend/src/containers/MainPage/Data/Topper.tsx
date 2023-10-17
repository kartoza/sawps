import React from "react";
import { Box, Button, Checkbox, ListItemText, Typography, Grid } from "@mui/material";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";


interface TopperProps {
    activity: string;
    organisationId: string;
    propertyId: string;
    endYear: number;
    startYear: number;
    species: string;
}


const Topper = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const activityId = useAppSelector((state: RootState) => state.SpeciesFilter.activityId)
    const propertyName = useAppSelector((state: RootState) => state.SpeciesFilter.propertyName)
    const organisationName = useAppSelector((state: RootState) => state.SpeciesFilter.organisationName)
    const organisationCount = organisationName ? organisationName.split(',').length : 0
    const propertyCount = propertyName ? propertyName.split(',').length : 0
    const activityCount = activityId !== '' ? activityId.split(',').length : 0
    const today = new Date().toLocaleDateString()

    return (
      <Box className={'topper-container'}>
          <Box>
              <Box padding={'10px'}>
                  <Box borderBottom={'thin solid'}>
                      <b>SAWPS SUMMARY REPORT</b>
                  </Box>
                  <Box>
                      <Box>
                          This report was generated on the {today} using the South African Wildlife Population System
                          (SAWPS).
                          The data presented is based on the following criteria.
                      </Box>
                      <Box className={'topper-detail'}>
                          <Grid container flexDirection={'row'} flexGrow={1}>
                              <Grid item xs>
                                  <Box><img src="/static/images/lion.svg" alt='Species image'/></Box>
                                  <Box className={'text-content'}><b>{selectedSpecies}</b></Box>
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
                                      <b>{startYear} - {endYear}</b>
                                  </Box>
                              </Grid>
                              <Grid item xs>
                                  <img src="/static/images/separator.svg" alt='Separator'/>
                              </Grid>
                              <Grid item xs>
                                  <Box><img src="/static/images/activity-topper.svg" alt='Activity image'/></Box>
                                  <Box className={'text-content'}>
                                      <b>{activityCount} {activityCount > 1 ? 'Activities' : 'Activity'}</b>
                                  </Box>
                              </Grid>
                          </Grid>
                      </Box>
                  </Box>
              </Box>
          </Box>
          <Box className={'topper-grey'} padding={'10px'}>
              <Box>
                  <b>Organisation list</b>: {organisationName}
              </Box>
              <Box>
                  <b>Property list</b>: {propertyName}
              </Box>
          </Box>
      </Box>
    )
}

export default Topper;