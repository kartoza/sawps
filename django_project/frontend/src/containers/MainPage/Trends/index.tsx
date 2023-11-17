import React, {useEffect, useRef, useState} from "react";
import {Box, Button, Grid, Typography} from "@mui/material";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import {useGetTaxonDetailQuery} from "../../../services/api";
import Topper from "../Data/Topper";
import './index.scss';
import NationalTrendSection from "./NationalTrendSection";
import ProvincialTrendSection from "./ProvincialTrendSection";
import PropertyTrendSection from "./PropertyTrendSection";


const Trends = () => {
  const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
  const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
  const [rerender, setRerender] = useState<boolean>(false)
  const contentRef = useRef(null);
  const {data: taxonDetail, isLoading: isTaxonDetailLoading, isSuccess} = useGetTaxonDetailQuery(selectedSpecies)

  // Declare errorMessage as a state variable
  const [showCharts, setShowCharts] = useState(false);

  const downloadTxtFile = () => {
    // TODO: download should filter out property that are not selected in the filter
    // const element = document.createElement("a");
    // const file = new Blob([JSON.stringify(jsonDoc)], {type: 'text/plain'});
    // element.href = URL.createObjectURL(file);
    // element.download = `${selectedSpecies}.json`;
    // document.body.appendChild(element); // Required for this to work in FireFox
    // element.click();
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
    <Box>
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
                <ProvincialTrendSection species={selectedSpecies} />
              </Grid>
            )}
            {selectedSpecies && rerender && (
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
          <Button
            onClick={downloadTxtFile}
            variant="contained"
            color="primary"
          >
            Download JSON Document
          </Button>
        </Box>
      )}
    </Box>
  )
}

export default Trends
