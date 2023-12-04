import React, {useEffect, useRef, useState} from "react";
import axios from "axios";
import {Box, Button, Grid, Typography} from "@mui/material";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import {useGetTaxonDetailQuery, useGetUserInfoQuery} from "../../../services/api";
import Topper from "../Data/Topper";
import './index.scss';
import NationalTrendSection from "./NationalTrendSection";
import ProvincialTrendSection from "./ProvincialTrendSection";
import PropertyTrendSection from "./PropertyTrendSection";

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/download/'

const Trends = () => {
  const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
  const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
  const provinceName = useAppSelector((state: RootState) => state.SpeciesFilter.selectedProvinceName).split(',')
  const [rerender, setRerender] = useState<boolean>(false)
  const contentRef = useRef(null);
  const {data: taxonDetail, isLoading: isTaxonDetailLoading, isSuccess} = useGetTaxonDetailQuery(selectedSpecies)
  const [isDownloadingJson, setIsDownloadingJson] = useState(false)
  const { data: userInfoData, isLoading: isUserInfoLoading, isSuccess: IsUserInfoSuccess } = useGetUserInfoQuery()

  // Declare errorMessage as a state variable
  const [showCharts, setShowCharts] = useState(false);

  const downloadTxtFile = () => {
    setIsDownloadingJson(true)
    let _data = {
      'species': selectedSpecies,
      'property': propertyId
    }
    axios.post(`${SPECIES_POPULATION_TREND_URL}`, _data, {
      responseType: 'blob',
    }).then((response) => {
        setIsDownloadingJson(false)
        if (response.data) {
          // create file link in browser's memory
          const href = URL.createObjectURL(response.data);

          // create "a" HTML element with href to file & click
          const link = document.createElement('a');
          link.href = href;
          link.setAttribute('download', `${selectedSpecies}.json`);
          document.body.appendChild(link);
          link.click();

          // clean up "a" element & remove ObjectURL
          document.body.removeChild(link);
          URL.revokeObjectURL(href);
        }
    }).catch((error) => {
        setIsDownloadingJson(false)
        console.log(error)
        if (
            error.request.responseType === 'blob' &&
            error.response.data instanceof Blob &&
            error.response.data.type &&
            error.response.data.type.toLowerCase().indexOf('json') != -1
        ) {
          error.response.data.text().then((text: string) => {
            let errorJSON = JSON.parse(text)
            if (errorJSON['detail']) {
              alert(errorJSON['detail'])
            }
          })
        }
    })
  }

  useEffect(() => {
    if (selectedSpecies) {
      setShowCharts(true)
    } else {
      setShowCharts(false)
    }
  }, [propertyId, selectedSpecies])

  useEffect(() => {
    if (taxonDetail?.id) {
      setRerender(true)
    }
  }, [isSuccess, taxonDetail])

  return (
    <Box className='main-content-wrap'>
      <Box className='main-content-area'>
        <Box className="charts-container">

          {showCharts ? (
            <>
            <Topper></Topper>
            <Grid container
                  ref={contentRef}
                  spacing={0}
                  direction="column"
                  alignItems="flex-start"
            >
              {selectedSpecies && rerender && (
                <Grid item xs={12} md={12} className="SectionItem" key={'NationalSectionItem'}>
                  <NationalTrendSection species={selectedSpecies} />
                </Grid>
              )}
              {selectedSpecies && rerender && (
                <Grid item xs={12} md={12} className="SectionItem" key={'ProvincialSectionItem'}>
                  <ProvincialTrendSection species={selectedSpecies} province={provinceName}/>
                </Grid>
              )}
              {selectedSpecies && rerender && userInfoData?.user_permissions.includes('Can view properties trends data') && (
                <Grid item xs={12} md={12} className="SectionItem" key={'PropertySectionItem'}>
                  <PropertyTrendSection species={selectedSpecies} property={propertyId} />
                </Grid>
              )}
            </Grid>
            </>
          ) : (
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
            { isDownloadingJson ?
              <Button
                disabled
                variant="contained"
                color="primary"
              >
                Downloading...
              </Button>:
              <Button
                onClick={downloadTxtFile}
                variant="contained"
                color="primary"
              >
                Download JSON Document
              </Button>
            }
          </Box>
        )}
      </Box>
    </Box>
  )
}

export default Trends
